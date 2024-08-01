from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from app.student.query import (
    get_user_password
)
# from app.student.query import (
#     get_user_password, 
#     get_student_courses, 
#     get_student_course_assignments, 
#     get_student_assignment_questions, 
#     get_student_assignment_questions_answers, 
#     get_upcoming_deadlines,
#     put_student_submission_new,
#     put_student_create_feedback
# )
# from app.faculty.query import (
#     get_faculty_courses,
#     get_faculty_course_assignments,
#     get_faculty_submissions,
#     get_faculty_single_submissions,
#     put_faculty_submission_grades,
#     put_faculty_create_assignment,
#     get_faculty_combine_feedback,
#     get_faculty_assignment_stats,
#     get_faculty_weak_students
# )

from app.blueprints.faculty import faculty
from app.blueprints.student import student

import json
import base64
from datetime import date

app = Flask(__name__)
cors = CORS(app, supports_credentials=False, origins=["http://localhost:3000"])
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(student)
app.register_blueprint(faculty)


@app.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    # Login logic here
    print("****************In Login_user****************")
    userData  = request.json
    print("Request JSON -------------",userData)
    username = userData.get('username')
    password = userData.get('password')

    actual_password, userType = get_user_password(username)
    print("Actual password is", actual_password, "\n")
    
    # password_base64 = base64.b64encode(bytes(password, 'utf-8'))
    password_base64 = base64.b64encode((password.encode('utf-8'))).decode()
    # password_base64 = base64.b64encode(password)
    print("Given password is", password_base64)

    # password = xyz
    # passwordbase64 = b'xyz'

    if actual_password == password_base64:
    # if True:
        return jsonify({"message": "Login successful", "UserType":userType}), 200
    else:
        print("Unsuccessful login")
        return jsonify({"message": "Login unsuccessful"}), 401


# @app.route('/courses', methods=['POST'])
# @cross_origin()
# def user_courses():
#     # Login logic here
#     print("******************In user courses*******************")
#     userData  = request.json
#     print("URequest JSON -------------",userData,"\n")
#     username = userData.get('username')

#     courses = get_student_courses(username)
#     print("Courses returned are:", courses)
#     return courses, 200


# @app.route('/assignments', methods=['POST'])
# @cross_origin()
# def course_assignments():
#     # Login logic here
#     print("*********************In Assignments**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     courseID = userData.get('courseID')

#     assignment_list = get_student_course_assignments(courseID)

#     data = {
#         "assignment": assignment_list
#     }

#     print("Assignments returned are:", data)
#     return data,200


# @app.route('/questions', methods=['POST'])
# @cross_origin()
# def assignment_questions():
#     print("********************In Questions***************************")
#     assignmentData  = request.json
#     print("Request JSON-------------",assignmentData,"\n")
#     assignmentID = assignmentData.get('assignmentID')

#     questions_list = get_student_assignment_questions(assignmentID)

#     data = {
#         "questions": questions_list
#     }

#     print("Questions returned are:", data)
#     return data, 200


# @app.route('/submissions', methods=['POST'])
# @cross_origin()
# def assignment_answers():
#     print("**************************In submissions***********************")
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



# # @app.route('/feedback', methods=['POST'])
# # @cross_origin()
# # def feed_back():
# #     # Login logic here
# #     print("******************In feedback*******************")
# #     userData  = request.json
# #     print("URequest JSON -------------",userData,"\n")
# #     text = userData.get('text')

# #     feedbackResponse = get_gpt_feedback(text)
# #     print("Gemini Feedback returned:", feedbackResponse)
# #     return feedbackResponse, 200



# @app.route('/upcoming_deadlines', methods=['POST'])
# @cross_origin()
# def upcoming_deadlines():
#     # Login logic here
#     print("******************In upcoming_deadlines*******************")
#     userData  = request.json
#     print("URequest JSON -------------",userData,"\n")

#     studentID = userData.get('username')

#     todayDate = date.today()
#     print("Today's date:", todayDate)
    
#     upcoming_deadlines = get_upcoming_deadlines(studentID, todayDate)
#     data = {
#         "deadlines": upcoming_deadlines
#     }
#     print("Deadlines returned:", data)
#     return data, 200


# @app.route('/new_submissions', methods=['POST'])
# @cross_origin()
# def new_assignment_answers():
#     print("**************************In new_submissions***********************")
#     submissionData  = request.json
#     print("Request JSON---------------",submissionData, "\n")
#     studentID = submissionData.get('studentID')
#     assignmentID = submissionData.get('assignmentID')
#     submittedResponses = submissionData.get('responses')


#     subjectiveExists = False
#     subjAnswer = None
#     objAnswers={}

#     for response in submittedResponses:
#         question_id = response["questionID"]
#         questionType = response["questionType"]

#         if questionType == 'O':
#             objAnswers[question_id] = response["response"]

#         if questionType == "S":
#             subjectiveExists = True
#             subjAnswer = response["response"]

#     message = put_student_submission_new(studentID, assignmentID, subjectiveExists, subjAnswer, objAnswers)


#     return jsonify({"message": message}), 200



# #-------------------------------------------------------------------------------------------------------------


# @app.route('/faculty_courses', methods=['POST'])
# @cross_origin()
# def faculty_courses():
#     print("******************In Faculty courses*******************")
#     userData  = request.json
#     print("URequest JSON -------------",userData,"\n")
#     username = userData.get('username')

#     courses = get_faculty_courses(username)
#     print("Courses returned are:", courses)
#     return courses, 200


# @app.route('/faculty_assignments', methods=['POST'])
# @cross_origin()
# def faculty_assignments():
#     print("*********************In Faculty Assignments**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     courseID = userData.get('courseID')

#     assignment_list = get_faculty_course_assignments(courseID)

#     data = {
#         "assignments": assignment_list
#     }

#     print("Assignments returned are:", data)
#     return data,200


# @app.route('/get_submissions', methods=['POST'])
# @cross_origin()
# def get_submissions():
#     print("*********************In Faculty Submissions**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     assignmentID = userData.get('assignmentID')

#     submission_list = get_faculty_submissions(assignmentID)

#     data = {
#         "submissions": submission_list
#     }

#     print("Submissions returned are:", data)
#     return data,200


# @app.route('/get_subj_responses', methods=['POST'])
# @cross_origin()
# def get_subj_responses():
#     print("*********************In Faculty get subj response**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     submissionID = userData.get('submissionID')
#     assignmentID = userData.get('assignmentID')

#     subj_responses = get_faculty_single_submissions(submissionID, assignmentID)

#     data = {
#         "responses": subj_responses
#     }

#     print("Submissions returned are:", data)
#     return data,200


# @app.route('/post_grades', methods=['POST'])
# @cross_origin()
# def post_grades():
#     print("*********************In Faculty post grades**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     submissionID = userData.get('submissionID')
#     list_of_grades = userData.get('grades')

#     marks = list_of_grades[0]['marks']
#     print("Marks:",marks)

#     put_faculty_submission_grades(submissionID, marks)

#     return "Grades Posted Successfully",200


# @app.route('/create_assignment', methods=['POST'])
# @cross_origin()
# def create_assignment():
#     print("*********************In Faculty create assignment**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     courseID = userData.get('courseID')
#     deadline = userData.get('deadline')
#     list_of_questions = userData.get('questions')

#     print("Questions:",list_of_questions)

#     assignment_id = put_faculty_create_assignment(courseID, deadline, list_of_questions)

#     return jsonify({"message": "Assignment Created Successfully", "AssignmentID":assignment_id}), 200


# @app.route('/submit_feedback', methods=['POST'])
# @cross_origin()
# def submit_feedback():
#     print("*********************In Student Submit Feedback**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     studentID = userData.get('studentID')
#     assignmentID = userData.get('assignmentID')
#     feedbackText = userData.get('feedbackText')

#     put_student_create_feedback(studentID, assignmentID, feedbackText)

#     return "Feedback submitted Successfully", 200


# @app.route('/combine_feedback', methods=['POST'])
# @cross_origin()
# def combine_feedback():
#     print("*********************In Faculty Combine Feedback**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     assignmentID = userData.get('assignmentID')

#     combined_feedback = get_faculty_combine_feedback(assignmentID)

#     data = {
#         "aggregated_feedback":combined_feedback
#     }

#     return data, 200


# @app.route('/course_stats', methods=['POST'])
# @cross_origin()
# def course_stats():
#     print("*********************In Faculty Course Stats**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     courseID = userData.get('courseID')
#     facultyID = userData.get('facultyID')

#     course_stats = get_faculty_assignment_stats(courseID, facultyID)

#     data = {
#         "course_stats":course_stats
#     }

#     return data, 200


# @app.route('/weak_students', methods=['POST'])
# @cross_origin()
# def weak_students():
#     print("*********************In Faculty Weak Students**********************")
#     userData  = request.json
#     print("Request JSON-------------",userData,"\n")
#     courseID = userData.get('courseID')
#     facultyID = userData.get('facultyID')

#     weak_students = get_faculty_weak_students(courseID, facultyID)

#     data = {
#         "weak_students":weak_students
#     }

#     return data, 200