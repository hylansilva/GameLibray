from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Games
from helpers import recovery_image, delete_image, GameForm
import time


# INITIAL ROUTE
@app.route('/')
def index():
    games = Games.query.order_by(Games.id)
    return render_template('lista.html', title='Games', games=games)


# CREATE
@app.route('/new')
def new_game():
    if 'loggeduser' not in session or session['loggeduser'] is None:
        return redirect(url_for('login', next=url_for('new_game')))
    form = GameForm()
    return render_template('novo.html', title='Add new Game', form=form)


@app.route('/add', methods=['POST', ])
def add_game():
    form = GameForm(request.form)

    if not form.validate_on_submit():
        redirect(url_for('new_game'))

    name = form.name.data
    category = form.category.data
    console = form.console.data
    game = Games.query.filter_by(name=name).first()
    if game:
        flash('Games alredy exists')
        return redirect(url_for('index'))
    new = Games(name=name, category=category, console=console)
    db.session.add(new)
    db.session.commit()
    upload_path = app.config['UPLOAD_PATH']
    file = request.files['file']
    file.save(f'{upload_path}/cover{new.id}.jpg')
    return redirect(url_for('index'))


# UPDATE
@app.route('/edit/<int:id>')
def edit(id):
    if 'loggeduser' not in session or session['loggeduser'] is None:
        return redirect(url_for('login', next=url_for('edit', id=id)))
    game = Games.query.filter_by(id=id).first()
    form = GameForm()
    form.name.data = game.name
    form.category.data = game.category
    form.console.data = game.console
    game_cover = recovery_image(id)
    return render_template('edit.html', title='Edit Game', id=id, game_cover=game_cover, form=form)


@app.route('/update', methods=['POST', ])
def update_game():
    form = GameForm(request.form)

    if form.validate_on_submit():
        game = Games.query.filter_by(id=request.form['id']).first()
        game.name = form.name.data
        game.category = form.category.data
        game.console = form.console.data

        db.session.add(game)
        db.session.commit()

        upload_path = app.config['UPLOAD_PATH']
        file = request.files['file']
        timestamp = time.time()
        delete_image(game.id)
        file.save(f'{upload_path}/cover{game.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


# DELETE
@app.route('/del/<int:id>')
def delete(id):
    if 'loggeduser' not in session or session['loggeduser'] is None:
        return redirect(url_for('login'))
    Games.query.filter_by(id=id).delete()
    db.session.commit()
    flash('the game has been deleted')
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory('uploads', filename)

