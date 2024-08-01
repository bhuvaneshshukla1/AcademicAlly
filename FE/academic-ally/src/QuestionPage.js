// QuestionPage.js
import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Question.css';

function QuestionPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const username = localStorage.getItem('username');
    const assignmentID = localStorage.getItem('assignmentID');
    const [questions, setQuestions] = useState([]);
    const [responses, setResponses] = useState({});
    // const [response_val,set_res] = useState("");

    useEffect(() => {
        const fetchQuestions = async () => {
            try {
		console.log(assignmentID)
                const response = await axios.post('http://35.208.243.254:8080/questions', {
                    assignmentID: assignmentID
                });
                setQuestions(response.data.questions);
            } catch (error) {
                console.error("Failed to fetch questions:", error);
                setQuestions([]);
            }
        };
        fetchQuestions();
    }, [assignmentID]);

    const handleOptionChange = (questionId, option) => {
        setResponses(prev => ({ ...prev, [questionId]: option }));
    };

    const handleSubmit = async () => {
	const submittedResponses = questions.map((question) => {  // Make sure to use (question) to define scope
        // const response = responses[question.question_id];
        // if(response){
        //     set_res(question.question_type === "O" ? response[1] : response);
            
        // }
        // else{
        //     set_res(question.question_type === "O" ? 'Z' : "");
        // }
        
       // const response = responses[question.question_id] ?  responses[question.question_id][1] : (question.question_type === "O" ? 'Z' : "");
	const response = responses[question.question_id] ?  (question.question_type === "O" ? responses[question.question_id][1] : responses[question.question_id]) : (question.question_type === "O" ? 'Z' : "");


        return {
            questionID: question.question_id,
            response: response, // Use the question variable that's now defined in the map function's scope
            questionType: question.question_type  // This also uses the defined question
        };
    });

        const data = {
            studentID: username,
            assignmentID: assignmentID,
            responses: submittedResponses
        };
        try {
            const response2 = await axios.post('http://35.208.243.254:8080/submissions', data);
	    localStorage.removeItem('assignmentID');
        console.log(response2.data.message);
        if(response2.data.message === 'Deadline Passed.'){
            alert('Cannot Submit - Deadline passed');
        }
        else{
            alert('Assignment submitted successfully.');
        }
            
            navigate('/select-course'); // Redirect back or to another page
        } catch (error) {
            console.error("Failed to submit assignment:", error);
        }
    };

    return (
        <div className='container'>
            <h1 className="q-title">Questions for Assignment {assignmentID}</h1>
            <div className='qa-container'>
                {questions.map((question, index) => (
                    <div key={question.question_id} className="question-container">
                        <p className="question-text">{index + 1}. {question.question_text}</p>
                        <div className="options-container">
                            {question.question_type === "O" ? (
                                question.options.map((option, idx) => (
                                    <label key={idx}>
                                        <input
                                            type="radio"
                                            name={question.question_id}
                                            value={option}
                                            checked={responses[question.question_id] === option}
                                            onChange={() => handleOptionChange(question.question_id, option)}
                                        />
                                        {option}
                                    </label>
                                ))
                            ) : (
                                <textarea
                                    value={responses[question.question_id] || ''}
                                    onChange={(e) => handleOptionChange(question.question_id, e.target.value)}
                                    rows="3"
                                />
                            )}
                        </div>
                    </div>
                ))}
                <button onClick={handleSubmit} className="submit-button">Submit Assignment</button>
            </div>
        </div>
    );
    
    
}

export default QuestionPage;