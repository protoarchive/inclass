import json
import requests

from flask import Flask, jsonify


app = Flask(__name__)
app.debug = True

broadly = 'http://challenge.broadly.com/classes'

@app.route('/')
def index():
    return "Broadly is ready."

@app.route('/solution')
def solution():
    lst = get_classes(send_request(broadly))
    results = get_students(lst)
    return jsonify(results)


# Handlers
def send_request(url):
    response = requests.get(url)
    return response.json()


def get_classes(data):
    app.logger.info("Number of classes: {}".format(len(data['classes'])))
    return [send_request(url) for url in data['classes']]


def get_students(class_list, total_students=0, total_classes=0):
    for clas in class_list:
        total_students += count_students(clas)
        total_classes += 1
        total_students, total_classes = get_next(clas.get('next'), total_students, total_classes)

    average = total_students / total_classes
    app.logger.info("Total students over 24 in all classes: {0}, total classes: {1}".format(total_students, total_classes))
    print("Total students over 24 in all classes: {0}, total classes: {1}".format(total_students, total_classes))
    return average


def count_students(cls):
    over_24 = [student for student in cls['students'] if student['age'] > 24]
    app.logger.info("Students over 24: {}".format(len(over_24)))
    return len(over_24)


def get_next(url, total_students=0, total_classes=0):
    next_class = send_request(url)
    total_students += count_students(next_class)
    total_classes += 1
    app.logger.info("Next total students: {0}, classes: {1}".format(total_students, total_classes))
    if next_class.get('next'):
        total_students, total_classes = get_next(next_class.get('next'), total_students, total_classes)
    app.logger.info("Total next students: {0}, classes: {1}".format(total_students, total_classes))
    return (total_students, total_classes)


if __name__ == '__main__':
    app.run()
