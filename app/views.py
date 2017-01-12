from app import app
from flask import render_template, session, redirect, url_for
import wtforms
import flask_wtf
import redis
from wtforms.validators import InputRequired, NumberRange, Length
from wtforms import StringField, IntegerField, SelectMultipleField, \
    RadioField, TextAreaField, PasswordField, SubmitField
import hashlib
import pandas as pd


df  = pd.read_excel('/Users/jacobferragut/gogo/app/templates/gogoKanjiKanji.xlsx',0) 
print df
Red = redis.StrictRedis()
class LoginForm(flask_wtf.FlaskForm):
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    login = SubmitField()
    register = SubmitField()

@app.route('/login', methods=['post','get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.login.data:
            passwordRedis = Red.get("password:"+form.username.data)
            value = hashlib.md5(form.password.data).hexdigest()
            if value == passwordRedis:
                print "logged in "+form.username.data
                session['user'] = form.username.data
                return redirect(url_for('index'))
            print "username or password : incorrect"
        elif form.register.data:
            print "registering"
            if not Red.get("password:"+form.username.data):
                Red.set( "password:"+form.username.data, hashlib.md5(form.password.data).hexdigest())
    else:
        print "invalid form"
        #Red.set( key, value )

    return render_template('login.html', form=form)

@app.route('/test/', methods=['post','get'])
def main0():
    parsedData = 0
    
    form = RequestForm()
    if form.validate_on_submit():
        #parse sentence from the form
        parsedData = app.parser(form.sentence.data)
        sents = []
        sents = parsedData.sents
        for span in parsedData.sents:
            sent = [parsedData[i] for i in range(span.start, span.end)]
            break
    lists = []
    try:    
        for token in sent:
            listy=[token.orth_, token.pos_, token.dep_,token.head.orth_]
            lists.append(listy)
            print(listy)
            
        #print parsedData
        return render_template('base.html', form=form, title = "home", data = lists)
    except: 
        return render_template('base.html', form = form, title = "home")    

class RequestForm(flask_wtf.FlaskForm):
    sentence = wtforms.StringField('Sentence', [wtforms.validators.InputRequired()])
    submit = wtforms.SubmitField()


class MainForm(flask_wtf.FlaskForm):
    answerBox = StringField("Answer here", [InputRequired()])
    submitAnswer = SubmitField()


@app.route('/')
def index():
    form = MainForm()
    if form.validate_on_submit():
        if form.main.data:
            return render_template('main.html', form=form)





