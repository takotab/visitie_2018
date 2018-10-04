from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, Email, EqualTo, DataRequired

from visitatie.data_models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ChangeInfoForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [Email(), DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user.username == username.data:
            print(user.username, username.data)
        else:
            if user is not None:
                raise ValidationError('Gebruik alstublieft een ander username.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Gebruik alstublieft een ander email-adres.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField(
            'Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Gebruik alstublieft een ander username.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Gebruik alstublieft een ander email-adres.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Vraag een nieuw wachtword aan.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField(
            'Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
