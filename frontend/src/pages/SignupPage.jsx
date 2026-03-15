import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { registerUser } from '../services/api'

export default function SignupPage() {
  const [searchParams] = useSearchParams()
  const defaultRole = searchParams.get('role') === 'recruiter' ? 'recruiter' : 'job_seeker'

  const [form, setForm] = useState({ email: '', password: '', password2: '', role: defaultRole, phone: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password !== form.password2) { setError('Passwords do not match.'); return }
    setLoading(true)
    setError('')
    try {
      const data = await registerUser(form)
      login(data.user, data.access, data.refresh)
      navigate(data.user.role === 'recruiter' ? '/dashboard/recruiter' : '/dashboard/seeker')
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4 py-12">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 right-1/3 w-96 h-96 bg-blue-600/15 rounded-full blur-3xl" />
        <div className="absolute bottom-1/3 left-1/4 w-96 h-96 bg-purple-600/15 rounded-full blur-3xl" />
      </div>

      <div className="relative w-full max-w-md">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center text-sm font-bold">AI</div>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">ResumeAI</span>
          </Link>
          <h1 className="text-3xl font-bold text-white">Create your account</h1>
          <p className="text-gray-400 mt-2">Start your AI-powered job journey today</p>
        </div>

        <div className="bg-white/3 border border-white/8 rounded-2xl p-8">
          {/* Role toggle */}
          <div className="flex gap-2 p-1 bg-white/5 rounded-xl mb-6">
            {['job_seeker', 'recruiter'].map(r => (
              <button key={r} type="button"
                id={`role-${r}`}
                onClick={() => setForm({ ...form, role: r })}
                className={`flex-1 py-2 rounded-lg text-sm font-medium transition ${form.role === r ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white' : 'text-gray-400 hover:text-white'}`}>
                {r === 'job_seeker' ? '🎯 Job Seeker' : '👔 Recruiter'}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm">{error}</div>
            )}
            <div>
              <label className="block text-sm text-gray-400 mb-2">Email address</label>
              <input id="signup-email" type="email" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })}
                required placeholder="you@example.com"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Phone (optional)</label>
              <input id="signup-phone" type="tel" value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })}
                placeholder="+91 9876543210"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Password</label>
              <input id="signup-password" type="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })}
                required placeholder="Min. 8 characters"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-2">Confirm Password</label>
              <input id="signup-confirm" type="password" value={form.password2} onChange={e => setForm({ ...form, password2: e.target.value })}
                required placeholder="Repeat password"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition" />
            </div>
            <button id="signup-submit" type="submit" disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl font-semibold hover:opacity-90 transition disabled:opacity-50 flex items-center justify-center gap-2 mt-2">
              {loading ? <span className="animate-spin border-2 border-white border-t-transparent rounded-full w-5 h-5" /> : 'Create Account'}
            </button>
          </form>
          <p className="text-center text-gray-500 mt-5 text-sm">
            Already have an account?{' '}
            <Link to="/login" className="text-purple-400 hover:text-purple-300 font-medium">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
