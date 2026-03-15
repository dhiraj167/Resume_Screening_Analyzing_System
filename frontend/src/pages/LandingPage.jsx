import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LandingPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const handleGetStarted = () => {
    if (user) {
      navigate(user.role === 'recruiter' ? '/dashboard/recruiter' : '/dashboard/seeker')
    } else {
      navigate('/signup')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white overflow-hidden">
      {/* Nav */}
      <nav className="fixed top-0 w-full z-50 bg-gray-950/80 backdrop-blur-md border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center">
              <span className="text-sm font-bold">AI</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              ResumeAI
            </span>
          </div>
          <div className="flex gap-4">
            {user ? (
              <button onClick={handleGetStarted}
                className="px-5 py-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full text-sm font-medium hover:opacity-90 transition">
                Dashboard
              </button>
            ) : (
              <>
                <Link to="/login" className="px-5 py-2 text-gray-300 hover:text-white transition text-sm">Login</Link>
                <Link to="/signup" className="px-5 py-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full text-sm font-medium hover:opacity-90 transition">
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero */}
      <div className="relative pt-32 pb-20 px-6">
        {/* Gradient orbs */}
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-40 right-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-full text-purple-400 text-sm mb-8">
            <span className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></span>
            AI-Powered Resume Intelligence
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold leading-tight mb-6">
            Land Your{' '}
            <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
              Dream Job
            </span>{' '}
            With AI
          </h1>
          <p className="text-lg md:text-xl text-gray-400 max-w-3xl mx-auto mb-12">
            Upload your resume. Get an instant score, ATS analysis, skill gap insights, and AI-matched job recommendations — all powered by NLP and semantic similarity.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button onClick={handleGetStarted}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl text-lg font-semibold hover:scale-105 transition-transform shadow-2xl shadow-purple-500/25">
              🚀 Start Free — Analyze Your Resume
            </button>
            <Link to="/signup?role=recruiter"
              className="px-8 py-4 bg-white/5 border border-white/10 rounded-2xl text-lg font-semibold hover:bg-white/10 transition">
              👔 I'm a Recruiter
            </Link>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center mb-4">Everything You Need to Get Hired</h2>
        <p className="text-gray-400 text-center mb-16">Two powerful portals. One intelligent platform.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { icon: '📄', title: 'Resume Analysis', desc: 'Get a score out of 100, ATS compatibility check, and actionable improvement suggestions.', color: 'purple' },
            { icon: '🎯', title: 'Job Matching', desc: 'AI matches your resume to the best jobs using sentence transformer embeddings and cosine similarity.', color: 'blue' },
            { icon: '📚', title: 'Skill Gap Learning', desc: 'Identify missing skills and get curated YouTube, Coursera, and GitHub learning resources.', color: 'pink' },
            { icon: '👥', title: 'Bulk Screening', desc: 'Recruiters upload hundreds of resumes. AI ranks candidates by match score instantly.', color: 'green' },
            { icon: '✉️', title: 'Auto Rejection Emails', desc: 'Automatically send personalized rejection emails with skill gap reasons to unqualified candidates.', color: 'orange' },
            { icon: '📊', title: 'Recruiter Analytics', desc: 'Dashboard with applicant stats, top candidates, skill demand distribution, and hiring insights.', color: 'teal' },
          ].map((f, i) => (
            <div key={i} className="p-6 bg-white/3 border border-white/8 rounded-2xl hover:border-purple-500/30 hover:bg-white/5 transition-all group">
              <div className="text-4xl mb-4">{f.icon}</div>
              <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Tech Stack */}
      <div className="border-t border-white/5 py-16 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <p className="text-gray-500 text-sm mb-8">POWERED BY</p>
          <div className="flex flex-wrap justify-center gap-6 text-gray-400 text-sm">
            {['spaCy NLP', 'all-MiniLM-L6-v2', 'Cosine Similarity', 'Django REST', 'React', 'Sentence Transformers'].map((t) => (
              <span key={t} className="px-4 py-2 bg-white/5 rounded-full border border-white/10">{t}</span>
            ))}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="max-w-4xl mx-auto px-6 py-20 text-center">
        <div className="p-12 bg-gradient-to-br from-purple-900/40 to-blue-900/40 border border-purple-500/20 rounded-3xl">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to supercharge your job search?</h2>
          <p className="text-gray-400 mb-8">Join thousands of candidates who found their dream jobs using AI.</p>
          <button onClick={handleGetStarted}
            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl text-lg font-semibold hover:scale-105 transition-transform">
            Get Started for Free →
          </button>
        </div>
      </div>

      <footer className="border-t border-white/5 py-8 text-center text-gray-500 text-sm">
        © 2026 ResumeAI. Built with ❤️ and AI.
      </footer>
    </div>
  )
}
