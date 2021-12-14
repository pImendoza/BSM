import bcrypt
from flask import Flask,render_template,url_for,redirect,session,flash,g
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
import sqlite3
from time import time
import os
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
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


def query_database(query, args=(), one=False):
    with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute(query, args)
    rv = [dict((cur.description[idx][0], value)for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def timestamp():
    return str(int(time()))

def postatopic(subject, content):
    with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute("insert into topic (subject) values (?)",(subject,))
            temp = cur.execute("select topic_id from topic where subject = ? ",(subject,))
    temp1 = temp.fetchone()[0]
    topic_id = temp1
    topic_id = str(topic_id)
    postareply(topic_id, content)
    return topic_id

def postareply(topic_id, content):
    g.user = current_user.get_id()
    user_value = str(g.user)
    with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO reply (topic_id, time, content, author) values (?, ?, ?, ?)",(topic_id, timestamp(), content,user_value))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20),unique = True,nullable= False)
    password = db.Column(db.String(80),unique = True,nullable = False)


class questions(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question = db.Column(db.String(256),unique = False,nullable = False)
    answer = db.Column(db.String(256),unique = False,nullable = False)
    difficulty = db.Column(db.String(256),unique = False,nullable = False)
    catergory = db.Column(db.String(256),unique = False,nullable = False)



class leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.String(256),unique = False, nullable = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    ques_id = db.Column(db.Integer,db.ForeignKey('question.id'))

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


class ReplyForm(FlaskForm):
    content = TextAreaField("Reply", validators=[InputRequired()])
    submit = SubmitField('reply')

class NewTopicForm(FlaskForm):
    subject = StringField("Subject", validators=[InputRequired()])
    content = TextAreaField("Reply", validators=[InputRequired()])
    submit = SubmitField('create new post')


#db.create_all()
    
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

@app.route('/topic',methods = ['GET','POST'])
@login_required
def topicmethod():
    topics = query_database("SELECT * FROM topic ORDER BY (SELECT MAX(time) FROM reply WHERE reply.topic_id = topic.topic_id) DESC")
    for topic in topics:
        reply_count = query_database("SELECT count(*) FROM reply WHERE topic_id = ?",[topic["topic_id"]], one=True)["count(*)"]
        topic["replies"] = reply_count - 1
        last_reply = query_database("SELECT time FROM reply WHERE topic_id = ? ORDER BY time DESC LIMIT 1", [topic["topic_id"]], one=True)
        topic["last_reply_date"] = last_reply
    return render_template('blog.html',topics = topics)


@app.route('/topic/new', methods=['GET', 'POST'])
def new_topic():
    form = NewTopicForm()
    if form.validate_on_submit():
        new_topic_id = postatopic(form.subject.data, form.content.data)
        flash("New topic posted.")
        return redirect('/topic/' + new_topic_id)
    return render_template("newtopic.html", form=form)

@app.route('/topic/<topic_id>', methods=['GET', 'POST'])
def view_topic(topic_id):
    subject = query_database("SELECT subject FROM topic WHERE topic_id = ?", [topic_id], one=True)
    form = ReplyForm()
    if form.validate_on_submit():
        postareply(topic_id, form.content.data)
    replies = query_database("SELECT * FROM reply WHERE topic_id = ? ORDER BY time",[topic_id])
    return render_template("topic.html", subject=subject, replies=replies, 
                           form=form)




@app.route('/correct',methods=['GET','POST'])
@login_required
def correctanswer():
    end = timer()
    c_time = str(end-start)
            
    g.user = current_user.get_id()
    user_value = str(g.user)
    

    L = leaderboard(time = c_time, user_id = user_value, ques_id = c_ques)
    db.session.add(L)
    db.session.commit()
    return render_template('correct.html')




@app.route('/questionpage/<int:idvalue>',methods = ['GET','POST'])
@login_required
def questionpage(idvalue):
    form = AnswerForm()
    temp = questions.query.filter_by(id=idvalue)
    if form.validate_on_submit():
        usersanswer = form.answer.data
        print('i am in the form ')
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            temp = cur.execute("select answer from question where id = ?",(idvalue,))
            answer  = str(temp.fetchone()[0])
        if usersanswer == answer:
            print('i am here')
            global c_ques 
            QP_temp = cur.execute("select id from questions where id = ?",(idvalue,))
            c_ques = str(QP_temp.fetchone()[0])

            return redirect(url_for('correctanswer')) 
    print('i am outside')
    return render_template('questionpage.html',query = temp,form= form)


@app.route('/leaderboard',methods = ['GET','POST'])
@login_required
def Leaderboard():
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
