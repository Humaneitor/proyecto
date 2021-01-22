
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired
import sqlite3
from movements import app

DBFILE = app.config['DBFILE']

def ask(query, params=()):
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



class MovementForm(FlaskForm):
    disponibles = ask('SELECT to__currency FROM movements;')

    listadisponibles=[]

    listadisponibles.append('EUR')

    for elemento in disponibles:
        if elemento['to__currency'] not in listadisponibles:
            listadisponibles.append(elemento['to__currency'])

    print (listadisponibles)

    date = StringField('Fecha')
    time = StringField('Hora')




    #from_currency = StringField('From_Currency', validators=[DataRequired()])
    from_currency = SelectField('Moneda origen', choices=listadisponibles, validators=[DataRequired()])
    from_quantity = FloatField('Cantidad de moneda de origen', validators=[DataRequired()])
    

    to__currency = SelectField('Moneda destino', choices=('EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA'), validators=[DataRequired()])
    submit = SubmitField('Calcular')
    to_quantity = FloatField('Cantidad de moneda de destino', validators=[DataRequired()])

    submit = SubmitField('Comprar')