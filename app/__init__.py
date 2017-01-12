from flask import Flask

app = Flask(__name__)
app.secret_key = 'dontguessme584829038572'

from app import views


#if __name__ == '__main__':
