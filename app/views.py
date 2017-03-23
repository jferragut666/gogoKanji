# -*- coding: utf-8 -*-
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
    
@app.route('/login', methods=['post','get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.login.data and (Red.get(form.username.data) != None):
            usernamePassword = pickle.loads(Red.get(form.username.data)).hashedPassword
            value = hashlib.md5(form.password.data).hexdigest()
            if value == usernamePassword:
                print "logged in "+form.username.data
                session['user'] = form.username.data
                user_object = pickle.loads(Red.get(session['user']))
                user_object.updateDateNow() 
                numOfDueCards = 0
                for i in xrange(len(user_object.getOverDueDeck())):
                    if user_object.getOverDueDeck()[i][2] <= user_object.dateNow():
                        numOfDueCards+=1
                                    
                lenOfOverDueDeck = numOfDueCards + user_object.newCardsPerDay
                user_object.done = [False]*lenOfOverDueDeck

                if False in user_object.done:
                    user_object.overDueIndex = user_object.done.index(False)
                else:
                    #flash("done for today 0")
                    return "done for today 0"
                    
                Red.set(form.username.data, pickle.dumps(user_object))

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
    form = MainForm()
    #cardList = [0]
    '''
    [[["aa", "wowo", datetime(2014,5,1)], ["taite", "usually", datetime(2019, 6, 19)]], [[u"かばん", "bag", datetime(2000,4,19)],
                                    [u"大抵", "usually", datetime(2017,2,4)],
                                     [u"上", "above",datetime(2017,2,25)],
                                    [u"犬", "dog", datetime(2017,5,25)]]]
    '''

    interfaceUser = pickle.loads(Red.get(session['user']))
    interfaceUser.updateDateNow() 
    interfaceUser.updateTomorrowDate() 

    interfaceUser.appendNewCards() 
    interfaceUser.getOverDueDeck()
    index = interfaceUser.overDueIndex
    print "OverDue Deck", interfaceUser.overDueDeck
    print "OverDue Index", interfaceUser.overDueIndex

    if interfaceUser.overDueDeck[index][2] <= interfaceUser.dateNow:
        if form.validate_on_submit():
            if form.answerBox.data == interfaceUser.overDueDeck[index][1]:
                #flash("correct")
                interfaceUser.overDueDeck[index] = interfaceUser.supermemo(interfaceUser.overDueDeck[index])
                interfaceUser.done[index] = True
                if index + 1 < len(interfaceUser.overDueDeck):
                    for i in xrange(index+1,len(interfaceUser.overDueDeck)):
                        if interfaceUser.done[i] == False:
                            index = i
                            break
                elif False in interfaceUser.done: 
                    interfaceUser.overDueIndex = interfaceUser.done.index(False)
                else:
                    #flash("done for today")
                    return "done for today"
            else:
                #flash("incorrect")
                #return "incorrect"
                pass
            
    else:
        print "interfaceUser.overDueDeck[interfaceUser.overDueIndex][2] > interfaceUser.dateNow"



    Red.set(session['user'], pickle.dumps(interfaceUser))

    return render_template("interface.html", card=interfaceUser.overDueDeck[index], form=form)

