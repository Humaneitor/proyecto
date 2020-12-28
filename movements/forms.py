
from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length



class MovementForm(FlaskForm):

    tipo = StringField('Tipo')
    fecha = DateField('Fecha', validators=[DataRequired()])
    concepto = StringField('Concepto', validators=[DataRequired(), Length(min=5, message="El concepto debe tener más de 5 caracteres")])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])

    submit = SubmitField('Aceptar')