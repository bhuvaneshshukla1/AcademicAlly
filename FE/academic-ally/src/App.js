import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import CourseSelectPage from './CourseSelectPage';
import QuestionPage from './QuestionPage';
import Faculty from './Faculty';
import Grading from './Grading';
import Assignment from './CreateAssignment'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/select-course" element={<CourseSelectPage />} />
        <Route path="/questions" element={<QuestionPage />} />
	<Route path="/faculty" element={<Faculty />} />
	<Route path="/gradesubmission" element={<Grading />} />
  <Route path="/createAssignment" element={<Assignment />} />
      </Routes>
    </Router>
  );
}

export default App;