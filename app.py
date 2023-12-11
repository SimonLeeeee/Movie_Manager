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
    id = db.Column(db.String(4), primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影标题
    release_date = db.Column(db.String(15)) # 电影年份
    country = db.Column(db.String(10)) # 电影国家
    type = db.Column(db.String(10)) # 电影类型
    year = db.Column(db.String(4)) # 电影年份
    box = db.Column(db.Float)  # 票房（单位亿元）

class Actor(db.Model): # 表名将会是 actor
    id = db.Column(db.String(4), primary_key=True) # 主键
    actor_name = db.Column(db.String(20)) # 演员名字
    gender = db.Column(db.String(2)) # 演员性别
    country = db.Column(db.String(20)) # 演员国籍

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
        ['1001', '战狼2', '2017/7/27', '中国', '战争', '2017', 56.84],
        ['1002', '哪吒之魔童降世', '2019/7/26', '中国', '动画', '2019', 50.15],
        ['1003', '流浪地球', '2019/2/5', '中国', '科幻', '2019', 46.86],
        ['1004', '复仇者联盟4', '2019/4/24', '美国', '科幻', '2019', 42.5],
        ['1005', '红海行动', '2018/2/16', '中国', '战争', '2018', 36.5],
        ['1006', '唐人街探案2', '2018/2/16', '中国', '喜剧', '2018', 33.97],
        ['1007', '我不是药神', '2018/7/5', '中国', '喜剧', '2018', 31],
        ['1008', '中国机长', '2019/9/30', '中国', '剧情', '2019', 29.12],
        ['1009', '速度与激情8', '2017/4/14', '美国', '动作', '2017', 26.7],
        ['1010', '西虹市首富', '2018/7/27', '中国', '喜剧', '2018', 25.47],
        ['1011', '复仇者联盟3', '2018/5/11', '美国', '科幻', '2018', 23.9],
        ['1012', '捉妖记2', '2018/2/16', '中国', '喜剧', '2018', 22.37],
        ['1013', '八佰', '2020/08/21', '中国', '战争', '2020', 30.10],
        ['1014', '姜子牙', '2020/10/01', '中国', '动画', '2020', 16.02],
        ['1015', '我和我的家乡', '2020/10/01', '中国', '剧情', '2020', 28.29],
        ['1016', '你好，李焕英', '2021/02/12', '中国', '喜剧', '2021', 54.13],
        ['1017', '长津湖', '2021/09/30', '中国', '战争', '2021', 53.48],
        ['1018', '速度与激情9', '2021/05/21', '中国', '动作', '2021', 13.92]
    ]

    actors = [
        ['2001', '吴京', '男', '中国'],
        ['2002', '饺子', '男', '中国'],
        ['2003', '屈楚萧', '男', '中国'],
        ['2004', '郭帆', '男', '中国'],
        ['2005', '乔罗素', '男', '美国'],
        ['2006', '小罗伯特·唐尼', '男', '美国'],
        ['2007', '克里斯·埃文斯', '男', '美国'],
        ['2008', '林超贤', '男', '中国'],
        ['2009', '张译', '男', '中国'],
        ['2010', '黄景瑜', '男', '中国'],
        ['2011', '陈思诚', '男', '中国'],
        ['2012', '王宝强', '男', '中国'],
        ['2013', '刘昊然', '男', '中国'],
        ['2014', '文牧野', '男', '中国'],
        ['2015', '徐峥', '男', '中国'],
        ['2016', '刘伟强', '男', '中国'],
        ['2017', '张涵予', '男', '中国'],
        ['2018', 'F·加里·格雷', '男', '美国'],
        ['2019', '范·迪塞尔', '男', '美国'],
        ['2020', '杰森·斯坦森', '男', '美国'],
        ['2021', '闫非', '男', '中国'],
        ['2022', '沈腾', '男', '中国'],
        ['2023', '安东尼·罗素', '男', '美国'],
        ['2024', '克里斯·海姆斯沃斯', '男', '美国'],
        ['2025', '许诚毅', '男', '中国'],
        ['2026', '梁朝伟', '男', '中国'],
        ['2027', '白百何', '女', '中国'],
        ['2028', '井柏然', '男', '中国'],
        ['2029', '管虎', '男', '中国'],
        ['2030', '王千源', '男', '中国'],
        ['2031', '姜武', '男', '中国'],
        ['2032', '宁浩', '男', '中国'],
        ['2033', '葛优', '男', '中国'],
        ['2034', '范伟', '男', '中国'],
        ['2035', '贾玲', '女', '中国'],
        ['2036', '张小斐', '女', '中国'],
        ['2037', '陈凯歌', '男', '中国'],
        ['2038', '徐克', '男', '中国'],
        ['2039', '易烊千玺', '男', '中国'],
        ['2040', '林诣彬', '男', '美国'],
        ['2041', '米歇尔·罗德里格兹', '女', '美国'],
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(id = m[0], title=m[1], release_date=m[2], country=m[3], type=m[4],year=m[5],box=m[6])
        db.session.add(movie)

    for a in actors:
        actor = Actor(id=a[0], actor_name=a[1], gender=a[2], country=a[3])
        db.session.add(actor)

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
        id = request.form['movie_id']
        title = request.form['title']
        release_date = request.form['release_date']
        country = request.form['country']
        type = request.form['type']
        year = request.form['year']
        box = request.form['box']

        if not title or len(year) > 4 or len(title) > 60 or len(release_date)>15 or len(country)>10 or len(type)>10:
            flash('Invalid input.')
            return redirect(url_for('index'))

        movie = Movie(id = id, title=title, year=year, release_date=release_date, country=country,type=type,box=box)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/actor_info', methods=['GET', 'POST'])
def actor_info():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('actor_info'))

    if request.method == 'POST':
        actor_id = request.form['actor_id']
        actor_name = request.form['actor_name']
        gender= request.form['actor_gender']
        country = request.form['country']

        if not actor_id or not actor_name or not gender or not country or len(actor_id)>4 or len(actor_name) > 20 or len(gender) > 2 or len(country)>10 :
            flash('Invalid input.')
            return redirect(url_for('actor_info'))

        a = Actor(id = actor_id, actor_name=actor_name, gender=gender, country=country)
        db.session.add(a)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('actor_info'))

    actors = Actor.query.all()
    return render_template('actor_info.html', actors=actors)

@app.route('/movie_box', methods=['GET', 'POST'])
def movie_box():
    movies = Movie.query.all()
    sorted_movies = sorted(movies, key=lambda x: x.box, reverse=True)

    return render_template('movie_box.html', movies=sorted_movies)

@app.route('/search1', methods=['GET'])
def search1():
    query1 = request.args.get('Keyword_query', '')  # 获取查询参数
    query2 = request.args.get('Country_query', '')  # 获取查询参数
    query3 = request.args.get('Year_query', '')  # 获取查询参数

    # 在此执行数据库查询，使用 query 进行过滤
    movies = Movie.query.filter(
        (Movie.title.ilike(f"%{query1}%")) |
        (Movie.type.ilike(f"%{query1}%")) |
        (Movie.country.ilike(f"%{query1}%")),
        (Movie.country.ilike(f"%{query2}%")),
        (Movie.year.ilike(f"%{query3}%"))
    ).all()

    return render_template('index.html', movies=movies, query=query1)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        id = request.form['movie_id']
        title = request.form['title']
        release_date = request.form['release_date']
        country = request.form['country']
        type = request.form['type']
        year = request.form['year']
        box = request.form['box']

        if not title or len(year) > 4 or len(title) > 60 or len(release_date)>15 or len(country)>10 or len(type)>10:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.id = id
        movie.title = title
        movie.release_date = release_date
        movie.country = country
        movie.type = type
        movie.year = year
        movie.box = box
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

@app.route('/actor_info/delete1/<int:actor_id>', methods=['POST'])
@login_required
def delete1(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('actor_info'))

@app.route('/actor_info/search2', methods=['GET'])
def search2():
    query1 = request.args.get('Name_query', '')  # 获取查询参数
    query2 = request.args.get('Gender_query', '')  # 获取查询参数
    query3 = request.args.get('Country_query', '')  # 获取查询参数

    # 在此执行数据库查询，使用 query 进行过滤
    actors = Actor.query.filter(
        (Actor.actor_name.ilike(f"%{query1}%")) ,
        (Actor.gender.ilike(f"%{query2}%")) ,
        (Actor.country.ilike(f"%{query3}%"))
    ).all()

    return render_template('actor_info.html', actors=actors,query = query1)
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
