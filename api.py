from flask import Flask, jsonify, request
from bson.json_util import dumps
import pymongo
from pymongo import MongoClient

#connects to the server 
client = MongoClient()
app = Flask(__name__)
#the database we want from the mongodb
db = client.notesatcu
#the collection we want from the database
courses = db.courses

#returns all courses (not very useful)


@app.route('/courses/<semester>', methods=['GET'])
def get_courses_by_semester(semester):
	if request.method == 'GET':
		all_courses = courses.find({"Term": semester})
		return dumps(all_courses)


@app.route('/professors/<semester>/<call_number>', methods=['GET'])
def get_professors_by_semester(semester, first_name):
	if request.method == 'GET':
		all_courses = courses.find({"Term": semester, "Instructor1Name": first_name})
		return dumps(all_courses)

@app.route('/professors/<full_name>/', methods=['GET'])
def get_courses_by_professor(full_name):
    if request.method == 'GET':
        all_courses = courses.find({"Instructor1Name": full_name})
        return dumps(all_courses)

@app.route('/professors/<semester>/<day>', methods=['GET'])
def get_courses_on_days(semester, day):
    if request.method == 'GET':
        all_courses = courses.find({"$or":[{ "Term": semester, "Meets1": day}, {"Term": semester, "Meets2": day}]})
        return dumps(all_courses)

@app.route('/courses/<semester>/<max>', methods=['GET'])
def get_courses_smaller_than(semester, max):
    if request.method == 'GET':
        query = []
        nums = digits_smaller_than_query(int(max), semester)
        all_courses = courses.find( {"$or": nums } )
        return dumps(all_courses)

#helper method to get all digits less than a certain, as strings
def digits_smaller_than_query(num, semester):
    queries = []
    if(num <= 0):
        return queries
    for i in range(0, num + 1):
        query = {"Term": semester, "MaxSize": str(i)}
        queries.append(query)
    return queries






if __name__ == '__main__':
    app.run(debug=True, port=5024)
