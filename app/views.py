from app import app
from flask import render_template, session, redirect, url_for
import wtforms
import flask_wtf
import redis
from wtforms.validators import InputRequired, NumberRange, Length
from wtforms import StringField, IntegerField, SelectMultipleField, \
    RadioField, TextAreaField, PasswordField, SubmitField
import hashlib
from theClass import user

Red = redis.StrictRedis()
class LoginForm(flask_wtf.FlaskForm):
    username = StringField("Username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    login = SubmitField()
    register = SubmitField()
testMan = user("nothing")
deck = testMan.getDeck()
@app.route('/login', methods=['post','get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.login.data:
            usernamePassword = Red.get(form.username.data).getPassword()
            value = hashlib.md5(form.password.data).hexdigest()
            if value == usernamePassword:
                print "logged in "+form.username.data
                session['user'] = form.username.data
                return redirect(url_for('index'))
            print "username or password : incorrect"
        elif form.register.data:
            print "registering"
            if not Red.get(form.username.data):
                Red.set(form.username.data, user(hashlib.md5(form.password.data).hexdigest()))
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

htmlFile = '''
<p>Japanese Kanji List</p>
<div class=row>
    <div class="col-xs-6 col-md-4">
<table align = "center">
<tr>
    <th>Kanji</th>
    <th>English</th>
    <th>Days</th>
</tr>
{% for card in data %}
    <tr>
    {% for element in card %}
        <td>{{element}}</td>
    {% endfor %}
    </tr>
{% endfor %}
'''
@app.route('/', methods=['post', 'get'])
def index():
    return render_template("kanjiTable.html", data=deck)





