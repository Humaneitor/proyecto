from movements import app
from movements.forms import MovementForm
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from datetime import date, datetime

DBFILE = app.config['DBFILE']
monedas = ('EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA')

def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    c.execute(query, params)
    conn.commit()

    filas = c.fetchall()
    conn.close()


    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

@app.route('/')
def listaIngresos():

    ingresos = consulta('SELECT date, time, from_currency, from_quantity, to__currency, to_quantity FROM movements;')

    return render_template("movementsList.html", datos=ingresos)

@app.route('/creaalta', methods=['GET', 'POST'])


def nuevoIngreso():
    



    form = MovementForm()
    
    if request.method == 'POST':
        now = datetime.now()
        today =date.today()
        fecha = today
        hora = now.time()
        form.date.data = str(fecha)
        form.time.data = str(hora)

        

        if form.validate():

            consulta('INSERT INTO movements (date, time, from_currency, from_quantity, to__currency, to_quantity) VALUES (?, ?, ? , ?, ?, ?);', 
                        (   
                            form.date.data,
                            form.time.data,
                            form.from_currency.data,
                            form.from_quantity.data,
                            form.to__currency.data,
                            form.to_quantity.data
                        )
                    )
            return redirect(url_for('listaIngresos'))
            
        else:
            return render_template("alta.html", form=form)
    return render_template("alta.html", form=form)