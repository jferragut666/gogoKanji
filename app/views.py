from app import app
from flask import render_template
import wtforms
import flask_wtf
#from run import parser
@app.template_filter()
def newLine(d):
  lst = [] 
  for i in d:
    lst.append(i+"\n")
  return lst
@app.route('/', methods=['post','get'])
def main():
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

    
