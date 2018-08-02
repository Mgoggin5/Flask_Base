from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import DataRequired, ValidationError, DataRequired, \
    Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


