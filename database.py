from flask import Flask, render_template, request, session
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
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


class Building(db.Model):
	"""
	This holds all the rooms in a buildings
	"""
	__tablename__ = 'building'
	name = db.Column(db.String(64), primary_key=True)
	rooms = db.relationship('Room', backref='building', lazy='dynamic')

	def __repr__(self):
		return '<Building %r>' % self.name

class Room(db.Model):
	"""
	This table represents one building. Each row is a reservation
	"""
	__tablename__ = 'room'
	id = db.Column(db.Integer(), primary_key = True)
	number = db.Column(db.Integer(), index=True)
	building_id = db.Column(db.String(64), db.ForeignKey('building.name'))
	reservations = db.relationship('Reservation', backref='room', lazy='dynamic')
	def __repr__(self):
		return '<Room %r>' % self.description

class Reservation(db.Model):
	'''
	Many to many solution (room - client)
	'''
	__tablename__ = 'reservation'
	arrive = db.Column(db.Date, primary_key = True)
	depart = db.Column(db.Date, primary_key = True)	
	clientId = db.Column(db.Integer(), db.ForeignKey('Client.id'))
	roomId = db.Column(db.Integer(), db.ForeignKey('Room.id'))
	def __repr__(self):
		return '<Reservation %r>' % self.description


class Client(db.Model):
	'''
	holds client info
	'''
	__tablename__= 'client'
	name = db.Column(db.String(64), index=True)
	id = db.Column(db.Integer(), primary_key=True)
	reservations = db.relationship('Reservation', backref='client', lazy='dynamic')

	def __repr__(self):
		return '<Client %r>' % self.description

def init_db():
	db.drop_all()
	db.create_all()
    # user = Users(name='lanejo01',password='asdf')


	miller = Building(name='Miller')
	brandt = Building(name='Brandt')
	
	isaac = Client(id = 1, name = "Isaac Davis")
	joe = Client(id = 2, name = "Joe Lane")
	
	r1 = Room(number = 1, building_id = miller)
	r2 = Room(number = 2, building_id = miller)
	r3 = Room(number = 1, building_id = brandt)

	res1 = Reservation(arrive = datetime.date(2012, 1, 2), depart = datetime.date(2012, 1, 3), clientID = isaac, roomId = r1)
	res2 = Reservation(arrive = datetime.date(2012, 1, 5), depart = datetime.date(2012, 1, 7), clientID = joe, roomId = r1)


	db.session.add_all([miller, brandt, isaac, joe, r1, r2, r3, res1, res2])
	db.session.commit()


	#allproj = Project.query.all()
	#for p in allproj:
#		print(p.tasks.all())
	
#	lproj = Project.query.filter_by(name='Luther').first()
#	lproj = Project.query.filter(Project.name=='Luther')
	# filter
	# filter_by
	# limit
	# order_by
	# group_by
	#
	#print(str(lproj))

	# query executors
	# all()
	# first()
	# get(id)
	# count()

	#
	# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#common-filter-operators
	#

	# raw sql
	res = db.engine.execute('select * from building')
	for row in res:
		print(row)
