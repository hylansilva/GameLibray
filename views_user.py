from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app
from models import Users
from helpers import LoginForm
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    next = request.args.get('next')
    form = LoginForm()
    return render_template('login.html', next=next, form=form)


@app.route('/auth', methods=['POST', ])
def auth():
    form = LoginForm(request.form)
    user = Users.query.filter_by(nickname=form.nickname.data).first()
    password = check_password_hash(user.password, form.password.data)
    if user and password:
        session['loggeduser'] = user.nickname
        flash('Wellcome ' + user.nickname + '!')
        next_page = request.form['next']
        return redirect(next_page)
    else:
        flash('user not found')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['loggeduser'] = None
    flash('Logout has Sucsesfull!')
    return redirect(url_for('index'))

