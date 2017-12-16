from datetime import datetime

from app import app, db
from flask import render_template, redirect, url_for, g, flash
from flask_login import current_user, login_required, login_user, logout_user
from .models import User, Post

from app.forms import SigninForm, PostForm, SignupForm


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/index/<int:page>', methods=['GET'])
def index(page=1):
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 6, False)
    return render_template('index.html', posts=posts)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))
    form = SigninForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is not None and u.verify_password(form.password.data):
            login_user(u, remember=form.remember_me.data)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('signin.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data,
                 password=form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('You can now login! :D')
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)




@app.route("/home", methods=['GET', 'POST'])
@app.route("/home/<int:page>", methods=['GET', 'POST'])
@login_required
def home(page=1):
    if not g.user.is_authenticated:
        return render_template(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        form = PostForm()
        if form.validate_on_submit():
            post = Post(body=form.post.data,
                        timestamp=datetime.utcnow(), user=g.user)
            db.session.add(post)
            db.session.commit()
            flash('Your post is now live!')
            return redirect(url_for('home'))
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, 6, False)
    return render_template('home.html', form=form, posts=posts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def user(username, page=1):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, 10, False)
    return render_template('profile.html', user=user, posts=posts)


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.now()
        db.session.add(g.user)
        db.session.commit()
