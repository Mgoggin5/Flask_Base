from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import DataRequired, ValidationError, DataRequired, \
    Email, EqualTo, Length
from app.models import User, Host


# class HostForm(FlaskForm): 
#     hostname = StringField(_l('Hostname'), validators = [DataRequired()])

#     def validate_hostname(self, hostname):  
#         hostname = Host