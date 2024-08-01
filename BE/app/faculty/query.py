from app.database import create_engine
import sqlalchemy
from random import randint, randrange
from app.feedback.feedback import get_aggregated_feedback
from scipy.stats import norm
from collections import defaultdict


def get_faculty_courses(username: str) -> list:

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT CourseID from Faculty NATURAL JOIN Course WHERE FacultyID='{username}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    courses_data = []
    for item in result:
      courseID, = item
      courses_data.append(courseID)
    
    data = {
        "courses": courses_data
    }
  return data

#0-----------
def get_faculty_course_assignments(course_id: str) -> list:

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT AssignmentID, Deadline from Course NATURAL JOIN Assignment WHERE CourseID='{course_id}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    assignment_data = []
    for item in result:
      average_score=0
      assignmentID, deadline = item
      average_difficulty = get_average_difficulty(assignmentID)
      # average_score = get_average_score(assignmentID)
      assignment_details = get_assignment_details(assignmentID)
      print("Assignment Details returned",assignment_details)
      print("Average Score:", assignment_details[0])
      print("No of submissions:", assignment_details[1])
      if assignment_details[0]:
        average_score = float(assignment_details[0])
      # feedback = get_faculty_combine_feedback(assignmentID)
      # if average_score:
      #   average_score = float(average_score)
      # data = {
      #   "assignmentID": assignmentID,
      #   "averageDifficulty": float(average_difficulty),
      #   "averageScore":average_score,
      #   # "feedback": feedback
      # }
      data = {
        "assignmentID": assignmentID,
        "averageDifficulty": float(average_difficulty),
        "averageScore": average_score,
        "noOfStudentsSubmitted":assignment_details[1]
        # "feedback": feedback
      }

      assignment_data.append(data)
  return assignment_data


# def get_average_score(assignmentID):
#   pool = create_engine()
#   with pool.connect() as db_conn:
#     query = f"SELECT AVG(TotalScore) AS AverageScore FROM Submission WHERE AssignmentID = '{assignmentID}' GROUP BY AssignmentID;"
#     result = db_conn.execute(sqlalchemy.text(query)).fetchall()
#     print("Average Score is :", result)
  
#   if result:
#     return result[0][0]
#   else:
#     return None


def get_faculty_submissions(assignment_id: str):
  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT SubmissionID FROM Assignment NATURAL JOIN Submission WHERE AssignmentID='{assignment_id}' AND SubScore IS NULL AND SubjAnswer IS NOT NULL;"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()

    print(result)

    submission_list = []
    for item in result:
      submission_list.append(item[0])
    
  return submission_list


def get_faculty_single_submissions(submission_id: str, assignment_id: str):
  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT QuestionID, Question, SubjAnswer FROM Submission NATURAL JOIN Assignment NATURAL JOIN Question WHERE SubmissionID='{submission_id}' AND AssignmentID = '{assignment_id}' AND Type = 'S';"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()

    print(result)
  
  subjAnswer_list = []

  for item in result:
    data = {
            "question_id": item[0],
            "question_text": item[1],
            "response_text": item[2],
    }

    subjAnswer_list.append(data)

  return subjAnswer_list


def put_faculty_submission_grades(submissionID: str, subjMarks: int):
  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"UPDATE Submission SET SubScore = {subjMarks} WHERE SubmissionID= '{submissionID}';"
    result = db_conn.execute(sqlalchemy.text(query))
  
    print(query)
    db_conn.commit()


# def get_new_assignment_number(courseID:str):
#   pool = create_engine()
#   with pool.connect() as db_conn:

#     query = f"SELECT * FROM Assignment WHERE CourseID = '{courseID}' ORDER BY AssignmentID"
#     result = db_conn.execute(sqlalchemy.text(query)).fetchall()

#     print(result)

#     list_of_existing_assignments= []
#     for item in result:
#       list_of_existing_assignments.append(item[0])
    
#     last_assignment = list_of_existing_assignments[-1]
#     last_number = int(last_assignment.split('HW')[-1])

#     print("Last_number is", last_number)

#     new_number = last_number + 1
#     new_assignment = f'MAT_10A_HW{new_number}'

#     print("New Assignment =", new_assignment)

#     return new_assignment


def get_new_assignment_number(courseID: str):
    pool = create_engine()  # Ensure your database connection string is configured correctly here
    print("courseID is", courseID)
    with pool.connect() as db_conn:

        # Modified query to extract numbers and order numerically
        query = f"""
        SELECT AssignmentID FROM Assignment 
        WHERE CourseID = '{courseID}'
        ORDER BY CAST(SUBSTRING(AssignmentID FROM POSITION('HW' IN AssignmentID) + 2) AS UNSIGNED)
        """
        result = db_conn.execute(sqlalchemy.text(query)).fetchall()

        print("AssignmentID existing:",result)

        # Assuming result is not empty and assignments are well-formed
        last_assignment = result[-1][0]  # last element, first column
        last_number = int(last_assignment.split('HW')[-1])

        print("Last_number is", last_number)

        new_number = last_number + 1
        new_assignment = f'{courseID}_HW{new_number}'

        print("New Assignment =", new_assignment)

        return new_assignment


def get_new_question_number():
  pool = create_engine()
  with pool.connect() as db_conn:

    query = f"SELECT MAX(CAST(QuestionID AS UNSIGNED)) FROM Question;"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()

    print("The max question number is",result)

    new_question_number = result[0][0] + 1
    print("New Question Number is", new_question_number)

    return new_question_number



def put_faculty_create_assignment(courseID:str, deadline, list_of_questions):
  print("Deadline is", deadline)
  print("List of questions",list_of_questions)
  pool = create_engine()
  with pool.connect() as db_conn:

    try:
      assignmentID = get_new_assignment_number(courseID)

      query=f"INSERT INTO Assignment(AssignmentID, CourseID, Deadline) VALUES('{assignmentID}','{courseID}', '{deadline}');"
      result = db_conn.execute(sqlalchemy.text(query))

      print("Query is:", query)
      # db_conn.commit()

      for item in list_of_questions:
        questionText = item['questionText']
        correctOption = item['correctOption']
        topic = item['topic']
        assumedDifficulty = item['assumedDifficulty']
        options = item['options']

        # options_string = options[0].split("; ")
        options_string = options
        print("Options String",options_string)
        question_unformatted_text = f"{questionText}\nOptions:\n" + "\n".join(options_string)

        print("New Question Unformatted", question_unformatted_text.replace("\n","\\n"))

        new_question_number = get_new_question_number()

        query = f"""INSERT INTO Question(QuestionID, AssignmentID, Type, Question, Topic, CorrectAnswer, AssumedDifficulty) 
                  VALUES('{new_question_number}', '{assignmentID}', 'O', '{question_unformatted_text}', '{topic}', '{correctOption}', '{assumedDifficulty}')"""

        result = db_conn.execute(sqlalchemy.text(query))

        db_conn.execute(sqlalchemy.text("COMMIT;"))
      
    except Exception as e:
      # Rollback in case of error
      db_conn.execute(sqlalchemy.text("ROLLBACK;"))
      print("Transaction failed:", str(e))
    # db_conn.commit()

  return assignmentID


def get_faculty_combine_feedback(assignmentID):

  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"SELECT Content FROM Feedback WHERE AssignmentID='{assignmentID}'"
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()

    print("Feedback for {assignmentID} is",result)

    combined_feedback = []

    for item in result:
      combined_feedback.append(item[0])

    # print("Feedbacks are:",combined_feedback)

  if result:
    aggregated_feedback = get_aggregated_feedback(combined_feedback)
  else:
    aggregated_feedback = ""

  return aggregated_feedback


def get_average_difficulty(assignmentID):
  print(assignmentID)
  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"""SELECT 
      FacultyID, CourseID, AssignmentID,
      ( SUM((AssumedDifficulty = 'E') * 1.0 * cnt) +
        SUM((AssumedDifficulty = 'M') * 2.0 * cnt) +
        SUM((AssumedDifficulty = 'H') * 3.0 * cnt)
      )/SUM(cnt) AS AssignmentDifficulty
    FROM 
      (
        SELECT 
          FacultyID, CourseID, AssignmentID, AssumedDifficulty, COUNT(*) AS cnt
        FROM 
          Faculty NATURAL JOIN Course NATURAL JOIN Assignment NATURAL JOIN Question
        WHERE 
          AssignmentID LIKE '{assignmentID}' AND Type='O'
        GROUP BY 
          FacultyID, CourseID,AssignmentID, AssumedDifficulty
      ) AS
    SubQuery
    GROUP BY 
      FacultyID, CourseID, AssignmentID;
      """
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()

    print(result)
    print(result[0][3])
  return result[0][3]


def get_faculty_assignment_stats(courseID, facultyID):
  pool = create_engine()
  course_stats=[]
  with pool.connect() as db_conn:
    query = f"""SELECT 
      Course.CourseID, Assignment.AssignmentID, Avg(Submission.TotalScore) AS AvgTotalScore, Count(DISTINCT Submits.StudentID) AS NumberOfStudentsSubmitted, Deadline
      FROM   
      Course LEFT JOIN Assignment
                    ON Course.CourseID = Assignment.CourseID
            LEFT JOIN Submission
                    ON Assignment.AssignmentID = Submission.AssignmentID
            LEFT JOIN Submits
                    ON Submission.SubmissionID = Submits.SubmissionID
      WHERE  
      Course.Facultyid = '{facultyID}' AND Course.CourseID='{courseID}'
      GROUP BY 
      Course.FacultyID, Course.CourseID, Deadline, Assignment.AssignmentID; 

      """
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    print(result)

    for item in result:
      data = {
        "assignmentID": item[1],
        "avgScore":float(item[2]),
        "noOfStudentSubmitted":item[3],
      }
      course_stats.append(data)
  return course_stats


def get_assignment_details(assignmentID):
  pool = create_engine()
  course_stats=[]
  with pool.connect() as db_conn:
    query = f"""SELECT 
      Assignment.AssignmentID, Avg(Submission.TotalScore) AS AvgTotalScore, Count(DISTINCT Submits.StudentID) AS NumberOfStudentsSubmitted, Deadline
      FROM   
      Course LEFT JOIN Assignment
                    ON Course.CourseID = Assignment.CourseID
            LEFT JOIN Submission
                    ON Assignment.AssignmentID = Submission.AssignmentID
            LEFT JOIN Submits
                    ON Submission.SubmissionID = Submits.SubmissionID
      WHERE  
      Assignment.AssignmentID='{assignmentID}'
      GROUP BY 
      Course.FacultyID, Course.CourseID, Deadline, Assignment.AssignmentID; 

      """
    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    print("Assignment Details",result)
  

  return (result[0][1], result[0][2])

  #   for item in result:
  #     data = {
  #       "assignmentID": item[1],
  #       "avgScore":float(item[2]),
  #       "noOfStudentSubmitted":item[3],
  #     }
  #     course_stats.append(data)
  # return course_stats


def get_faculty_weak_students(courseID):
  pool = create_engine()
  with pool.connect() as db_conn:
    query = f"""
        SELECT 
          s.StudentID, s.Email, ScoreStats.avg_score, sub.TotalScore, s.FirstName, s.LastName, sub.AssignmentID, ScoreStats.std_dev,
        (sub.TotalScore - ScoreStats.avg_score) / ScoreStats.std_dev AS std_devs_behind
    FROM
        Student s
    NATURAL JOIN 
        Submits su
    NATURAL JOIN 
        Submission sub
    NATURAL JOIN 
        Assignment a
    JOIN 
        (SELECT 
            Assignment.AssignmentID, AVG(Submission.TotalScore) AS avg_score, STDDEV(Submission.TotalScore) AS std_dev
        FROM 
            Submission
        NATURAL JOIN 
            Assignment     
    WHERE 
            Assignment.CourseID = '{courseID}'
        GROUP BY 
            Assignment.AssignmentID
        ) AS ScoreStats ON a.AssignmentID = ScoreStats.AssignmentID
    WHERE 
        sub.TotalScore < ScoreStats.avg_score
    """

    result = db_conn.execute(sqlalchemy.text(query)).fetchall()
    print(result)

  weak_students = []

  for item in result:
    data = {
      "studentID": item[0],
      "avgScore": item[2],
      "studentScore": item[3],
      "studentName": item[4]+item[5],
      "assignmentID": item[6],
      "assignmentSTD": item[7],
      "percentile":norm.cdf(item[8]) * 100
    }

    weak_students.append(data)

  # perennially_weak_students = []
  # perennially_weak_students = defaultdict(list)
  # for item in weak_students:
  #   print("Item", item)
  #   print('StudentID', item['studentID'])
  #   overall_weak_student = defaultdict(set)
  #   overall_weak_student[item['studentID']].add(item['assignmentID'])

  #   perennially_weak_students.append(overall_weak_student)
  
  # print(perennially_weak_students)

  # perennially_weak_students = defaultdict(set)
  # for item in weak_students:
  #   print("Item", item)
  #   print('StudentID', item['studentID'])

  #   # Append to the set associated with the studentID
  #   perennially_weak_students[item['studentID']].add(item['assignmentID'])

  #   # Now, if you need it in a list format, where each entry is a dictionary
  #   consolidated_list = []
  # for student_id, assignments in perennially_weak_students.items():
  #     consolidated_list.append({student_id: tuple(assignments)})

  # print(consolidated_list)


  # perennially_weak_students = defaultdict(set)

  # for item in weak_students:
  #     # Append to the set associated with the studentID
  #     perennially_weak_students[item['studentID']].add(item['assignmentID'])

  # # Now, build the list format with each entry having the count of assignments
  # consolidated_student = []
  # for student_id, assignments in perennially_weak_students.items():
  #     # Create a dictionary for each student with their assignments and the count of assignments
  #     student_info = {
  #         student_id: tuple(assignments),
  #         'count': len(assignments)  # Add the count of assignments
  #     }
  #     consolidated_student.append(student_info)

  # print(consolidated_student)

  perennially_weak_students = defaultdict(set)

  for item in weak_students:
      # Append to the set associated with the studentID
      perennially_weak_students[item['studentID']].add(item['assignmentID'])

  # Now, build the list format with each entry in the specified format, including a condition for more than 2 assignments
  consolidated_list = []
  for student_id, assignments in perennially_weak_students.items():
      if len(assignments) > 2:  # Only include students with more than 2 assignments
          student_info = {
              "studentID": student_id,
              "noOfAssignments": len(assignments),
              "listOfAssignments": list(assignments)
          }
          consolidated_list.append(student_info)

  print(consolidated_list)
  return consolidated_list