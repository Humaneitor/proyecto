from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError
from wtforms import validators
from wtforms.fields.core import DecimalField, SelectField, TimeField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from datetime import date, datetime, timezone
from movements.db_ejec import moneda_saldo_total 



coin = ('EUR', 'BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX')

def validar_select(form, field):
    if form.from_currency.data == form.to_currency.data:
            raise ValidationError('Error: Monedas Iguales')

def validar_saldo(form, field):
    saldo_total = moneda_saldo_total()
    if form.from_currency.data == 'EUR':
        pass
    elif field.data > saldo_total[form.from_currency.data]:
        raise ValidationError('No tienes saldo de esta criptomoneda')

            

class MovementForm(FlaskForm):
    from_currency = SelectField('Moneda original que utilizas para comprar',choices = coin, validators=[validar_select])
    from_cantidad = FloatField('Cantidad de moneda original', validators= [DataRequired(), NumberRange(min=0.00000001, max=1000000000, message= "Error: Cantidad no válida"),validar_saldo]) 
    to_currency = SelectField('Moneda que quieres comprar', choices = coin)
    to_cantidad = DecimalField('Cantidad que vas a comprar al cambio')
    precio_unitario = DecimalField ('Precio Unitario')
    calculadora = SubmitField("Calcular Operación")
    guardar = SubmitField ('Confirmar y comprar operación')


class Status_Form(FlaskForm): 
    invertido = DecimalField('Euros invertidos en la compra')
    valor_actual = DecimalField('Valor actual de tu inversión')