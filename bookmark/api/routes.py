#BOOKMARK API using Flask_RESTful and Blueprint
from flask import Flask,jsonify,request,json,Response,Blueprint,make_response,abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort, Api, Resource
import json

app = Flask(__name__)
#Initialize Blueprint
bookmarks = Blueprint('api',__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite://///home/sumaiya/Bookmark_Example/bookmarksdata.db'


api_obj = Api(bookmarks)

db = SQLAlchemy(app)


#Bookmark Model 
class btable(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String)
    
    def __init__(self, name, url):
        self.name = name
        self.url = url

# shows,post,put,remove a single Bookmark item
class Bookmark(Resource):   
    def get(self, id):
        one_marks = btable.query.filter_by(id=int(id)).first()
        if one_marks:
            return make_response(jsonify({"Requested Bookmark name:" : one_marks.name,"Requested Bookmark url:" : one_marks.url}))
        return abort(404,message="BOOKMARK NOT FOUND!!!")
        
      
    def post(self):
        if(request.method == 'POST'):
            bt = btable(request.json['name'],request.json['url'])
            db.session.add(bt)
            db.session.commit()
            return make_response(jsonify({"Added Bookmark Name:" : request.json['name'] ,"AddedBookmark URL:" : request.json['url']}),201)

    def put(self, id):
        one_marks = btable.query.filter_by(id=int(id)).first()
        if one_marks:
            one_marks.name = request.json['name']
            one_marks.url = request.json['url']
            bt = btable(one_marks.name,one_marks.url)
            db.session.add(bt)
            db.session.commit()
            return make_response(jsonify({"Updated Bookmark name:" : one_marks.name,"Updated Bookmark url:" : one_marks.url}))
        return abort(404,message="BOOKMARK NOT FOUND!!!")

    def delete(self, id):
        one_marks = btable.query.filter_by(id=int(id)).first()
        if one_marks:
            db.session.delete(one_marks)
            db.session.commit()
            return make_response(jsonify({"Deleted Bookmark name:" : one_marks.name}))
        return abort(404,message="BOOKMARK NOT FOUND!!!")
        

# shows,post,put,remove a single Bookmark item
class BookmarkAll(Resource):  
    def get(self):
        all_marks = btable.query.all()
        if all_marks:
            bt = []
            marks = []
            for i in all_marks:
                all_marks_dict ={
                    'name':i.name,
                    'url': i.url
                }
                marks.append(all_marks_dict)
            return make_response(json.dumps(marks),201)
        return abort(404,message="NO BOOKMARKS AVAILABLE!!!")


## Actually setup the Api resource routing here
api_obj.add_resource(Bookmark,'/bookmarks','/bookmarks/<int:id>') 
api_obj.add_resource(BookmarkAll,'/bookmarksAll') 



