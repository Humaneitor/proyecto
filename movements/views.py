import requests
from movements import app 
from flask import render_template, request, redirect, url_for
import sqlite3 
from movements.forms import MovementForm, Status_Form
from datetime import date, datetime
from config import*
from movements.funcionalidades import *

now = datetime.now()
today = date.today() 
today_2 = "{}/{}/{}".format(today.year, today.month, today.day)
time = "{}:{:02d}:{:02d}".format(now.hour, now.minute,now.second)

url_coin = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"

def peticion(url):
    respuesta = requests.get(url) 
    if respuesta.status_code == 200:
        datos = respuesta.json() 
        return datos

@app.route('/')
def listaIngresos():
    
    form = MovementForm()
    mensajes = []
    
    try:
        ingresos = consulta('SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, precio FROM movimientos;')
    except Exception as e:
        print("**ERROR**🔧: Acceso a base de datos:{} - {}".format(type(e).__name__, e))
        mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")

        return render_template('movimientos.html', form=form, movimientos=[], mensajes=mensajes)
    
    return render_template("base.html", datos=ingresos, form = form)
    

@app.route('/compra', methods=['GET', 'POST'])
def nuevaCompra():
    

    form = MovementForm() 
    mensajes = []
    try:
        moneda_saldo = monedas_activas()   
        form.from_currency.choices=moneda_saldo      
        saldo_total = moneda_saldo_total()
    
    except Exception as e:
        print("**ERROR**🔧: Acceso a base de datos:{} - {}".format(type(e).__name__, e))
        mensajes.append("Error en acceso a base de datos. Consulte con el administrador.")

        return render_template("compra.html", form = form, vacio = True,mensajes=mensajes)

    if request.method == 'POST' and form.validate(): 
        if form.calculadora.data == True:
            try:
                amount = form.from_cantidad.data 
                symbol = form.from_currency.data
                convert = form.to_currency.data
                respuesta = peticion(url_coin.format(amount, symbol, convert, API_KEY))
                cantidad_coin = respuesta['data']['quote'][convert]['price']

                pu = float(amount) / float(cantidad_coin)

                api_coin = [amount, symbol, convert, cantidad_coin,pu]
                return render_template("compra.html", form = form, api_coin = api_coin, vacio = False)
            except Exception as e:
                print("**ERROR**🔧: API - insert: {} - {}". format(type(e).__name__, e))
                mensajes.append("Error API. Consulte con el administrador.")
                return render_template("compra.html", form = form, mensajes = mensajes, vacio = True)
        else:
            try:       
                consulta('INSERT INTO movimientos (date, time, from_currency, from_quantity,to_currency, to_quantity, precio) VALUES (?, ?, ? , ? , ? , ?, ?);',       
                                (
                                    today_2,
                                    time,
                                    form.from_currency.data,
                                    float(form.from_cantidad.data),
                                    form.to_currency.data,
                                    float(form.to_cantidad.data), 
                                    float(form.precio_unitario.data)
                                )) 
                return redirect(url_for('listaIngresos'))
            except Exception as e:
                print("**ERROR**🔧: base de datos - insert: {} - {}". format(type(e).__name__, e))
                mensajes.append("Error base de datos. Consulte con el administrador.")

    else:
        return render_template("compra.html", form = form, vacio = True, mensajes = mensajes)


@app.route('/estado', methods =['GET'])
def Estado_Inversion():
    form = Status_Form()
    mensajes = []
    try: 
        ingresos = consulta('SELECT SUM(to_quantity) AS total, to_currency FROM movimientos WHERE from_currency = "EUR" GROUP BY to_currency')
        
        conversion = consulta('SELECT SUM(to_quantity) AS total, to_currency FROM movimientos WHERE to_currency="EUR"')

        ingresos_2 = consulta('SELECT SUM(from_quantity) AS total, from_currency FROM movimientos WHERE from_currency="EUR"')
        
        ingresos_2 = ingresos_2[0]['total']-conversion[0]['total']

        total = 0
        try: 
            for ingreso in ingresos:
                respuesta = peticion(url_coin.format(ingreso['total'], ingreso['to_currency'],"EUR", API_KEY))
                total += float(respuesta['data']['quote']['EUR']['price'])
            return render_template ("estado.html", form = form, valor_invertido=round(ingresos_2, 2), valor_actual=round(total, 8))
        except Exception as e:
            print("**ERROR**🔧: API - insert: {} - {}". format(type(e).__name__, e))
            mensajes.append("Error API. Consulte con el administrador.")
            return render_template ("estado.html", form = form, mensajes = mensajes)
    except Exception as e:
        print("**ERROR**🔧: base de datos - insert: {} - {}". format(type(e).__name__, e))
        mensajes.append("Error base de datos. Consulte con el administrador.")
    return render_template ("estado.html", form = form, mensajes = mensajes)