
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired



class MovementForm(FlaskForm):

    date = DateField('Fecha', validators=[DataRequired()])
    time = DateField('Hora', validators=[DataRequired()])

    #from_currency = StringField('From_Currency', validators=[DataRequired()])
    from_currency = SelectField('Moneda origen', choices=('EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA'), validators=[DataRequired()])
    from_quantity = FloatField('Cantidad de moneda de origen', validators=[DataRequired()])

    to_currency = SelectField('Moneda origen', choices=('EUR', 'ETH', 'LTC', 'BNB', 'EOS', 'XLM', 'TRX', 'BTC', 'XRP', 'BCH', 'USDT', 'BSV', 'ADA'), validators=[DataRequired()])
    to_quantity = FloatField('Cantidad de moneda de destino', validators=[DataRequired()])

    submit = SubmitField('Aceptar')