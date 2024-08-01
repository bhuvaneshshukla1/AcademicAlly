import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://35.208.243.254:8080/login', {
                username,
                password
            }, { withCredentials: false });

            if (response.status === 200) {
                // Store username in local storage
                localStorage.setItem('username', username);

                // Determine role based on ID prefix
                const prefix = username.substring(0, 3).toUpperCase();
                if (prefix === "SID") {
                    // Student
                    navigate('/select-course', { state: { username } });
                } else {
                    // Faculty or unknown
                    navigate('/Faculty', { state: { username } });
                }
            } else {
                alert("Login successful, but no courses found.");
            }
        } catch (error) {
            alert('Login failed!');
            console.error(error);
        }
    };

    return (
        <form onSubmit={handleLogin}>
            <p className='page-title'><center>AcademicAlly</center></p>
            <input type="text" value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
            <button className='login_button' type="submit">Login</button>
        </form>
    );
}

export default LoginPage;
