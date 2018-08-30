from flask_wtf import FlaskForm
from wtforms import StringField
from app.models import User

class InputForm(FlaskForm):
    text = StringField('text')
    submit_text = SubmitField('Post')
