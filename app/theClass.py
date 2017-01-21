import pandas as pd
df  = pd.read_excel('/Users/jacobferragut/gogo/app/templates/gogoKanjiKanji.xlsx',0) 
excelList = list(df.T.itertuples())


class user:
    def __init__(self, password):
        self.hashedPassword = password
        self.deck = []
        self.col1 = excelList[0]
        self.col2 = excelList[1]
        for word in xrange(len(excelList[0])):
           self.deck.append([self.col1[word],self.col2[word], 0])
    def getDeck(self):
        return self.deck
    def setDeck(self,d):
        self.deck = d
    
    def getPassword(self):
        return self.hashedPassword




