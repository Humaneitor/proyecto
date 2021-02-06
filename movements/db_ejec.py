import sqlite3
from config import*
from movements import app
from datetime import date
from datetime import datetime

DBFILE = app.config['DBFILE'] 

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


def monedas_activas(): 

    cryto_money = ['BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX']

    movimientos = consulta('SELECT from_currency,from_quantity, to_currency, to_quantity  FROM movimientos;')

    lista_from = ['EUR']

    counter_cantidad = 0 

    for i in movimientos: 
        if i['to_currency'] != 'EUR' and i['to_currency'] not in lista_from:
            lista_from.append(i['to_currency'])
    return lista_from 

def moneda_saldo_total():

    saldo_to_currency = consulta('SELECT to_currency, sum(to_quantity) FROM movimientos GROUP BY to_currency;' )

    saldo_from_currency = consulta('SELECT from_currency, sum(from_quantity) FROM movimientos GROUP BY from_currency;' )

    lista_to_prueba = []
    for i in saldo_to_currency:
        lista_to_prueba.append((i['to_currency'], i['sum(to_quantity)']))

    lista_from_prueba = []
    for i in saldo_from_currency:
        lista_from_prueba.append((i['from_currency'], i['sum(from_quantity)']))

    dic_saldo = {}
    for i in lista_to_prueba:
        dic_saldo[i[0]] = i[1]
    for b in lista_from_prueba:
        if b[0] in dic_saldo:
            dic_saldo[b[0]] = dic_saldo[b[0]] - b[1]
    
    return dic_saldo


now = datetime.now()
today = date.today() 
today_2 = "{}/{}/{}".format(today.year, today.month, today.day)
now = datetime.now() 
time = "{}:{:02d}:{:02d}".format(now.hour, now.minute,now.second)