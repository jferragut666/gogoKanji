# -*- coding: utf-8 -*-
from app import app
from flask import render_template, session, redirect, url_for
from wtforms.validators import InputRequired, NumberRange, Length

from wtforms import StringField, IntegerField, SelectMultipleField, \
    RadioField, TextAreaField, PasswordField, SubmitField

from theClass import User
from datetime import *
import wtforms, flask_wtf, redis, hashlib, pickle, time


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
                if len(user_object.getOverDueDeck()) == 0:
                    for i in xrange(user_object.newCardsPerDay):
                        if len(user_object.deck) != 0:
                            user_object.overDueDeck.append(user_object.deck.pop())
                            numOfDueCards+=1
                else:
                    for i in xrange(len(user_object.getOverDueDeck())):
                        if user_object.getOverDueDeck()[i][2] <= user_object.dateNow:
                            numOfDueCards+=1

                user_object.done = [False]*numOfDueCards

                if False not in user_object.done:
                    user_object.index = 0
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
    print "updatedatenow in index(): ", interfaceUser.dateNow
    print "tomorrow in index pre updatenewcards: ", interfaceUser.tomorrow
    #interfaceUser.appendNewCards()
    if interfaceUser.tomorrow <= interfaceUser.dateNow:
        print "tomorrow is now or in the past"
        for i in xrange(interfaceUser.newCardsPerDay):
            if len(interfaceUser.deck) != 0:
                interfaceUser.overDueDeck.append(interfaceUser.deck.pop())
        interfaceUser.tomorrow = interfaceUser.dateNow + timedelta(days=+1)
        print "tomorrow post update: ", interfaceUser.tomorrow

        Red.set(session['user'], pickle.dumps(interfaceUser))
        return render_template('login.html', form=LoginForm())
    else:
        print "damn!"
    #interfaceUser.updateTomorrowDate() 
    index = interfaceUser.index 
    if form.validate_on_submit():
        if form.answerBox.data == interfaceUser.overDueDeck[index][1]:
            print "correct"

            if interfaceUser.overDueDeck[index][3] != -1:
                interfaceUser.done[index] = True
                print interfaceUser.overDueDeck[index][3], " not equal to -1" 
            print "interfaceUser.overDueDeck[",index,"] has been updated"
            interfaceUser.overDueDeck[index] = interfaceUser.supermemo(interfaceUser.overDueDeck[index])

            if index + 1 < len(interfaceUser.overDueDeck):
                #print index + 1, " < len(interfaceUser.overDueDeck)"
                for i in xrange(index+1,len(interfaceUser.overDueDeck)):
                    if interfaceUser.done[i] == False:
                        interfaceUser.index = i
                        print "index is now: ", interfaceUser.index 
                        break
                    elif i == len(interfaceUser.overDueDeck) -1:
                        print "i == len(interfaceUser.overDueDeck) -1"
                        if False in interfaceUser.done:
                            print "false in done and index = first false"
                            interfaceUser.index = interfaceUser.done.index(False)
                        else:
                            return "done"

            elif False in interfaceUser.done: 
                interfaceUser.index = interfaceUser.done.index(False)
                print "index + 1 >= len(interfaceUser.overdueDeck) and index = first false at ", interfaceUser.index
            else:
                #flash("done for today")
                interfaceUser.index = 0
                return "done for today"

        print interfaceUser.done
        print interfaceUser.overDueDeck
    else:
        print "invalid form"

    Red.set(session['user'], pickle.dumps(interfaceUser))

    return render_template("interface.html", card=interfaceUser.overDueDeck[interfaceUser.index][0], form=form)

