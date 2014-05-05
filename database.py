from flask import Flask, render_template, request, session
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.debug = True   # need this for autoreload as well as stack trace
app.secret_key = 'luthercollege'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


db = SQLAlchemy(app)
class Users(db.Model):
    '''
	This allows login verification
    '''
    __tablename__= 'user'
    username = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text)

    def __init__(self,username,password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username

class School(db.Model):
	"""
	This holds all the buildings on campus
	"""
	__tablename__ = 'school'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)

class Building(db.Model):
	"""
	This holds all the rooms in a buildings
	"""
	__tablename__ = 'building'
	name = db.Column(db.String(64), primary_key=True)
	open = db.Column(db.Boolean)
	tasks = db.relationship('Room', backref='building', lazy='dynamic')\

	def __repr__(self):
		return '<Project %r>' % self.name

class Room(db.Model):
	"""
	This table represents one building. Each row is a reservation
	"""
	__tablename__ = 'room'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(64), unique=True, index=True)
	arrive = db.Column(db.Date)
	depart = db.Column(db.Date)
	building_id = db.Column(db.String(64), db.ForeignKey('school.name'))

	def __repr__(self):
		return '<Task %r>' % self.description

def init_db():
	db.drop_all()
	db.create_all()
    # user = Users(name='lanejo01',password='asdf')

	school = School(name='Luther')
	building1 = Building(name='Miller')
	building2 = Building(name='Brandt')
	r1 = Room()

	schoolp = Project(name='Luther')
	homep = Project(name='Home')
	prep1 = Task(description='prep for IProg',project=schoolp,done=False)
	prep2 = Task(description='hot tub maintenance',project=homep,done=False)
	prep3 = Task(description='wind the clock',project=homep,done=False)
	prep4 = Task(description='water the rosemary',due=datetime.now(),project=homep,done=False)

	db.session.add_all([schoolp, homep]) #, prep1, prep2, prep3, prep4])
	db.session.commit()

	allproj = Project.query.all()
	for p in allproj:
		print(p.tasks.all())
	
	lproj = Project.query.filter_by(name='Luther').first()
	lproj = Project.query.filter(Project.name=='Luther')
	# filter
	# filter_by
	# limit
	# order_by
	# group_by
	#
	print(str(lproj))

	# query executors
	# all()
	# first()
	# get(id)
	# count()

	#
	# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#common-filter-operators
	#

	# raw sql
	res = db.engine.execute('select * from project')
	for row in res:
		print(row)