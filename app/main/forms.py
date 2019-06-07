from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import Required,Email,EqualTo
from ..models import User
from wtforms import ValidationError

class ContactForm(FlaskForm):
   name = StringField('Your name')
   email = StringField('Your email')
   message = TextAreaField('Message')
   submit = SubmitField('Send')

class UpdateProfile(FlaskForm):
   bio = TextAreaField('Tell us about you.',validators = [Required()])
   submit = SubmitField('update bio')