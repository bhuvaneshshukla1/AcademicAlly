import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Grade() {
  const navigate = useNavigate();
  const [responses, setResponses] = useState([]);
  const [grades, setGrades] = useState({});

  useEffect(() => {
    const submissionID = localStorage.getItem('submissionID');  // Retrieve the submissionID from local storage
    const assignmentID = localStorage.getItem('assignmentID');
    if (submissionID) {
      axios.post('http://35.208.243.254:8080/get_subj_responses', { submissionID: submissionID, assignmentID: assignmentID })
        .then(response => {
          setResponses(response.data.responses);
          const initialGrades = {};
          response.data.responses.forEach(item => {
            initialGrades[item.question_id] = ''; // Initialize with empty grade fields
          });
          setGrades(initialGrades);
        })
        .catch(error => console.error('Failed to fetch submission details:', error));
    } else {
      console.error('No submission ID found in local storage');
      // Optionally navigate back or handle the lack of ID appropriately
    }
  }, []);

 const handleGradeChange = (questionID, value) => {
  const newValue = value === '' ? '' : Number(value); // Convert to number if not empty, else keep as empty string
  setGrades(prevGrades => ({
    ...prevGrades,
    [questionID]: newValue
  }));
};


  const handleSubmit = () => {
    const gradesArray = Object.keys(grades).map(questionID => ({
      questionID,
       marks: parseInt(grades[questionID], 10)
    }));
	const validGrades = gradesArray.filter(grade => !isNaN(grade.marks));
    axios.post('http://35.208.243.254:8080/post_grades', { submissionID: localStorage.getItem('submissionID'), grades: validGrades })
      .then(() => {
        alert('Grades submitted successfully.');
        navigate('/faculty');  // Navigate back to the faculty page
      })
      .catch(error => console.error('Failed to submit grades:', error));
  };

 return (
  <div>
    <h1>Grade Submissions</h1>
    {responses.map((response, index) => (
      <div key={index}>
        <h3>{response.question_text}</h3>
        <p>{response.response_text}</p>
<input
  type="number"
  placeholder="Enter marks"
  value={grades[response.question_id] !== undefined ? grades[response.question_id] : ''}
  onChange={(e) => handleGradeChange(response.question_id, e.target.value)}
/>

      </div>
    ))}
    <button onClick={handleSubmit}>Submit Grades</button>
  </div>
);
}

export default Grade;