from enum import unique
from flask import Flask, render_template,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from newsapi import NewsApiClient

app = Flask(__name__)
app.config['SECRET_KEY']='Thhisissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Project/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager =  LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password', validators=[InputRequired(), Length(min= 8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

def GetNews(source,ctr):
    newsapi = NewsApiClient(api_key="38122ac1faf54ee2acdbc704e062cd89")
    topheadlines = newsapi.get_top_headlines(sources=source, category=ctr, page_size=90, page=1,language='en')

    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    url = []

    for i in range (len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])

    myList = zip(news, desc, img, url)    
    return myList


@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1> Invalid username or password </h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    """
    newsapi = NewsApiClient(api_key="38122ac1faf54ee2acdbc704e062cd89")
    topheadlines = newsapi.get_everything(sources="bbc-news,the-verge,axios,ary-news,ansa,abc-news", page_size=90, page=1,language='en')

    articles = topheadlines['articles']

    desc = []
    news = []
    img = []
    url = []

    for i in range (len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])

    myList = zip(news, desc, img, url)
    """
    
    dash = GetNews(source="bbc-news,the-verge,axios,ary-news,ansa,abc-news", ctr=None)

    return render_template('dashboard.html', name=current_user.username, context=dash)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/business')
@login_required
def business():

    politic = GetNews(source=None, ctr="business")

    return render_template('business.html', name=current_user.username, context=politic)

@app.route('/health')
@login_required
def health():

    health = GetNews(source=None, ctr="health")

    return render_template('health.html', name=current_user.username, context=health)

@app.route('/entertainment')
@login_required
def entertainment():

    entertainment = GetNews(source=None, ctr="entertainment")

    return render_template('entertainment.html', name=current_user.username, context=entertainment)

@app.route('/sports')
@login_required
def sports():

    sports = GetNews(source=None, ctr="sports")

    return render_template('sports.html', name=current_user.username, context=sports)

@app.route('/technology')
@login_required
def technology():

    technology = GetNews(source=None, ctr="technology")

    return render_template('technology.html', name=current_user.username, context=technology)

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html', name=current_user.username)

if __name__ == '__main__':
    app.run(debug=True)