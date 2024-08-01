import React, { useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Bar,Pie } from 'react-chartjs-2';
import 'chart.js/auto';
import "./Course.css";

function CourseSelectPage() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [assignments, setAssignments] = useState([]);
  const [selectedAssignment, setSelectedAssignment] = useState('');
  const [showAssignments, setShowAssignments] = useState(false);
  const [deadlines, setDeadlines] = useState([]);
const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [feedbackText, setFeedbackText] = useState('');
const [stats, setStats] = useState([]);
const [pieData, setPieData] = useState({});
const [selectedBarIndex, setSelectedBarIndex] = useState(null);
const username = localStorage.getItem('username');
const [interactiveChartData, setInteractiveChartData] = useState({
  labels: [],
  datasets: []
});
const [assignmentTopics, setAssignmentTopics] = useState({});

  const fetchCourses = useCallback(async () => {  // Use useCallback to ensure function stability
    try {
      const response = await axios.post('http://35.208.243.254:8080/courses', { username: localStorage.getItem('username') });
      setCourses(response.data.courses || []);
    } catch (error) {
      console.error("Failed to fetch courses:", error);
      setCourses([]);
    }
  }, []);  // Dependencies should include any props/state used inside

  const handleLogout = () => {
    localStorage.clear(); // Clears all local storage
    navigate('/'); // Navigate to login page
  };

  useEffect(() => {
    if(courses.length === 0) {
      fetchCourses();
      fetchDeadlines();
    }
    
  }, [courses.length, fetchCourses]);  // Now properly dependent on courses.length and fetchCourses

useEffect(() => {
    fetchCourses();
    fetchDeadlines();
  }, [fetchCourses]);

const fetchDeadlines = async () => {
    try {
      const response = await axios.post('http://35.208.243.254:8080/upcoming_deadlines', {
        username: localStorage.getItem('username')
      });
      setDeadlines(response.data.deadlines || []);
    } catch (error) {
      console.error("Failed to fetch deadlines:", error);
      setDeadlines([]);
    }
  };

const fetchStats = async (courseID, studentID) => {
  try {
    const response = await axios.post('http://35.208.243.254:8080/student_course_stats', {
      courseID: courseID,
      studentID: studentID
    });
    const fetchedStats = response.data.stats || [];
    setStats(fetchedStats);

    // Processing to extract unique topics for each assignment
    const topicsByAssignment = fetchedStats.reduce((acc, curr) => {
      if (curr.suggestedTopics && curr.suggestedTopics.length > 0) {        // Using a Set to ensure uniqueness
        acc[curr.assignmentID] = [...new Set(curr.suggestedTopics)];      }
      return acc;
    }, {});

    setAssignmentTopics(topicsByAssignment);
  } catch (error) {
    console.error("Failed to fetch course stats:", error);
    setStats([]);
    setAssignmentTopics({});
  }
};

  const handleCourseChange = async (event) => {
    const selected = event.target.value;
    setSelectedCourse(selected);
    setShowAssignments(false);
    setPieData({});
fetchStats(selected, localStorage.getItem('username'));

    try {
      const response = await axios.post('http://35.208.243.254:8080/assignments', {
        courseID: selected
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setAssignments(response.data.assignment || []);
      setShowAssignments(true);
    } catch (error) {
      console.error("Failed to fetch assignments:", error);
      setAssignments([]);
    }
  };


  const handleAssignmentSelection = (event) => {
    
    setSelectedAssignment(event.target.value);
  };

  const openAssignment = () => {
    if (selectedAssignment) {
      localStorage.setItem('assignmentID',selectedAssignment)
      navigate('/questions', { state: { assignmentID: selectedAssignment, username: localStorage.getItem('username') } });
    } else {
      alert("Please select an assignment first.");
    }
  };

 const handleFeedbackClick = () => {
    setShowFeedbackForm(true); // Show feedback form
  };

const handleFeedbackSubmit = async () => {
    const studentID = localStorage.getItem('username');
    const assignmentID = selectedAssignment;

    await axios.post('http://35.208.243.254:8080/submit_feedback', {
      studentID: studentID,
      feedbackText: feedbackText,
      assignmentID: assignmentID
    }).then(() => {
      alert('Feedback submitted successfully!');
      setFeedbackText(''); // Clear the feedback input
      setShowFeedbackForm(false); // Hide the feedback form
    }).catch(error => {
      console.error('Failed to submit feedback:', error);
      alert('Failed to submit feedback.');
    });
  };

const chartData = {
  labels: stats.map(stat => stat.assignmentID),
  datasets: [
    {
      label: 'Student Marks',
      data: stats.map(stat => ({
        x: stat.assignmentID,
        y: stat.studentMarks
      })),
      backgroundColor: 'rgba(53, 162, 235, 0.5)'
    },
    {
      label: 'Class Average',
      data: stats.reduce((filtered, stat) => {
        if (stat.classAverage !== undefined && stat.assignmentID) {
          filtered.push({
            x: stat.assignmentID,
            y: stat.classAverage
          });
        }
        return filtered;
      }, []),
      type: 'line',
      borderColor: 'rgb(255, 99, 132)',
      borderWidth: 2,
      fill: false
    }
  ]
};

const aggregateTopics = (stats) => {
  const topicCounts = {};

  stats.forEach(stat => {
    stat.suggestedTopics.forEach(topic => {
      if (topicCounts[topic]) {
        topicCounts[topic] += 1;
      } else {
        topicCounts[topic] = 1;
      }
    });
  });

  return topicCounts;
};

useEffect(() => {
console.log(stats);
  if (stats.length > 0) {

    const filteredStats = selectedBarIndex !== null ? [stats[selectedBarIndex]] : stats;
	console.log(filteredStats);

    // Updating the interactive chart data for the bar and line chart
    setInteractiveChartData({
      labels: filteredStats.map(stat => stat.assignmentID),
      datasets: [
        {
          label: 'Student Marks',
          data: filteredStats.map(stat => ({
            x: stat.assignmentID,
            y: stat.studentMarks
          })),
          backgroundColor: 'rgba(53, 162, 235, 0.5)'
        },
        {
          label: 'Class Average',
          data: filteredStats.map(stat => ({
            x: stat.assignmentID,
            y: stat.classAverage
          })),
          type: 'line',
          borderColor: 'rgb(255, 99, 132)',
          borderWidth: 2,
          fill: false
        }
      ]
    });
	console.log(interactiveChartData);

    // Aggregate topics only from filtered statistics
    const topicCounts = aggregateTopics(filteredStats);
    const topics = Object.keys(topicCounts);
    const counts = topics.map(topic => topicCounts[topic]);

    // Updating the pie chart data based on aggregated topics
    setPieData({
      labels: topics,
      datasets: [{
        data: counts,
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#F7464A',
          '#949FB1',
          '#AC64AD'
        ],
        hoverBackgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#F7464A',
          '#949FB1',
          '#AC64AD'
        ]
      }]
    });
  }
}, [stats, selectedBarIndex]); // Depend on stats and selectedBarIndex
 // Include selectedBarIndex as a dependency
 // React to changes in stats or selected bar

const chartOptions = {
  responsive: true,
  scales: {
    x: { type: 'category' },
    y: { beginAtZero: true }
  },
  plugins: {
    tooltip: { enabled: true },
    legend: { display: true },
    onClick: (event, elements, chart) => {
      console.log(elements); // Log clicked elements to ensure data is received
      if (elements.length > 0) {
        const elementIndex = elements[0].index;
        console.log('Element index:', elementIndex); // Check the index of clicked bar
        setSelectedBarIndex(elementIndex);
      } else {
        console.log('No elements clicked, resetting index.');
        setSelectedBarIndex(null); // Reset if clicking outside of bars
      }
    }
  }
};

// Ensure data is ready and valid for rendering the Pie chart
const isPieDataReady = pieData && pieData.datasets && pieData.datasets[0] && pieData.datasets[0].data.length > 0;
return (
  <div class="dashboard-container">
    <div class="dashboard-titles">
      <h1>Student Dashboard</h1>
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
        <div>

        {Object.keys(assignmentTopics).length > 0 && (
          <div>
            <h2>Assignment Topics</h2>
            <table>
              <thead>
                <tr>
                  <th>Assignment ID</th>
                  <th>Suggested Topics</th>
                </tr>
              </thead>
              <tbody>
                {Object.keys(assignmentTopics).map((assignmentID) => (
                  <tr key={assignmentID}>
                    <td>{assignmentID}</td>
                    <td>{assignmentTopics[assignmentID].join(', ')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

      </div>
        {showAssignments && (
          <div>
            <h2>Select an Assignment</h2>
            <select onChange={handleAssignmentSelection} value={selectedAssignment}>
              <option value="">Select an assignment</option>
              {assignments.map((assignment, index) => (
                <option key={index} value={assignment.assignmentID}>
                  {assignment.assignmentID} - Due: {new Date(assignment.deadline).toLocaleDateString()}
                </option>
              ))}
            </select>

            <button className='assgn' onClick={openAssignment}>Open Assignment</button>
          </div>
        )}

        <h2>Upcoming Deadlines</h2>
        <table>
          <thead>
            <tr>
              <th>Assignment ID</th>
              <th>Upcoming Deadline</th>
            </tr>
          </thead>
          <tbody>
            {deadlines.map((deadline, index) => (
              <tr key={index}>
                <td>{deadline.assignment_id}</td>
                <td>{deadline.deadline}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div class="right-pane">
    {stats.length > 0 && (
        <Bar data={interactiveChartData} options={chartOptions} />
    )}
    {isPieDataReady && (
        <div  style={{ height: '90%', width: '90%', paddingTop: "20px" }}>
            <Pie data={pieData} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>
    )}
    <button onClick={handleFeedbackClick}>Submit Feedback</button>
    {showFeedbackForm && (
        <div class="feedback-form-container">
            <textarea
                placeholder="Type your feedback here..."
                value={feedbackText}
                onChange={(e) => setFeedbackText(e.target.value)}
            />
            <button onClick={handleFeedbackSubmit}>Submit</button>
        </div>
    )}
</div>

    </div>
  </div>
);
}

export default CourseSelectPage;