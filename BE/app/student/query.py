from app.database import create_engine
import sqlalchemy
from random import randint, randrange
from datetime import datetime

def get_user_password(username: str) -> str:

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT Password, UserType from User WHERE UserID='{username}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchone()

  if result:
    return result[0], result[1]
  else:
    return None


def get_student_courses(username: str) -> list:

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT CourseID from Student NATURAL JOIN Class NATURAL JOIN Course WHERE StudentID='{username}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    courses_data = []
    for item in result:
      courseID, = item
      courses_data.append(courseID)
    
    data = {
        "courses": courses_data
    }
  return data


def get_student_course_assignments(course_id: str) -> list:

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT AssignmentID, Deadline from Course NATURAL JOIN Assignment WHERE CourseID='{course_id}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    assignment_data = []
    for item in result:
      assignmentID, deadline = item
      data = {
        "assignmentID": assignmentID,
        "deadline": deadline
      }
      assignment_data.append(data)
  return assignment_data


def get_student_assignment_questions(assignment_id: str) -> list:

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT QuestionID, Question, Type FROM Question NATURAL JOIN Assignment WHERE AssignmentID='{assignment_id}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    # print("Return Student Assignment Questions -",result)
    question_data = []
    for item in result:
      question_id, question_text, question_type = item
      print("*********************Question Text", question_text.replace("\n", "\\n"))
    #   print(question_text)
      if question_type == 'O':
        questions_text_data = question_text.split("Options:")
        print("*****************Questions Text Data:", questions_text_data)
        actual_question_text = questions_text_data[0]
        print("*****************Actual Question Text:", actual_question_text)
        actual_question_options = questions_text_data[1]
        print("*****************Actual Question Options:", actual_question_options)
        actual_question_options.replace("$",'')
        print("*****************Actual Question Options:", actual_question_options)

        options = actual_question_options.split("\n")
        print("*****************Options", options)
        options.pop(0)
        print("*****************Options", options)

        #   print(actual_question_options)
        data = {
            "question_id": question_id,
            "question_text": actual_question_text,
            "options": options,
            "question_type":question_type
        }
    
      elif question_type == 'S':
        options = []
        data = {
            "question_id": question_id,
            "question_text": question_text,
            "options": question_type,
            "options": options,
            "question_type": question_type
        }

      question_data.append(data)
  return question_data



def get_student_assignment_questions_answers(assignment_id: str) -> list:
  # print(assignment_id)
  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT QuestionID, CorrectAnswer, Type FROM Question NATURAL JOIN Assignment WHERE AssignmentID='{assignment_id}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    # print("Return Question, Correct Answer - ",result)
    question_data = []
    for item in result:
      question_id, correctAnswer, questionType = item
      data = {
        "question_id": question_id,
        "correctAnswer": correctAnswer,
        "type": questionType
      }
      question_data.append(data)
    # print(question_data)
  return question_data


def get_student_faculty(studentID, assignmentID: str) -> str:

  print("Assignment ID is",assignmentID)
  # courseID = assignmentID[0:-4]

  courseID = assignmentID.split("_HW")[0]
  print("CourseID",courseID)
  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT FacultyID from Student NATURAL JOIN Class NATURAL JOIN Course WHERE StudentID='{studentID}' AND CourseID='{courseID}'"
    # print("Faculty Check -",query)
    result = db_conn.execute(sqlalchemy.text(query)).fetchone()
  # print(result)
  return result[0]


def check_deadline(assignmentID):
  pool = create_engine()
  with pool.connect() as db_conn:
    print("Deadline check")
    query = f"SELECT Deadline FROM Assignment WHERE AssignmentID = '{assignmentID}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchone()
  
  print("Deadline:",result)
  return result[0]



def check_submission(studentID, assignmentID: str) -> str:

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT SubmissionID FROM Submits NATURAL JOIN Submission WHERE StudentID='{studentID}' AND AssignmentID='{assignmentID}'"
    # print("SubmissionID Check -",query)
    result = db_conn.execute(sqlalchemy.text(query)).fetchone()
  print("Existing Submission ID",result)
  if result:
    return result[0]
  else:
    return False


# def update_submission(submissionID, objScore: int, totalScore: int, subjective_exists, subjAnswer):
#     pool = create_engine()
#     # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
#     # print(subjAnswer)
#     # print(objScore)
#     # print(totalScore)
#     with pool.connect() as db_conn:
#         if subjective_exists:
#             query = f"UPDATE Submission SET ObjScore='{objScore}', TotalScore='{totalScore}', SubjAnswer='{subjAnswer}' WHERE SubmissionID='{submissionID}';"
#         else:
#             query = f"UPDATE Submission SET ObjScore='{objScore}', TotalScore='{totalScore}' WHERE SubmissionID='{submissionID}';"
#         # print("Submission update -",query)
#         result = db_conn.execute(sqlalchemy.text(query))
#         # print(result)
#         db_conn.commit()


# def put_student_submission(studentID: str, assignmentID: str, objScore: int, totalScore: int, subjective_exists: bool, subjAnswer: str):
  
#   submissionID = check_submission(studentID, assignmentID)
#   # print("@@@@@@@@@@@@@@@@@@@",submissionID)
#   pool = create_engine()
#   with pool.connect() as db_conn:

#     if submissionID:
#         print("Updating submission")
#         update_submission(submissionID, objScore, totalScore, subjective_exists, subjAnswer)
#         return

#     facultyID = get_student_faculty(studentID, assignmentID)
#     submissionID = "SUB"+str(randrange(100000, 1000000))

#     print("Creating submission")
#     if subjective_exists:
#         query = f"INSERT INTO Submission(SubmissionID,AssignmentID,FacultyID,ObjScore,TotalScore, SubjAnswer) values('{submissionID}','{assignmentID}','{facultyID}',{objScore},{totalScore}, '{subjAnswer}');"
#     else:
#         query = f"INSERT INTO Submission(SubmissionID,AssignmentID,FacultyID,ObjScore,TotalScore) values('{submissionID}','{assignmentID}','{facultyID}',{objScore},{totalScore});"
#     result = db_conn.execute(sqlalchemy.text(query))
#     print("Submission insert - ",query)

#     query = f"INSERT INTO Submits(SubmissionID, StudentID) VALUES('{submissionID}','{studentID}');"
#     result = db_conn.execute(sqlalchemy.text(query))
#     print("Submits insert",result)

#     db_conn.commit()
#     # print(result)

  
def get_upcoming_deadlines(studentID: str, todayDate):

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"""(
        (SELECT 
          AssignmentID, StudentID, deadline 
        FROM (
          SELECT 
            ClassID, CourseID, AssignmentID, StudentID, deadline 
          FROM 
            Student NATURAL JOIN Class NATURAL JOIN Course NATURAL JOIN Assignment 
          WHERE 
            deadline > '{todayDate}' AND StudentID = '{studentID}'
          GROUP BY 
	          StudentID, ClassID, CourseID, AssignmentID, deadline
        ) AS T1) 
        
        EXCEPT
          SELECT 
            AssignmentID, StudentID, deadline
          FROM 
            Submits NATURAL JOIN Submission NATURAL JOIN Assignment
          WHERE 
            Deadline > '{todayDate}' AND StudentID = '{studentID}'
          GROUP BY 
	          StudentID, AssignmentID, deadline)
        ORDER BY deadline;
      """
    
    results = db_conn.execute(sqlalchemy.text(query)).fetchall()
    # print("All upcoming deadlines are:",results)

    fullData = []

    for result in results:
      data = {
              "assignment_id": result[0],
              "deadline": result[2],
          }
      fullData.append(data)
    
  return fullData


def put_student_submission_new(studentID: str, assignmentID: str, subjectiveExists: bool, subjAnswer: str, objAnswers):

  submissionExists = False
  # submissionID = "SUB"+str(randrange(100000, 1000000))
  facultyID = get_student_faculty(studentID, assignmentID)

  submissionID = check_submission(studentID, assignmentID)

  deadline = check_deadline(assignmentID)
  todayDate = datetime.today()
  print("Today's date:", todayDate)
  if deadline < todayDate:
    return "Deadline Passed."

  if submissionID:
    submissionExists = True

  if not submissionExists:
    print("Submission ID doesn't exist")
    submissionID = "SUB"+str(randrange(100000, 1000000))

  pool = create_engine()
  with pool.connect() as db_conn:

    try:
      db_conn.execute(sqlalchemy.text("START TRANSACTION;"))

      query = "CREATE TEMPORARY TABLE TempResponses (StudentID VARCHAR(20), SubmissionID VARCHAR(20), QuestionID VARCHAR(20), response VARCHAR(100));"
      # query = "CREATE TABLE IF NOT EXISTS TempResponses (StudentID VARCHAR(20), SubmissionID VARCHAR(20), QuestionID VARCHAR(20), response VARCHAR(100));"
      result = db_conn.execute(sqlalchemy.text(query))

      query = "CREATE TEMPORARY TABLE TempIncorrectResponses (SubmissionID VARCHAR(20), Topic VARCHAR(255));"
      # query = "CREATE TABLE IF NOT EXISTS TempResponses (StudentID VARCHAR(20), SubmissionID VARCHAR(20), QuestionID VARCHAR(20), response VARCHAR(100));"
      result = db_conn.execute(sqlalchemy.text(query))
      # db_conn.commit()

      # query = "SHOW TABLES;"
      # result = db_conn.execute(sqlalchemy.text(query)).fetchall()
      # print("Show Tables",result)

      # query = "SELECT * FROM TempResponses;"
      # result = db_conn.execute(sqlalchemy.text(query)).fetchall()
      # print("Result1",result)

      for key in objAnswers:

        query = f"INSERT INTO TempResponses VALUES('{studentID}', '{submissionID}', '{key}', '{objAnswers[key]}')"
        result = db_conn.execute(sqlalchemy.text(query))
        print("Result2", result)
        # db_conn.commit()

      if submissionExists:
        print("Updating Submission")
        proc_call = sqlalchemy.text("CALL UpdateScoresWithProcedure(:assignment_id, :faculty_id, :submission_id)")
        result = db_conn.execute(proc_call, {'assignment_id': assignmentID, 'faculty_id': facultyID, 'submission_id': submissionID}).fetchone()
        print(assignmentID, facultyID, submissionID)
        print("Result3", result)

      else:
        print("Creating Submission")
        proc_call = sqlalchemy.text("CALL CalculateScoresWithProcedure(:assignment_id, :faculty_id, :submission_id)")
        result = db_conn.execute(proc_call, {'assignment_id': assignmentID, 'faculty_id': facultyID, 'submission_id': submissionID}).fetchone()
        print(assignmentID, facultyID, submissionID)
        print("Result3", result)

      if subjectiveExists:
        query = f"UPDATE Submission SET SubjAnswer = '{subjAnswer}' WHERE submissionID = '{submissionID}'"
        print(query)
        result = db_conn.execute(sqlalchemy.text(query))
        print("Result4", result)
        # db_conn.commit()
    
      # query = "SELECT * FROM TempResponses;"
      # result = db_conn.execute(sqlalchemy.text(query)).fetchall()
      # print("Result6",result)

      # query = "DROP TABLE TempResponses;"
      # result = db_conn.execute(sqlalchemy.text(query))
      # print("Result5", result)
      # db_conn.commit()

      db_conn.execute(sqlalchemy.text("COMMIT;"))

      return "Assignment submitted successfully"

    except Exception as e:
      # Rollback in case of error
      db_conn.execute(sqlalchemy.text("ROLLBACK;"))
      print("Transaction failed:", str(e))

      return "Submission Unsuccessful"


def put_student_create_feedback(studentID, assignmentID, feedbackText):
  print("FeedbackText is", feedbackText)
  pool = create_engine()
  feedbackExists = False

  with pool.connect() as db_conn:
    try:
      db_conn.execute(sqlalchemy.text("START TRANSACTION;"))

      query = f"SELECT * FROM Feedback WHERE StudentID='{studentID}' AND AssignmentID='{assignmentID}'"
      result = db_conn.execute(sqlalchemy.text(query)).fetchone()
      print(result)
      if result:
        print("Feedback Exists")
        feedbackExists = True

      if feedbackExists:
        query = f"UPDATE Feedback SET Content='{feedbackText}' WHERE StudentID='{studentID}' AND AssignmentID='{assignmentID}'"
        print(query)
        result = db_conn.execute(sqlalchemy.text(query))

      else:
        query = f"INSERT INTO Feedback VALUES('{studentID}','{assignmentID}','{feedbackText}')"
        print(query)
        result = db_conn.execute(sqlalchemy.text(query))
      
      db_conn.execute(sqlalchemy.text("START TRANSACTION;"))

    except Exception as e:
      # Rollback in case of error
      db_conn.execute(sqlalchemy.text("ROLLBACK;"))
      print("Transaction failed:", str(e))


    # db_conn.commit()


# def get_student_course_stats(courseID, studentID):

#   assigment_dict={}
#   courseDetails = []
#   pool = create_engine()
#   with pool.connect() as db_conn:
#     query = f"""
#         SELECT 
#           a.AssignmentID,
#           s.SubmissionID,
#           s.TotalScore AS StudentScore,
#           (
#             SELECT AVG(TotalScore)
#             FROM 
#               Submission 
#             WHERE 
#               AssignmentID = a.AssignmentID)
#              AS ClassAverageScore
#       FROM
#           Assignment a
#       LEFT JOIN
#           Submission s ON a.AssignmentID = s.AssignmentID AND s.SubmissionID IN 
#               (SELECT SubmissionID FROM Submits WHERE StudentID = '{studentID}')
#       WHERE
#           a.CourseID = '{courseID}';
#     """

#     result = db_conn.execute(sqlalchemy.text(query)).fetchall()
#     print("Result:",result)

#     for item in result:
#       topics = []
#       query = f"SELECT Topic FROM Question WHERE AssignmentID='{item[0]}'"
#       resultTopics = db_conn.execute(sqlalchemy.text(query)).fetchall()

#       for topic in resultTopics:
#         topics.append(topic[0])
      
#       topics = sorted(topics)

#       # print(topics)

#       if item[2]:
#         avgScore = float(item[3])
#       else:
#         avgScore = None
      
#       if item[2]:
#         data = {
#           "assignmentID":item[0],
#           "studentMarks": item[2],
#           "classAverage": avgScore,
#           "topics": topics
#         }
#         courseDetails.append(data)

#   return courseDetails


def get_student_course_stats_new(courseID, studentID):

  print("In get_student_course_stats_new")
  assigment_dict={}
  courseDetails = []
  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"""
        SELECT 
          a.AssignmentID,
          s.SubmissionID,
          s.TotalScore AS StudentScore,
          (
            SELECT AVG(TotalScore)
            FROM 
              Submission 
            WHERE 
              AssignmentID = a.AssignmentID)
             AS ClassAverageScore
      FROM
          Assignment a
      LEFT JOIN
          Submission s ON a.AssignmentID = s.AssignmentID AND s.SubmissionID IN 
              (SELECT SubmissionID FROM Submits WHERE StudentID = '{studentID}')
      WHERE
          a.CourseID = '{courseID}';
    """

    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    print("Result:",result)

    for item in result:
      topics = []
      query = f"SELECT Topic FROM IncorrectResponses NATURAL JOIN Submission NATURAL JOIN Submits WHERE AssignmentID='{item[0]}' AND StudentID='{studentID}' "
      resultTopics = db_conn.execute(sqlalchemy.text(query)).fetchall()

      for topic in resultTopics:
        topics.append(topic[0])
      
      topics = sorted(topics)

      # print(topics)

      if item[2]:
        avgScore = float(item[3])
      else:
        avgScore = None
      
      if item[2]:
        data = {
          "assignmentID":item[0],
          "studentMarks": item[2],
          "classAverage": avgScore,
          "suggestedTopics": topics
        }
        courseDetails.append(data)

  return courseDetails
