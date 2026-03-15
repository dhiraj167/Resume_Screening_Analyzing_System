import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import JobSeekerDashboard from './pages/JobSeekerDashboard'
import RecruiterDashboard from './pages/RecruiterDashboard'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route
            path="/dashboard/seeker/*"
            element={<ProtectedRoute role="job_seeker"><JobSeekerDashboard /></ProtectedRoute>}
          />
          <Route
            path="/dashboard/recruiter/*"
            element={<ProtectedRoute role="recruiter"><RecruiterDashboard /></ProtectedRoute>}
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
