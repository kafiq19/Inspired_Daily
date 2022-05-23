import flask
from flask_mail import Mail, Message

app = flask.Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'khalfeen1@gmail.com'
app.config['MAIL_PASSWORD'] = 'jvofajjseaajkszt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
  msg = Message('Hello from the other side!', sender =   'khal@mailtrap.io', recipients = ['tha_realist1990@hotmail.com'])
  msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
  mail.send(msg)
  return "Message sent!"

if __name__ == '__main__':
   app.run(debug = True)


# def notification():
#     #creates a notification email


#     print("Successfully sent notification email")

# if __name__ == "__main__":
#     notification()