import {
    BrowserRouter as Router,
    Routes,
    Route,
    Navigate,
} from 'react-router-dom';
import PlantDashboard from './page/dashboard';
import Header from './page/nav';
import PlantForm from './page/PlantForm';
import History from './page/History';
// import Login from './page/login';
// import Register from './page/register';

export default function App() {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" element={<PlantDashboard />} />
                <Route path="/update" element={<PlantForm />} />
                <Route path="/dashboard" element={<PlantDashboard />} />
                <Route path="/history" element={<History />} />
                <Route path="*" element={<Navigate to="/dashboard" />} />

                {/* <Route
                            path="/login"
                            element={<Login onLogin={login} />}
                        />
                        <Route path="/register" element={<Register />} /> */}
            </Routes>
        </Router>
    );
}
