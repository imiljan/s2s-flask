from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from .models import User


class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(1, 64)])
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Username is required'),
                                                   Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(message='Email is required'),
                                             Length(min=1, max=128), Email()])
    password = PasswordField('Password', validators=[DataRequired('Password is required'),
                                                     Length(1, 64)])
    confirm = PasswordField('Confirm password', validators=[DataRequired(message='Confirm is required'),
                                                            EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username in use!')


class PostForm(FlaskForm):
    # username = StringField('username', validators=[DataRequired()])
    post = StringField('post', validators=[DataRequired()])
