from movements import app
from movements.forms import MovementForm
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from datetime import date

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

        if form.validate():
            consulta('INSERT INTO movements (date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES (?, ?, ? ,? ,?, ? );', 
                        (   
                            form.date.data,
                            form.time.data,
                            form.from_currency.data,
                            form.from_quantity.data,
                            form.to_currency.data,
                            fotm.to_quantity.data
                        )
                    )
            return redirect(url_for('listaIngresos'))
            
        else:
            return render_template("alta.html", form=form)
    return render_template("alta.html", form=form)


@app.route("/modifica/<id>", methods=['GET', 'POST'])
def modificaIngreso(id):
    
    if request.method == 'GET':

        registro = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos where id = ?', (id,))[0] 
        registro['fecha'] = date.fromisoformat(registro['fecha'])
        form = MovementForm(data=registro)

        return render_template("modifica.html", form=form, id=id)

    else:
        form = MovementForm()
        if form.validate():
            consulta('UPDATE movimientos SET fecha = ?, concepto= ?, cantidad = ? WHERE id = ?',
                    (
                    request.form.get('fecha'),
                    request.form.get('concepto'),
                    float(request.form.get('cantidad')),
                    id
                    )
            )

            return redirect(url_for("listaIngresos"))
        else:
            return render_template("modifica.html", form=form, id=id)

@app.route("/elimina/<id>", methods=['GET', 'POST'])
def eliminaIngreso(id):
    
    if request.method == 'GET':

        registro = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos where id = ?', (id,))[0] 
        registro['fecha'] = date.fromisoformat(registro['fecha'])
        form = MovementForm(data=registro)

        return render_template("elimina.html", form=form, id=id)

    else:
        form = MovementForm()
        if form.validate():
            consulta('DELETE FROM movimientos WHERE id = ?', (id,))
            return redirect(url_for("listaIngresos"))
        else:
            return render_template("elimina.html", form=form, id=id)