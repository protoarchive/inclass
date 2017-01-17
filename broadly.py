"""
Broadly Classroom Analyzer
"""
import requests

from flask import Flask, jsonify

# Creates an application server.
app = Flask(__name__)
app.debug = True

BROADLY_URL = 'http://challenge.broadly.com/classes'

@app.route('/')
def index():
    """
    Just a server check.
    :return: A string.
    """
    return "Broadly is ready."

# ##############
# Routes
# ##############
@app.route('/solution')
def solution():
    """
    Sends a request to BROADLY_URL and returns the solution to the riddle.
    :return: Average number of students per class aged > 24
    """
    lst = get_classes(send_request(BROADLY_URL))
    results = get_average_class_size(lst)
    return jsonify(results)

# ###############
# Handlers
# ##############
def send_request(url):
    """
    Send http requests to a url.
    :param url: Target location
    :return: JSON object with 2 attributes: note (string), classes (list)
    """
    response = requests.get(url)
    return response.json()


def get_classes(data):
    """
    Convert a list of classroom urls to a list of classroom objects.
    :param data: A list of urls
    :return: A list of classes
    """
    app.logger.info("Number of classes: {}".format(len(data['classes'])))
    return [send_request(url) for url in data['classes']]


def get_average_class_size(class_list, total_students=0, total_classes=0):
    """
    Process a list of students from a list of classes.
    :param class_list: a list for class objects
    :param total_students: integer of current student count
    :param total_classes: integer of current class count
    :return: integer, the average number of students.
    """
    for clas in class_list:
        total_students += count_students(clas)
        total_classes += 1
        total_students, total_classes = get_next(clas.get('next'), total_students, total_classes)

    average = total_students / total_classes
    app.logger.info("Total students over 24 in all classes: {0}, total classes: {1}".format(total_students, total_classes))
    print("Total students over 24 in all classes: {0}, total classes: {1}".format(total_students, total_classes))
    return average


def count_students(cls):
    """
    Counts the number of students over 24 in each class.
    :param cls: a class object.
    :return: integer of students aged > 24
    """
    over_24 = [student for student in cls['students'] if student['age'] > 24]
    app.logger.info("Students over 24: {}".format(len(over_24)))
    return len(over_24)


def get_next(url, total_students=0, total_classes=0):
    """
    Loop through classroom links and count students and classes.
    :param url: classroom link
    :param total_students: integer current student count
    :param total_classes: integer current student count
    :return: two-tuple students and classes
    """
    next_class = send_request(url)
    total_students += count_students(next_class)
    total_classes += 1
    app.logger.info("Next total students: {0}, classes: {1}".format(total_students, total_classes))
    if next_class.get('next'):
        total_students, total_classes = get_next(next_class.get('next'), total_students, total_classes)
    app.logger.info("Total next students: {0}, classes: {1}".format(total_students, total_classes))
    return (total_students, total_classes)


if __name__ == '__main__':
    """
    Run the server.
    """
    app.run()
