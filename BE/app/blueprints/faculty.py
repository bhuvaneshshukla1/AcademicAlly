from flask import Blueprint, jsonify

faculty = Blueprint('faculty', __name__)

from app.faculty.query import (
    get_faculty_courses,
    get_faculty_course_assignments,
    get_faculty_submissions,
    get_faculty_single_submissions,
    put_faculty_submission_grades,
    put_faculty_create_assignment,
    get_faculty_combine_feedback,
    get_faculty_assignment_stats,
    get_faculty_weak_students
)

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import date
import json

@faculty.route('/faculty_courses', methods=['POST'])
@cross_origin()
def faculty_courses():
    print("******************In Faculty courses*******************")
    userData  = request.json
    print("URequest JSON -------------",userData,"\n")
    username = userData.get('username')

    courses = get_faculty_courses(username)
    print("Courses returned are:", courses)
    return courses, 200


@faculty.route('/faculty_assignments', methods=['POST'])
@cross_origin()
def faculty_assignments():
    print("*********************In Faculty Assignments**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    courseID = userData.get('courseID')

    assignment_list = get_faculty_course_assignments(courseID)
    weak_student_list = get_faculty_weak_students(courseID)

    data = {
        "assignments": assignment_list,
        "weakStudents": weak_student_list
    }

    print("Assignments returned are:", data)
    return data,200


@faculty.route('/get_submissions', methods=['POST'])
@cross_origin()
def get_submissions():
    print("*********************In Faculty Submissions**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    assignmentID = userData.get('assignmentID')

    submission_list = get_faculty_submissions(assignmentID)

    data = {
        "submissions": submission_list
    }

    print("Submissions returned are:", data)
    return data,200


@faculty.route('/get_subj_responses', methods=['POST'])
@cross_origin()
def get_subj_responses():
    print("*********************In Faculty get subj response**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    submissionID = userData.get('submissionID')
    assignmentID = userData.get('assignmentID')

    subj_responses = get_faculty_single_submissions(submissionID, assignmentID)

    data = {
        "responses": subj_responses
    }

    print("Submissions returned are:", data)
    return data,200


@faculty.route('/post_grades', methods=['POST'])
@cross_origin()
def post_grades():
    print("*********************In Faculty post grades**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    submissionID = userData.get('submissionID')
    list_of_grades = userData.get('grades')

    marks = list_of_grades[0]['marks']
    print("Marks:",marks)

    put_faculty_submission_grades(submissionID, marks)

    return "Grades Posted Successfully",200


@faculty.route('/create_assignment', methods=['POST'])
@cross_origin()
def create_assignment():
    print("*********************In Faculty create assignment**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    courseID = userData.get('courseID')
    deadline = userData.get('deadline')
    list_of_questions = userData.get('questions')

    print("Questions:",list_of_questions)

    assignment_id = put_faculty_create_assignment(courseID, deadline, list_of_questions)

    return jsonify({"message": "Assignment Created Successfully", "AssignmentID":assignment_id}), 200


@faculty.route('/combine_feedback', methods=['POST'])
@cross_origin()
def combine_feedback():
    print("*********************In Faculty Combine Feedback**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    assignmentID = userData.get('assignmentID')

    combined_feedback = get_faculty_combine_feedback(assignmentID)

    data = {
        "aggregated_feedback":combined_feedback
    }

    return data, 200


@faculty.route('/course_stats', methods=['POST'])
@cross_origin()
def course_stats():
    print("*********************In Faculty Course Stats**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    courseID = userData.get('courseID')
    facultyID = userData.get('facultyID')

    course_stats = get_faculty_assignment_stats(courseID, facultyID)

    data = {
        "course_stats":course_stats
    }

    return data, 200


@faculty.route('/weak_students', methods=['POST'])
@cross_origin()
def weak_students():
    print("*********************In Faculty Weak Students**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    courseID = userData.get('courseID')

    weak_students = get_faculty_weak_students(courseID)

    data = {
        "weak_students":weak_students
    }

    return data, 200

