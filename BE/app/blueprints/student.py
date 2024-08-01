from flask import Blueprint, jsonify

student = Blueprint('student', __name__)

from app.student.query import (
    get_user_password, 
    get_student_courses, 
    get_student_course_assignments, 
    get_student_assignment_questions, 
    get_student_assignment_questions_answers, 
    # put_student_submission, 
    get_upcoming_deadlines,
    put_student_submission_new,
    put_student_create_feedback,
    # get_student_course_stats,
    get_student_course_stats_new
)

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import base64
from datetime import date
import json


@student.route('/courses', methods=['POST'])
@cross_origin()
def user_courses():
    print("******************In user courses*******************")
    userData  = request.json
    print("URequest JSON -------------",userData,"\n")
    username = userData.get('username')

    courses = get_student_courses(username)
    print("Courses returned are:", courses)
    return courses, 200


@student.route('/assignments', methods=['POST'])
@cross_origin()
def course_assignments():
    print("*********************In Assignments**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    courseID = userData.get('courseID')

    assignment_list = get_student_course_assignments(courseID)

    data = {
        "assignment": assignment_list
    }

    print("Assignments returned are:", data)
    return data,200


@student.route('/questions', methods=['POST'])
@cross_origin()
def assignment_questions():
    print("********************In Questions***************************")
    assignmentData  = request.json
    print("Request JSON-------------",assignmentData,"\n")
    assignmentID = assignmentData.get('assignmentID')

    questions_list = get_student_assignment_questions(assignmentID)

    data = {
        "questions": questions_list
    }

    print("Questions returned are:", data)
    return data, 200


# @student.route('/submissions', methods=['POST'])
# @cross_origin()
# def assignment_answers():
#     print("**************************In submissions***********************")
#     pool = create_engine()
#     submissionData  = request.json
#     print("Request JSON---------------",submissionData, "\n")
#     studentID = submissionData.get('studentID')
#     assignmentID = submissionData.get('assignmentID')
#     submittedResponses = submissionData.get('responses')

#     correctResponses = get_student_assignment_questions_answers(assignmentID)
#     print("Correct Response-------------",correctResponses, "\n")

#     count_o = 0
#     count_s = 0

#     for item in correctResponses:
#         if item['type'] == 'O':
#             count_o += 1
#         elif item['type'] == 'S':
#             count_s += 1
#     # You can add additional elif statements to count other types if needed

#     # Print the counts
#     print("Count of type O:", count_o)
#     print("Count of type S:", count_s)

#     # print(correctResponses)
#     correct_answers_dict = {answer["question_id"]: answer["correctAnswer"] for answer in correctResponses}
#     # print(correct_answers_dict)

#     num_correct = 0
#     num_obj = 0
#     subjAnswer = None

#     subjective_exists = False
#     # if len(submittedResponse) == 0:
#         # return jsonify({"message": "Assignment Submitted Successfully"}), 200
#     for response in submittedResponses:
#         question_id = response["questionID"]
#         questionType = response["questionType"]
#         if questionType == 'O':
#             num_obj += 1
#             if question_id in correct_answers_dict and response["response"] == correct_answers_dict[question_id]:
#                 num_correct += 1
        
#         if questionType == "S":
#             subjective_exists = True
#             subjAnswer = response["response"]
    
#     # print(num_correct)
#     # print(num_obj)
#     # print(subjAnswer)
    
#     # print(num_correct)
#     # print(len(submittedResponses))
#     objScore = (num_correct*100/count_o)
#     totalScore = objScore
#     # print("-------------",objScore)

#     put_student_submission(studentID, assignmentID, int(objScore), int(totalScore), subjective_exists, subjAnswer)

#     # print("Questions returned are:", data)
#     return jsonify({"message": "Assignment Submitted Successfully"}), 200


@student.route('/upcoming_deadlines', methods=['POST'])
@cross_origin()
def upcoming_deadlines():
    print("******************In upcoming_deadlines*******************")
    userData  = request.json
    print("URequest JSON -------------",userData,"\n")

    studentID = userData.get('username')

    todayDate = date.today()
    print("Today's date:", todayDate)
    
    upcoming_deadlines = get_upcoming_deadlines(studentID, todayDate)
    data = {
        "deadlines": upcoming_deadlines
    }
    print("Deadlines returned:", data)
    return data, 200


@student.route('/submissions', methods=['POST'])
@cross_origin()
def new_assignment_answers():
    print("**************************In new_submissions***********************")
    submissionData  = request.json
    print("Request JSON---------------",submissionData, "\n")
    studentID = submissionData.get('studentID')
    assignmentID = submissionData.get('assignmentID')
    submittedResponses = submissionData.get('responses')


    subjectiveExists = False
    subjAnswer = None
    objAnswers={}
    

    for response in submittedResponses:
        print("Response:",response)
        if response is not None:
            question_id = response["questionID"]
            questionType = response["questionType"]

            if questionType == 'O':
                objAnswers[question_id] = response["response"]

            if questionType == "S":
                subjectiveExists = True
                subjAnswer = response["response"]
        else:
            print("The response got is null")

    message = put_student_submission_new(studentID, assignmentID, subjectiveExists, subjAnswer, objAnswers)

    return jsonify({"message": message}), 200


@student.route('/submit_feedback', methods=['POST'])
@cross_origin()
def submit_feedback():
    print("*********************In Student Submit Feedback**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    studentID = userData.get('studentID')
    assignmentID = userData.get('assignmentID')
    feedbackText = userData.get('feedbackText')

    put_student_create_feedback(studentID, assignmentID, feedbackText)

    return "Feedback submitted Successfully", 200


@student.route('/student_course_stats', methods=['POST'])
@cross_origin()
def course_stats():
    print("*********************In Student Course Stats**********************")
    userData  = request.json
    print("Request JSON-------------",userData,"\n")
    courseID = userData.get('courseID')
    studentID = userData.get('studentID')

    stats = get_student_course_stats_new(courseID, studentID)
    print("############Stats", stats)
    data = {
        "stats":stats
    }

    return data, 200


# @student.route('/student_course_stats_new', methods=['POST'])
# @cross_origin()
# def course_stats_new():
#     print("*********************In Student Course Stats New**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     courseID = userData.get('courseID')
#     studentID = userData.get('studentID')

#     stats = get_student_course_stats_new(courseID, studentID)
#     print("############Stats", stats)
#     data = {
#         "stats":stats
#     }

#     return data, 200