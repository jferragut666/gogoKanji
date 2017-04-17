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


# df  = pd.read_excel('/Users/jacobferragut/gogo/app/templates/gogoKanjiKanji.xlsx',0) 
# excelList = list(df.T.itertuples())
#eshell is the best 

#example of a card: [u'\u9762\u767d\u3044', 'to help', 'datetimeHere', 0]
#---------------------  card face --------  card back -- due date ---- number of times correct 
class User(object):
    def __init__(self, password):
        print "かばん"
        print u'\u9762\u767d\u3044'
        '''
        self.exampleOverDueDeck = [[u"かばん", "bag", datetime(2000,4,19), -1],
                                    [u"大抵", "usually", datetime(2017,2,4), -1],
                                     [u"上", "above",datetime(2017,2,25), -1],
                                    [u"犬", "dog", datetime(2017,5,25), -1]]
        '''
        
        self.deck = []#deck where you grab new cards
        R = csv.reader(open('/Users/jacobferragut/gogo/app/templates/gogoKanjiKanji.csv', 'rU'))
        cards = [ (unicode(a, 'utf-8'), b, c) for a,b,c in R ]
        for i in cards:
            temp = list(i)
            temp[2] = date.today()
            temp.append(-1)
            self.deck.append(temp)

        self.hashedPassword = password
        #self.reviewDeck = [] #deck of things you got incorrect 5
        self.overDueDeck = [] #deck of things that you probably know 43
        self.overDueIndex = 0
        self.done = []
        
        self.newCardsPerDay = 2
        #self.dateNow = datetime.today()
        self.dateNow = date.today()
        self.tomorrow = date.today() + timedelta(days=+1) 
        self.yesterday = date.today() + timedelta(days=-1)
        self.index = 0
        # each card is structed as a list as shown:
        #                                     [jin,person, (dateDue in terms of datetime.today())]
        # for word in xrange(len(excelList[0])):
        #     # the final zero in this list is the day its due in terms of datetime
        #     self.deck.append([self.col1[word],self.col2[word], 0, 0])
           
    
        
    #basically call when you start your review session
    def updateDateNow(self):
        self.dateNow = date.today()

    def getOverDueDeck(self):
        swapIndex = 0
        temp = 0
        '''
        for i in xrange(len(self.overDueDeck)):
            if self.overDueDeck[i][2] <= self.dateNow:
               temp = self.overDueDeck[i]
               self.overDueDeck[i] = self.overDueDeck[swapIndex]
               self.overDueDeck[swapIndex] = temp
               swapIndex += 1
        '''
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

        
    # def REVIEW(self, form):
    #     #over due deck = [ "face", "back", datetime(2000, 4, 19), -1]
    #     for i in self.overDueDeck:
    #         print "due date: ",i[2], " date now: ", self.dateNow
    #         if i[2] <= self.dateNow:
    #             return i
                #temp = raw_input("enter answer: ")
                # if temp == i[1]:
                #     self.supermemo(i) NOTES: review one card at a time
                #     print "correct"   make overDueDeck[0] equal next index for card to grab
                # else:
                #     if i[3] != -1:
                #         i[3] = 0
                #     else:
                #         i[3] = -1
                # print "due date: ",i[2], " date now: ", self.dateNow
                

#    def updateTomorrowDate(self):
#        if self.tomorrow <= self.dateNow: # if tomorrow is now or in the past then update tomorrow
#            self.tomorrow = self.dateNow + timedelta(days=+1)
#program wont work because the update to tomorrow is before appendnewcards goes off. Therefore, appendnewCards will never append new cards even though the len of done is the correct length.        
#(it might work now because I made it so that updatetomorrowdate is after appendNewCards)
    def supermemo(self, card):
        print "inputted card[3] value: ", card[3]
        if card[3] == -1:
            card[3] = 0
            print "card is now: ", card[3], " ", card[2]
        elif card[3]==0:
            card[2] = self.dateNow + timedelta(days=+1) 
            card[3] = 1
            print card[2], " time delta applied"

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
    supermemo 0


            I(1)=1
            I(2)=7
            I(3)=16
            I(4)=35
            for i>4: I(i):=I(i-1)*2
            where I(i) is the interval used after the i-th repetition.
    '''

    ''' 
    One programming challenge that I had was trying to check to see if the user needed more daily cards 
    Another programming problem was making sure that a card is due on a certain day.
    
    fix cycling questions ( if get wrong it finishes)
    fix words in index cards 
    ''' 

    

    












