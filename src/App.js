// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import PlantDashboard from './page/dashboard';
import Header from './page/nav';
import PlantForm from './page/PlantForm';
import History from './page/History';
import MyComponent from './page/test';

export default function App() {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<PlantDashboard />} />
                <Route path="/update" element={<PlantForm class_ />} />
                <Route path="/dashboard" element={<PlantDashboard class_ />} />
                <Route path="/history" element={<History class_ />} />

                <Route path="/test" element={<MyComponent class_ />} />
            </Routes>
        </Router>
    );
}
