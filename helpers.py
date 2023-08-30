import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


class GameForm(FlaskForm):
    name = StringField('Name', [validators.data_required(), validators.Length(min=1, max=50)])
    category = StringField('Category', [validators.data_required(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.data_required(), validators.Length(min=1, max=20)])
    save = SubmitField('Save')


class LoginForm(FlaskForm):
    nickname = StringField('NickName', [validators.data_required(), validators.Length(min=1, max=20)])
    password = PasswordField('Password', [validators.data_required(), validators.Length(min=1, max=100)])
    login = SubmitField('Save')


def recovery_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in filename:
            return filename

    return 'default_cover.jpg'


def delete_image(id):
    file = recovery_image(id)
    if file != 'default_cover.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
