# -*- coding: utf-8 -*-
import os
import sys
import click


from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

prefix = 'sqlite:///'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'

class Movie(db.Model): # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影标题
    release_date = db.Column(db.String(15)) # 电影年份
    country = db.Column(db.String(10)) # 电影国家
    type = db.Column(db.String(10)) # 电影类型
    year = db.Column(db.String(4)) # 电影年份

@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Simon Li'
    movies = [
        ['战狼2','2017/7/27','中国','战争','2017'],
        ['哪吒之魔童降世','2019/7/26','中国','动画','2019'],
        ['流浪地球','2019/2/5','中国','科幻','2019'],
        ['复仇者联盟4','2019/4/24','美国','科幻','2019'],
        ['红海行动','2018/2/16','中国','战争','2018'],
        ['唐人街探案2','2018/2/16','中国','喜剧','2018'],
        ['我不是药神','2018/7/5','中国','喜剧','2018'],
        ['中国机长','2019/9/30','中国','剧情','2019'],
        ['速度与激情8','2017/4/14','美国','动作','2017'],
        ['西虹市首富','2018/7/27','中国','喜剧','2018'],
        ['复仇者联盟3', '2018/5/11', '美国', '科幻', '2018'],
        ['捉妖记2', '2018/2/16', '中国', '喜剧', '2018'],
        ['八佰', '2020/08/21', '中国', '战争', '2020'],
        ['姜子牙', '2020/10/01', '中国', '动画', '2020'],
        ['我和我的家乡', '2020/10/01', '中国', '剧情', '2020'],
        ['你好，李焕英', '2021/02/12', '中国', '喜剧', '2021'],
        ['长津湖', '2021/09/30', '中国', '战争', '2021'],
        ['速度与激情9', '2021/05/21', '中国', '动作', '2021']
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m[0], release_date=m[1], country=m[2], type=m[3],year=m[4])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']
        country = request.form['country']
        type = request.form['type']
        year = request.form['year']

        if not title or len(year) > 4 or len(title) > 60 or len(release_date)>15 or len(country)>10 or len(type)>10:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(title=title, year=year, release_date=release_date, country=country,type=type)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']
        country = request.form['country']
        type = request.form['type']
        year = request.form['year']

        if not title or len(year) > 4 or len(title) > 60 or len(release_date)>15 or len(country)>10 or len(type)>10:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.release_date = release_date
        movie.country = country
        movie.type = type
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))
