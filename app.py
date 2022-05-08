import flask
from flask import request
from flask import Flask, render_template
from jinja2 import Template
import pandas as pd
import random
import os
import psycopg2

data = pd.read_csv('quotes.csv', names=['author', 'quote'])

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    msg = data.loc[random.randint(0,len(data.index))]
    quote = msg.quote
    author = msg.author
    # msg = msg.to_json()

    return render_template('home.html', quote=quote , author=author,)
    #return Template('home.html').render(something="World")
    
    # return "<h1>Daily Inspired</h1> \
    # <p>A curated selection of quotes to inspire your day. -KA</p>"

@app.route('/random', methods=['GET'])
def api_random():
    try:
        msg = data.loc[random.randint(0,len(data.index))]
    except Exception as e:
        return{e}
    return msg.to_json()


if __name__ == '__main__':
    app.run(debug = True)

''' CSV
author, quote, type[joke, quote], KA[0,1],  

'''

    # return data.loc[random.randint(0,len(data.index))] 

    # quote = request.args['random']
    # try:
    #     return data.loc[random.randint(0,len(data.index))]
    # except KeyError:
    #     return f'Invalid input ({data.index.min()} - {data.index.max()})'

'''api.py:
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()

python api.py '''