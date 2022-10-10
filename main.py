from datetime import date
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 112233445566
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

CORS(app) #enable routes from other parts of the network without blocking the requests

class EventModel(db.Model):
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    event = db.Column(db.String, nullable=False)
    event_info = db.Column(db.String, nullable=False)
    event_link = db.Column(db.String, nullable=True)

    def __repr__(self):
        return ""

#db.create_all() #Run this to create a new db class

event_put_args = reqparse.RequestParser()
event_put_args.add_argument(
    "date", type=str, help="Date of video", required=True)
event_put_args.add_argument(
    "event", type=str, help="Event Type e.g. Motion or Object or Face Detected", required=True)
event_put_args.add_argument(
    "event_info", type=str, help="Info about the event", required=True)
event_put_args.add_argument(
     "event_link", type=str, help="CLoud link to event in storage bucket", required=False)

resource_fields = {
    'id': fields.String,
    'date': fields.String,
    'event': fields.String,
    'event_info': fields.String,
    'event_link': fields.String
}

class Event(Resource):
    @marshal_with(resource_fields)
    def put(self):
        event_id = str(uuid.uuid4())
        args = event_put_args.parse_args()
        print(args)
        print(event_id)
        if args['event_link'] =="":
            args['event_link'] = "No Link"
        thing = EventModel(
            id=event_id, date=args['date'], event=args['event'], event_info=args['event_info'], event_link=args['event_link'])
        db.session.add(thing)
        db.session.commit()
        return 200

class getEvent(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        entry = EventModel.query.filter_by(id=id).first()
        return entry
    
    def delete(self,id):
        EventModel.query.filter_by(id=id).delete()
        db.session.commit()
        return ''

class getEvents(Resource):
    @marshal_with(resource_fields)
    def get(self):
        entries = EventModel.query.all()
        return entries

class DelEvents(Resource):
    def put(self):
        db.session.query(EventModel).delete()
        db.session.commit()

api.add_resource(Event, "/event/")
api.add_resource(getEvent, "/event/<string:id>")
api.add_resource(getEvents, "/events/")
api.add_resource(DelEvents, "/delevents/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
