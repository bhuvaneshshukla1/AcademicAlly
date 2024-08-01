import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import "./CreateAssignment.css";

function CreateAssignment() {
  const navigate = useNavigate();
  const [deadline, setDeadline] = useState('');
  const [questions, setQuestions] = useState([]);

  const addQuestion = () => {
    setQuestions([...questions, {
      topic: '',
      questionText: '',
      options: ['', '', '', ''],
      correctOption: '',
      assumedDifficulty: 'E'  // Default difficulty is set to 'Easy'
    }]);
  };

  const handleTopicChange = (index, value) => {
    const newQuestions = [...questions];
    newQuestions[index].topic = value;
    setQuestions(newQuestions);
  };

  const handleQuestionChange = (index, value) => {
    const newQuestions = [...questions];
    newQuestions[index].questionText = value;
    setQuestions(newQuestions);
  };

  const handleOptionChange = (questionIndex, optionIndex, value) => {
    const newQuestions = [...questions];
    newQuestions[questionIndex].options[optionIndex] = value;
    setQuestions(newQuestions);
  };

  const handleCorrectOptionChange = (index, value) => {
    const newQuestions = [...questions];
    newQuestions[index].correctOption = value;
    setQuestions(newQuestions);
  };

  const handleDifficultyChange = (index, value) => {
    const newQuestions = [...questions];
    newQuestions[index].assumedDifficulty = value;
    setQuestions(newQuestions);
  };

  const handleDeleteQuestion = (index) => {
    setQuestions(questions.filter((_, i) => i !== index));
  };

  const handleSubmit = () => {
    const courseID = localStorage.getItem('courseID');
    if (!courseID) {
      alert('Course ID is not set. Please select a course first.');
      navigate('/faculty');
      return;
    }

    // Append "T00:00:00" to the deadline date to form a full datetime string
    const formattedDeadline = `${deadline}T00:00:00`;

    axios.post('http://35.208.243.254:8080/create_assignment', {
      courseID,
      deadline: formattedDeadline,  // Use the formatted deadline
      questions,
    }).then(() => {
      alert('Assignment created successfully!');
      navigate('/faculty');
    }).catch(error => {
      console.error('Error creating assignment:', error);
      alert('Failed to create assignment.');
    });
  };

  return (
    <div className='cont'>
      <h1>Create Assignment</h1>
      <div>
        <label className='deadline'>Set a deadline for the assignment:</label>
        <input className='date-input'
          type="date"
          value={deadline}
          onChange={e => setDeadline(e.target.value)}
        />
      </div>

      {questions.map((question, index) => (
        <div className='font-s' key={index}>
          <h3>Enter question {index + 1}</h3>
          <input
            type="text"
            placeholder="Enter topic"
            value={question.topic}
            onChange={e => handleTopicChange(index, e.target.value)}
          />
          <input
            type="text"
            placeholder="Enter question"
            value={question.questionText}
            onChange={e => handleQuestionChange(index, e.target.value)}
          />

          {question.options.map((option, idx) => (
            <input
              key={idx}
              type="text"
              placeholder={`Option ${idx + 1}`}
              value={option}
              onChange={e => handleOptionChange(index, idx, e.target.value)}
            />
          ))}

          <input
            type="text"
            placeholder="Correct option"
            value={question.correctOption}
            onChange={e => handleCorrectOptionChange(index, e.target.value)}
          />

          <h4>Set the assumed difficulty of the question</h4>
          <select
            value={question.assumedDifficulty}
            onChange={e => handleDifficultyChange(index, e.target.value)}
          >
            <option value="E">Easy</option>
            <option value="M">Medium</option>
            <option value="H">Hard</option>
          </select>

          <div className="delete-container">
            <button onClick={() => handleDeleteQuestion(index)}>Delete Question</button>
          </div>
        </div>
      ))}

      <div className="action-buttons">
        <button onClick={addQuestion}>Add Question</button>
        <button onClick={handleSubmit}>Create</button>
      </div>
    </div>
  );
}

export default CreateAssignment;
