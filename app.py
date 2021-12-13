import bcrypt
from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
import sqlite3
import os
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='thisisasecertkey'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

login_manager  = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique = True,nullable= False)
    password = db.Column(db.String(80),unique = True,nullable = False)
    def __repr__(self):
        return self.username

class question(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question = db.Column(db.String(256),unique = False,nullable = False)
    answer = db.Column(db.String(256),unique = False,nullable = False)
    difficulty = db.Column(db.String(256),unique = False,nullable = False)
    catergory_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    def __repr__(self):
        return self.id

class leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.String(256),unique = False, nullable = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('leaderboard', lazy=True))
    ques_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    question = db.relationship('question', backref=db.backref('leaderboard',lazy=True))


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min = 4,max=20)],render_kw={"placeholder":"username"})
    password = PasswordField(validators=[InputRequired(),Length(min = 4,max=20)],render_kw={"placeholder":"password"})
    submit = SubmitField('Register')
    def validate_user(self,username):
        existingusername = User.query.filter_by(username = username.data).first()
        if existingusername:
            raise ValidationError("the user already exists")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min = 4,max=20)],render_kw={"placeholder":"username"})
    password = PasswordField(validators=[InputRequired(),Length(min = 4,max=20)],render_kw={"placeholder":"password"})
    submit = SubmitField('Login in')


class AnswerForm(FlaskForm):
    answer = StringField(validators=[InputRequired(),Length(min = 1,max=30)],render_kw={"placeholder":"answer"})
    submit = SubmitField('Submit Answer')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        temp = User.query.filter_by(username= form.username.data).first()
        if temp:
            if bcrypt.check_password_hash(temp.password,form.password.data):
                login_user(temp)
                return redirect(url_for('dashboard'))
    return render_template('login.html',form = form)

@app.route('/logout',methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard',methods = ['GET','POST'])
@login_required
def dashboard():

    return render_template('dashboard.html')

@app.route('/correct',methods=['GET','POST'])
@login_required
def correctanswer():
    return render_template('correct.html')




@app.route('/questionpage/<int:idvalue>',methods = ['GET','POST'])
@login_required
def questionpage(idvalue):
    form = AnswerForm()
    temp = question.query.filter_by(id=idvalue)
    if form.validate_on_submit():
        usersanswer = form.answer.data
        print('i am in the form ')
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            temp = cur.execute("select answer from question where id = ?",(idvalue,))
            answer  = str(temp.fetchone()[0])
        if usersanswer == answer:
            print('i am here')
            return render_template('correct.html')
    print('i am outside')
    return render_template('questionpage.html',query = temp,form= form)


@app.route('/leaderboard',methods = ['GET','POST'])
@login_required
def leaderboard():
    lb = leaderboard.query.all()
    return render_template('leaderboard.html', lb = lb)


@app.route('/register',methods = ['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashedpassword = bcrypt.generate_password_hash(form.password.data)
        newuser = User(username = form.username.data,password = hashedpassword)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html',form = form)

if __name__ == '__main__':
    app.run(debug=True)
