from app import app
from flask import render_template, session, redirect, url_for
from wtforms.validators import InputRequired, NumberRange, Length

from wtforms import StringField, IntegerField, SelectMultipleField, \
    RadioField, TextAreaField, PasswordField, SubmitField

from theClass import User

import wtforms, flask_wtf, redis, hashlib, pickle


Red = redis.StrictRedis()
class LoginForm(flask_wtf.FlaskForm):
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    login = SubmitField()
    register = SubmitField()
    
testMan = User("nothing")
deck = testMan.getDeck()
@app.route('/login', methods=['post','get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.login.data:

            usernamePassword = pickle.loads(Red.get(form.username.data)).getPassword()
            value = hashlib.md5(form.password.data).hexdigest()
            if value == usernamePassword:
                print "logged in "+form.username.data
                session['user'] = form.username.data
                userClass = pickle.loads(Red.get(form.username.data))
                userClass.syncNow()
                for i in pickle.loads(Red.get(form.username.data)).exampleKnowDeck:
                   if i[2]<userClass.dateNow:
                       userClass.reviewDeck.append(i)
                       print userClass.reviewDeck
                for i in xrange(userClass.newCardsPerDay):
                    userClass.reviewDeck.append(deck.pop(i))
                return redirect(url_for('index'))
            print "username or password : incorrect"
        elif form.register.data:
            print "registering"
            if not Red.get(form.username.data):
                Red.set(form.username.data, pickle.dumps(User(hashlib.md5(form.password.data).hexdigest())))
    else:
        print "invalid form"
        #Red.set( key, value )

    return render_template('login.html', form=form)

class RequestForm(flask_wtf.FlaskForm):
    sentence = wtforms.StringField('Sentence', [wtforms.validators.InputRequired()])
    submit = wtforms.SubmitField()


class MainForm(flask_wtf.FlaskForm):
    answerBox = StringField("Answer here", [InputRequired()])
    submitAnswer = SubmitField()


@app.route('/', methods=['post', 'get'])
def index():
    '''
    Red.get("username")###
    return render_template("kanjiTable.html", data=deck)
    '''

    return render_template("interface.html", data=userClass)

