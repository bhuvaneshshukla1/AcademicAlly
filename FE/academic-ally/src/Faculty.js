import React, { useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import "./Faculty.css";

function Faculty() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [assignments, setAssignments] = useState([]);
  const [selectedAssignment, setSelectedAssignment] = useState('');
  const [showAssignments, setShowAssignments] = useState(false);
  const [submissions, setSubmissions] = useState([]);
  const [selectedSubmission, setSelectedSubmission] = useState('');
  const [showSubmissions, setShowSubmissions] = useState(false);
  const [averageDifficulty, setAverageDifficulty] = useState(null);
  const [selectedAssignmentDifficulty, setSelectedAssignmentDifficulty] = useState('');
  const [chartData, setChartData] = useState({});
  const [aggregatedFeedback, setAggregatedFeedback] = useState('');
  const [weakStudents, setWeakStudents] = useState([]);
  const username = localStorage.getItem('username');


const formatFeedback = feedbackText => {
    const parts = feedbackText.split('*').map(part => part.trim()).filter(part => part);
    return (
      <>
        {parts.map((part, index) => (
          <p key={index}>&bull; {part}</p> // Bullet point for each feedback item
        ))}
      </>
    );
  };

  const handleLogout = () => {
    localStorage.clear(); // Clears all local storage
    navigate('/'); // Navigate to login page
  };

  const fetchCourses = useCallback(async () => {  // Use useCallback to ensure function stability
    try {
      const response = await axios.post('http://35.208.243.254:8080/faculty_courses', { username: localStorage.getItem('username') });
      setCourses(response.data.courses || []);
    } catch (error) {
      console.error("Failed to fetch courses:", error);
      setCourses([]);
    }
  }, []);  // Dependencies should include any props/state used inside

  useEffect(() => {
    if(courses.length === 0) {
      fetchCourses();
    }
    
  }, [courses.length, fetchCourses]);  // Now properly dependent on courses.length and fetchCourses

const fetchAssignmentsAndDifficulties = async (courseID) => {
    try {
        const response = await axios.post('http://35.208.243.254:8080/faculty_assignments', { courseID });
        setAssignments(response.data.assignments || []);
        setShowAssignments(true);
	setWeakStudents(response.data.weakStudents || []);

        if (response.data.assignments.length > 0) {
            const totalDifficulty = response.data.assignments.reduce((acc, curr) => acc + curr.averageDifficulty, 0);
            const avgDifficulty = totalDifficulty / response.data.assignments.length;
            setAverageDifficulty(avgDifficulty.toFixed(2));

            // Prepare data for the chart
            const difficultyScores = response.data.assignments.reduce((acc, curr) => {
                const { averageDifficulty, averageScore } = curr;
                if (acc[averageDifficulty]) {
                    acc[averageDifficulty].push(averageScore);
                } else {
                    acc[averageDifficulty] = [averageScore];
                }
                return acc;
            }, {});

            const difficulties = Object.keys(difficultyScores).map(parseFloat).sort();
            const scores = difficulties.map(diff => {
                const scores = difficultyScores[diff];
                return scores.reduce((a, b) => a + b, 0) / scores.length;
            });

            setChartData({
                labels: difficulties,
                datasets: [{
                    label: 'Average Score vs. Difficulty',
                    data: scores,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            });
        } else {
            setAverageDifficulty(0); // No assignments mean no difficulty to average
            setChartData({});
        }
    } catch (error) {
        console.error("Failed to fetch assignments and difficulties:", error);
        setAssignments([]);
        setAverageDifficulty(null);
        setChartData({});
	setWeakStudents([]);
    }
};


  const handleCourseChange = async (event) => {
   const selected = event.target.value;
    localStorage.setItem('courseID',selected);
    setSelectedCourse(selected);
   setShowAssignments(false);
	if (selected) {
     fetchAssignmentsAndDifficulties(selected);
    }

 //   try {
 //     const response = await axios.post('http://35.208.243.254:8080/assignments', {
  //      courseID: selected
 //     }, {
   //     headers: {
   //       'Content-Type': 'application/json'
   //     }
   //   });
      
   //   setAssignments(response.data.assignment || []);
   //   setShowAssignments(true);
   // } catch (error) {
   //   console.error("Failed to fetch assignments:", error);
   //   setAssignments([]);
  //  }
  };

const handleAssignmentChange = async (event) => {
    const selected = event.target.value;
    setSelectedAssignment(selected);
    setShowSubmissions(false);
    const foundAssignment = assignments.find(assignment => assignment.assignmentID === selected);
    if (foundAssignment) {
      setSelectedAssignmentDifficulty(foundAssignment.averageDifficulty.toFixed(2));
    }
    try {
      const response = await axios.post('http://35.208.243.254:8080/get_submissions', {
        assignmentID: selected
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setSubmissions(response.data.submissions || []);
      setShowSubmissions(true);
 const feedbackResponse = await axios.post('http://35.208.243.254:8080/combine_feedback', {
        assignmentID: selected
      });
      setAggregatedFeedback(feedbackResponse.data.aggregated_feedback || 'No feedback available');
    } catch (error) {
      console.error("Failed to fetch submissions or feedback:", error);
      setSubmissions([]);
      setAggregatedFeedback('');
    }
  };
    


  const handleSubmissionSelection = (event) => {
    
    setSelectedSubmission(event.target.value);
  };

  const openSubmission = () => {
    if (selectedSubmission) {
      localStorage.setItem('assignmentID',selectedAssignment);
      localStorage.setItem('submissionID',selectedSubmission);
      navigate('/gradesubmission', { state: { submissionID: selectedSubmission, username: localStorage.getItem('username'), submissionID: selectedAssignment } });
    } else {
      alert("Please select a submission first.");
    }
  };

const handleCreateAssignment = () => {
    if (selectedCourse) {
      navigate('/createAssignment',{state: {courseID: localStorage.getItem('courseID') }}); // Assuming the path to create assignments is '/createAssignment'
    } else {
      alert("Please select a course first.");
    }
  };

  return (
    <div class="dashboard-container">
      <div class="dashboard-titles">
        <h1>Faculty Dashboard</h1>
        <div className='lt'>
        <h2 class="welcome">Welcome back {username}</h2>
        <button className = "logout" onClick={handleLogout}>Logout</button>
      </div>
      </div>

      <div class="dashboard-content">
        <div class="left-pane">
          <h2>Select a Course</h2>
          <select onChange={handleCourseChange} value={selectedCourse}>
            <option value="">Select a course</option>
            {courses.map((course, index) => (
              <option key={index} value={course}>{course}</option>
            ))}
          </select>

          {averageDifficulty !== null && <span className = "diff">Average Difficulty: {averageDifficulty}</span>}

      

          {showAssignments && (
            <div>
              <h2>Select an Assignment</h2>
              <select onChange={handleAssignmentChange} value={selectedAssignment}>
                <option value="">Select an assignment</option>
                {assignments.map((assignment, index) => (
                  <option key={index} value={assignment.assignmentID}>
                    {assignment.assignmentID}
                  </option>
                ))}
              </select>

              {selectedAssignment && <span className='diff'>Difficulty of Selected Assignment: {selectedAssignmentDifficulty}</span>}

              {selectedAssignment && (
                <div className='scroll-feedback'>
                  <h2><center>Feedback for {selectedAssignment}</center></h2>
                  {aggregatedFeedback ? formatFeedback(aggregatedFeedback) : <p>No feedback available.</p>}
                </div>
              )}

              {selectedCourse && <button onClick={handleCreateAssignment}>Create Assignment</button>}
            </div>
          )}

          {showAssignments && showSubmissions && (
            <div>
              <h2>Select a Submission</h2>
              <select onChange={handleSubmissionSelection} value={selectedSubmission}>
                <option value="">Select a Submission</option>
                {submissions.map((submission, index) => (
                  <option key={index} value={submission}>
                    {submission}
                  </option>
                ))}
              </select>
              <button onClick={openSubmission}>Open Submission for grading</button>
            </div>
          )}
        </div>

        <div class="right-pane">
          {chartData.labels && <Line data={chartData} />}

          <a href="https://lookerstudio.google.com/u/2/reporting/8945d0ec-081a-400b-8514-b4749d4c492b/page/4bmyD" target="_blank" rel="noopener noreferrer">Visit Metrics-Hub for more insights</a>
        
          <div className='scroll'> 
            <h2>Weak Students</h2>
            <table>
              <thead>
                <tr>
                  <th>Student ID</th>
                  <th>Number of Assignments</th>
                  <th>List of Assignments</th>
                </tr>
              </thead>
              <tbody>
                {weakStudents.map((student, index) => (
                  <tr key={index}>
                    <td>{student.studentID}</td>
                    <td>{student.noOfAssignments}</td>
                    <td>{student.listOfAssignments.join(', ')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
      </div>
    </div>
  );
}

export default Faculty;