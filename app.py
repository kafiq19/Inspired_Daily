import os
import random
from datetime import date

import flask


from flask import Flask #del
from flask_mail import Mail, Message #del
from mailjet_rest import Client #del

from flask import request
from flask import Flask, render_template
from jinja2 import Template
import pandas as pd
import psycopg2

csv_data = pd.read_csv('quotes.csv', names=['author', 'quote','ka', 'sch','tags'], dtype={'quote': str})
#csv_data['sch'] = pd.to_datetime(csv_data['sch'], format='%m/%d/%Y')
#csv_data['sch'] = csv_data['sch'].dt.date

# dataBASE_URL = os.environ['csv_dataBASE_URL']
# conn = psycopg2.connect(csv_dataBASE_URL, sslmode='require')

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    msg = csv_data.loc[random.randint(0,len(csv_data.index))]
    quote = msg.quote
    author = msg.author
    # msg = msg.to_json()

    return render_template('home.html', quote=quote , author=author)
    #return Template('home.html').render(something="World")
    
    # return "<h1>Daily Inspired</h1> \
    # <p>A curated selection of quotes to inspire your day. -KA</p>"

@app.route('/api/random', methods=['GET'])
def api_random():
    
    try:
        msg = csv_data.loc[random.randint(0,len(csv_data.index))]
    
    except Exception as e:
        return{e}
    
    return msg.to_json(orient='records', force_ascii=False)

@app.route('/api/qotd', methods=['GET'])
def api_qotd():
    
    try:
        today = date.today()
        today = today.strftime("%m/%d/%y")
        msg = csv_data.loc[csv_data['sch'] == today]
        del msg['sch']
    
    except Exception as e:
        return{e}
    
    return msg.to_json(orient='records', force_ascii=False)

@app.route('/api/ka', methods=['GET'])
def api_ka():
    
    try:
        msg = csv_data.loc[csv_data['ka'] > 0]
        msg = msg.sample()
        del msg['sch']
        print(msg)
    
    except Exception as e:
        return{e}
    
    return msg.to_json(orient='records', force_ascii=False)

#--
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'khalfeen1@gmail.com'
# app.config['MAIL_PASSWORD'] = 'B@l@nc3G2021'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

app.config['MAIL_SERVER']='smtp.elasticemail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'khalfeen1@gmail.com'
app.config['MAIL_PASSWORD'] = '84A0AA97343F8A38D2CA935E7F8BCFCF952A'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/email', methods=['GET'])
def index():
    msg = Message('Hello from the other side!', sender =   'khalfeen1@gmail.com', recipients = ['tha_realist1990@hotmail.com'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    mail.send(msg)
    return "Message sent!"


if __name__ == '__main__':
    app.run(debug = True)

#> set FLASK_ENV=development
#> flask run





''' CSV
author, quote, type[joke, quote], KA[0,1],  

'''

    # return csv_data.loc[random.randint(0,len(csv_data.index))] 

    # quote = request.args['random']
    # try:
    #     return csv_data.loc[random.randint(0,len(csv_data.index))]
    # except KeyError:
    #     return f'Invalid input ({csv_data.index.min()} - {csv_data.index.max()})'

'''api.py:
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()

python api.py '''