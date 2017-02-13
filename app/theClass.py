#import pandas as pd
import csv
from datetime import *
# df  = pd.read_excel('/Users/jacobferragut/gogo/app/templates/gogoKanjiKanji.xlsx',0) 
'''
supermemo 0


        I(1)=1
        I(2)=7
        I(3)=16
        I(4)=35
        for i>4: I(i):=I(i-1)*2
        where I(i) is the interval used after the i-th repetition.

'''
# excelList = list(df.T.itertuples())

R = csv.reader(open('/Users/jacobferragut/gogo/app/templates/gogoKanjiKanji.csv', 'rU'))
cards = [ (unicode(a, 'utf-8'), b, c) for a,b,c in R ]

class User:
    def __init__(self, password):
        self.exampleKnowDeck = [["card face", "card back", datetime(2000,4,19)],
                                    ["card fa", "card Back", datetime(2017,2,4)],
                                     ["card fa", "card Back",datetime(2017,2,20)],
                                    ["card fa", "card Back", datetime(2017,2,25)]]

        self.hashedPassword = password
        self.deck = [ card for card in cards ]
        self.reviewDeck = []
        self.knowDeck = []
        self.newCardsPerDay = 10
        self.dateNow = 0#= datetime.today()
        # each card is structed as a list as shown:
        #                                     [jin,person, (dateDue in terms of datetime.today())]
        # for word in xrange(len(excelList[0])):
        #     # the final zero in this list is the day its due in terms of datetime
        #     self.deck.append([self.col1[word],self.col2[word], 0, 0])
           
    def getDeck(self):
        return self.deck
    
    def setDeck(self,d):
        self.deck = d
    
    def getPassword(self):
        return self.hashedPassword
    
    #basically call when you start your review session
    def syncNow(self):
        self.dateNow = datetime.today()




