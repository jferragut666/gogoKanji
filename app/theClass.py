#import pandas as pd
# -*- coding: utf-8 -*-
import csv
from datetime import *
import time
from app import app
from flask import render_template, session, redirect, url_for
from wtforms.validators import InputRequired, NumberRange, Length

from wtforms import StringField, IntegerField, SelectMultipleField, \
    RadioField, TextAreaField, PasswordField, SubmitField

import wtforms, flask_wtf, redis, hashlib, pickle



#example of a card: [u'\u9762\u767d\u3044', 'to help', 'datetimeHere', 0,                          u'\u9732\u727d\u3424']
#----------------  card face ------------- card back -- due date --- number of days til review -- furigana(hiragana above kanji) 
class User(object):
    def __init__(self, password):

        self.deck = []#deck where you grab new cards
        R = csv.reader(open('/Users/jacobferragut/gogo/app/templates/gogoKanjiKanji.csv', 'rU'))
        cards = [ (unicode(a, 'utf-8'), b, c, unicode(d, 'utf-8')) for a,b,c,d in R ]
        for i in cards:
            temp = list(i)
            temp.append("")
            temp[2] = date.today()
            temp[3] = -1
            temp[4] = i[3]
            self.deck.append(temp)
        print self.deck
        self.hashedPassword = password
        self.overDueDeck = [] 
        self.overDueIndex = 0
        self.done = []
        
        self.newCardsPerDay = 5
        self.dateNow = date.today()
        self.tomorrow = date.today() + timedelta(days=+1) 
        self.index = 0
          
    
        
    def updateDateNow(self):
        self.dateNow = date.today()

    def getOverDueDeck(self):
        swapIndex = 0
        temp = 0
        return self.overDueDeck
       


        
    def appendNewCards(self, form): #["wowow", "wowow"]
        if self.tomorrow <= self.dateNow or len(self.overDueDeck) == 0:
            print "tomorrow is now or in the past or odeck length is 0"
            for i in xrange(self.newCardsPerDay):
                if len(self.deck) != 0:
                    self.overDueDeck.append(self.deck.pop())
            self.tomorrow = self.dateNow + timedelta(days=+1)
            return render_template('login.html', form=form)
        else:
            print "damn!"

        
    
    def supermemo(self, card):
        if card[3] == -1:
            card[3] = 0
        elif card[3]==0:
            card[2] = self.dateNow + timedelta(days=+1) 
            card[3] = 1
        elif card[3]==1:
            card[2] = self.dateNow + timedelta(days=+7)
            card[3] = 7
        elif card[3] == 7:
            card[2] = self.dateNow + timedelta(days=+16)
            card[3] = 16
        elif card[3] == 16:
            card[2] = self.dateNow + timedelta(days=+35)
            card[3] = 35
        elif card[3] >= 35:
            card[2] = self.dateNow + timedelta(days=+card[3]*2)
            card[3] += card[3]*2
        return card
        
    ''' 
    One programming challenge that I had was trying to check to see if the user needed more daily cards 
    Another programming problem was making sure that a card is due on a certain day.
    
    fix cycling questions ( if get wrong it finishes)
    fix words in index cards 
    ''' 
