from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, FileForm
from app.models import User, Photo
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import logging
import os
import sys

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user = User.query.get(current_user.id)
    photos = user.photos.all()
    
    form = FileForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)

        basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/photos')
        f.save(os.path.join(basedir, filename))
        
        user = User.query.get(current_user.id)
        photo = Photo(file_name=filename, owner=user)
        
        db.session.add(photo)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form, photos=photos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)