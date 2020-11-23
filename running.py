from flask import Flask, render_template, redirect
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
moment = Moment(app)



basedir=os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET KEY']='HardPassword'

db = SQLAlchemy(app)

if __name__ == '__main__':
    from routes import apply_routing

    apply_routing(app).run(debug=True)