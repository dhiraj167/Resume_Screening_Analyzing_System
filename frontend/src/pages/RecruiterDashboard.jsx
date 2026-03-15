import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { getRecruiterJobs, createJob, updateJob, deleteJob, screenCandidates, getRecruiterAnalytics, clearRecruiterAnalytics } from '../services/api'

const SidebarItem = ({ icon, label, active, onClick }) => (
  <button onClick={onClick}
    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${active ? 'bg-purple-600/20 text-purple-300 border border-purple-500/20' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
    <span className="text-xl">{icon}</span>{label}
  </button>
)

const StatCard = ({ icon, label, value, color = 'purple' }) => (
  <div className="p-5 bg-white/3 border border-white/8 rounded-2xl">
    <div className="text-3xl mb-2">{icon}</div>
    <p className="text-2xl font-bold text-white">{value}</p>
    <p className="text-xs text-gray-400 mt-1">{label}</p>
  </div>
)

export default function RecruiterDashboard() {
  const { user, logout } = useAuth()
  const [activeTab, setActiveTab] = useState('jobs')
  const [jobs, setJobs] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [screenResults, setScreenResults] = useState(null)
  const [showJobForm, setShowJobForm] = useState(false)
  const [editJob, setEditJob] = useState(null)
  const [screening, setScreening] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [selectedJobId, setSelectedJobId] = useState('')
  const [analyticsJobId, setAnalyticsJobId] = useState('')
  const [threshold, setThreshold] = useState(70)
  const filesRef = useRef()

  const [jobForm, setJobForm] = useState({
    title: '', company: '', description: '', required_skills: '',
    experience_required: '', salary: '', location: '', job_type: 'Full-time'
  })

  useEffect(() => { loadJobs() }, [])

  const loadJobs = async () => {
    setLoading(true)
    try { const j = await getRecruiterJobs(); setJobs(j.results || j) } catch {}
    setLoading(false)
  }

  const loadAnalytics = async (jobId = null) => {
    setLoading(true)
    try { setAnalytics(await getRecruiterAnalytics(jobId)) } catch {}
    setLoading(false)
  }

  const handleTabClick = (tab) => {
    setActiveTab(tab)
    if (tab === 'analytics') loadAnalytics(analyticsJobId)
  }

  const handleClearAnalytics = async () => {
    if (!confirm(analyticsJobId ? 'Are you sure you want to clear all analytics for this specific job? This cannot be undone.' : 'Are you sure you want to clear ALL screening analytics? This cannot be undone.')) return
    
    setLoading(true)
    try {
      const res = await clearRecruiterAnalytics(analyticsJobId)
      setSuccess(res.message || 'Analytics cleared successfully.')
      await loadAnalytics(analyticsJobId)
    } catch (e) {
      setError(e.message)
    }
    setLoading(false)
  }

  const handleJobSubmit = async (e) => {
    e.preventDefault()
    setError(''); setSuccess('')
    const payload = {
      ...jobForm,
      required_skills: jobForm.required_skills.split(',').map(s => s.trim()).filter(Boolean)
    }
    try {
      if (editJob) { await updateJob(editJob.id, payload) } else { await createJob(payload) }
      setSuccess(editJob ? 'Job updated!' : 'Job posted successfully!')
      setShowJobForm(false); setEditJob(null)
      setJobForm({ title: '', company: '', description: '', required_skills: '', experience_required: '', salary: '', location: '', job_type: 'Full-time' })
      await loadJobs()
    } catch (e) { setError(e.message) }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this job?')) return
    try { await deleteJob(id); await loadJobs() } catch (e) { setError(e.message) }
  }

  const handleScreening = async () => {
    const files = filesRef.current?.files
    if (!files?.length) { setError('Please select resume files.'); return }
    if (!selectedJobId) { setError('Select a job to screen against.'); return }
    setScreening(true); setError(''); setScreenResults(null)
    const fd = new FormData()
    fd.append('job_id', selectedJobId)
    fd.append('threshold', threshold)
    Array.from(files).forEach(f => fd.append('resumes', f))
    try {
      const res = await screenCandidates(fd)
      setScreenResults(res)
      setSuccess(`Screened ${res.total_screened} candidates!`)
    } catch (e) { setError(e.message) }
    setScreening(false)
  }

  return (
    <div className="min-h-screen bg-gray-950 flex text-white">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900/60 border-r border-white/5 flex flex-col">
        <div className="p-6 border-b border-white/5">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xs font-bold">AI</div>
            <span className="font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">ResumeAI</span>
          </div>
          <p className="text-xs text-gray-500 mt-1">Recruiter Portal</p>
        </div>
        <div className="flex-1 p-4 space-y-1">
          <SidebarItem icon="💼" label="My Jobs" active={activeTab==='jobs'} onClick={() => setActiveTab('jobs')} />
          <SidebarItem icon="🔍" label="Screen Candidates" active={activeTab==='screen'} onClick={() => setActiveTab('screen')} />
          <SidebarItem icon="📊" label="Analytics" active={activeTab==='analytics'} onClick={() => handleTabClick('analytics')} />
        </div>
        <div className="p-4 border-t border-white/5">
          <div className="px-4 py-3 bg-white/3 rounded-xl mb-3">
            <p className="text-sm font-medium truncate">{user?.email}</p>
            <p className="text-xs text-gray-400">Recruiter</p>
          </div>
          <button onClick={logout} className="w-full text-sm text-red-400 hover:text-red-300 py-2 transition text-left px-4">→ Logout</button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 p-8 overflow-auto">
        {error && <div className="mb-4 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm">{error}</div>}
        {success && <div className="mb-4 p-4 bg-green-500/10 border border-green-500/20 rounded-xl text-green-400 text-sm">{success}</div>}

        {/* JOBS TAB */}
        {activeTab === 'jobs' && (
          <div className="max-w-3xl">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold">My Job Postings</h1>
                <p className="text-gray-400 text-sm mt-1">{jobs.length} job(s) posted</p>
              </div>
              <button id="post-job-btn" onClick={() => { setEditJob(null); setShowJobForm(!showJobForm) }}
                className="px-5 py-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl text-sm font-medium hover:opacity-90 transition">
                + Post New Job
              </button>
            </div>

            {/* Job Form */}
            {showJobForm && (
              <div className="p-6 bg-white/3 border border-white/8 rounded-2xl mb-6">
                <h2 className="font-semibold mb-5">{editJob ? 'Edit Job' : 'Post a New Job'}</h2>
                <form onSubmit={handleJobSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[
                    ['title', 'Job Title *', 'e.g. Data Scientist'],
                    ['company', 'Company *', 'e.g. Acme Corp'],
                    ['location', 'Location', 'e.g. Bangalore / Remote'],
                    ['salary', 'Salary', 'e.g. ₹8-12 LPA'],
                    ['experience_required', 'Experience', 'e.g. 2-4 years'],
                    ['job_type', 'Job Type', 'Full-time'],
                  ].map(([field, label, placeholder]) => (
                    <div key={field}>
                      <label className="block text-xs text-gray-400 mb-1">{label}</label>
                      <input id={`job-form-${field}`} value={jobForm[field]} onChange={e => setJobForm({ ...jobForm, [field]: e.target.value })}
                        placeholder={placeholder} required={['title', 'company'].includes(field)}
                        className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition" />
                    </div>
                  ))}
                  <div className="col-span-2">
                    <label className="block text-xs text-gray-400 mb-1">Required Skills (comma-separated) *</label>
                    <input id="job-form-skills" value={jobForm.required_skills} onChange={e => setJobForm({ ...jobForm, required_skills: e.target.value })}
                      placeholder="Python, Machine Learning, SQL, TensorFlow"
                      className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition" />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-xs text-gray-400 mb-1">Job Description *</label>
                    <textarea id="job-form-desc" value={jobForm.description} onChange={e => setJobForm({ ...jobForm, description: e.target.value })}
                      rows={4} required placeholder="Describe the role, responsibilities, and requirements…"
                      className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-gray-600 focus:outline-none focus:border-purple-500 transition resize-none" />
                  </div>
                  <div className="col-span-2 flex gap-3">
                    <button type="submit" className="px-6 py-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl text-sm font-medium hover:opacity-90 transition">
                      {editJob ? 'Update Job' : 'Post Job'}
                    </button>
                    <button type="button" onClick={() => setShowJobForm(false)}
                      className="px-6 py-2 bg-white/5 rounded-xl text-sm hover:bg-white/10 transition">Cancel</button>
                  </div>
                </form>
              </div>
            )}

            {loading ? (
              <div className="flex justify-center py-16"><div className="animate-spin border-4 border-purple-500 border-t-transparent rounded-full w-10 h-10" /></div>
            ) : jobs.length === 0 ? (
              <p className="text-gray-400 text-center py-16">No jobs posted yet. Create your first job above!</p>
            ) : (
              <div className="space-y-4">
                {jobs.map(job => (
                  <div key={job.id} className="p-5 bg-white/3 border border-white/8 rounded-2xl">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="font-semibold">{job.title}</h3>
                        <p className="text-sm text-gray-400">{job.company} • {job.location} • {job.job_type}</p>
                      </div>
                      <div className="flex gap-2">
                        <span className="text-xs text-gray-400 bg-white/5 px-2 py-1 rounded-lg">{job.applicant_count || 0} apps</span>
                        <button onClick={() => { setEditJob(job); setJobForm({ ...job, required_skills: (job.required_skills || []).join(', ') }); setShowJobForm(true) }}
                          className="text-xs text-blue-400 hover:text-blue-300 transition">Edit</button>
                        <button onClick={() => handleDelete(job.id)} className="text-xs text-red-400 hover:text-red-300 transition">Delete</button>
                      </div>
                    </div>
                    <p className="text-sm text-gray-400 line-clamp-2 mb-2">{job.description}</p>
                    <div className="flex flex-wrap gap-1">
                      {job.required_skills?.map(s => <span key={s} className="px-2 py-0.5 bg-purple-500/15 text-purple-300 rounded-full text-xs">{s}</span>)}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* SCREEN TAB */}
        {activeTab === 'screen' && (
          <div className="max-w-3xl">
            <h1 className="text-2xl font-bold mb-2">Screen Candidates</h1>
            <p className="text-gray-400 mb-8">Upload multiple resumes. AI ranks them instantly.</p>
            <div className="p-6 bg-white/3 border border-white/8 rounded-2xl mb-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Select Job</label>
                  <select id="screen-job-select" value={selectedJobId} onChange={e => setSelectedJobId(e.target.value)}
                    className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-xl text-sm text-white focus:outline-none focus:border-purple-500 transition">
                    <option value="" className="bg-gray-900 text-white">-- Choose a job --</option>
                    {jobs.map(j => <option key={j.id} value={j.id} className="bg-gray-900 text-white">{j.title}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Match Threshold: {threshold}%</label>
                  <input id="screen-threshold" type="range" min="10" max="95" step="5" value={threshold}
                    onChange={e => setThreshold(Number(e.target.value))}
                    className="w-full accent-purple-500" />
                </div>
              </div>
              <div className="border-2 border-dashed border-white/10 rounded-xl p-8 text-center mb-4 hover:border-purple-500/40 transition cursor-pointer"
                onClick={() => filesRef.current?.click()}>
                <input id="screen-files-input" ref={filesRef} type="file" multiple accept=".pdf,.docx,.doc,.txt" className="hidden" />
                <p className="text-3xl mb-2">📂</p>
                <p className="text-sm text-gray-400">Click to upload multiple resume files (PDF/DOCX/TXT)</p>
              </div>
              <button id="screen-submit-btn" onClick={handleScreening} disabled={screening}
                className="w-full py-3 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl font-medium hover:opacity-90 transition disabled:opacity-50 flex items-center justify-center gap-2">
                {screening ? <><span className="animate-spin border-2 border-white border-t-transparent rounded-full w-5 h-5" /> Analyzing...</> : '🤖 Screen & Rank Candidates'}
              </button>
            </div>

            {/* Results */}
            {screenResults && (
              <div>
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <StatCard icon="👥" label="Total Screened" value={screenResults.total_screened} />
                  <StatCard icon="✅" label="Shortlisted" value={screenResults.shortlisted_count} />
                  <StatCard icon="❌" label="Rejected" value={screenResults.rejected_count} />
                </div>
                <div className="space-y-3">
                  {screenResults.candidates?.map((c, i) => (
                    <div key={i} className={`p-5 rounded-2xl border ${c.status === 'shortlisted' ? 'bg-green-500/5 border-green-500/20' : 'bg-red-500/5 border-red-500/10'}`}>
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <p className="font-medium">{c.name} <span className="text-xs text-gray-400">— {c.filename}</span></p>
                          <p className="text-xs text-gray-400">{c.email}</p>
                        </div>
                        <div className="text-right">
                          <p className={`text-lg font-bold ${c.status === 'shortlisted' ? 'text-green-400' : 'text-red-400'}`}>
                            {c.match_score?.toFixed(1)}%
                          </p>
                          <span className={`text-xs px-2 py-0.5 rounded-full ${c.status === 'shortlisted' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
                            {c.status}
                          </span>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {c.matched_skills?.slice(0, 5).map(s => <span key={s} className="px-2 py-0.5 bg-green-500/15 text-green-400 rounded-full text-xs">✓ {s}</span>)}
                        {c.missing_skills?.slice(0, 3).map(s => <span key={s} className="px-2 py-0.5 bg-red-500/15 text-red-400 rounded-full text-xs">✗ {s}</span>)}
                      </div>
                      {c.rejection_email_sent && <p className="text-xs text-gray-500 mt-2">✉️ Rejection email sent</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ANALYTICS TAB */}
        {activeTab === 'analytics' && (
          <div className="max-w-4xl">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-2xl font-bold">Recruiter Analytics</h1>
              <div className="flex items-center gap-3">
                <select 
                  value={analyticsJobId} 
                  onChange={e => {
                    setAnalyticsJobId(e.target.value)
                    loadAnalytics(e.target.value)
                  }}
                  className="px-3 py-2 bg-white/5 border border-white/10 rounded-xl text-sm text-white focus:outline-none focus:border-purple-500 transition min-w-[200px]"
                >
                  <option value="" className="bg-gray-900 text-white">All Jobs (Aggregate)</option>
                  {jobs.map(j => <option key={j.id} value={j.id} className="bg-gray-900 text-white">{j.title}</option>)}
                </select>
                <button 
                  onClick={handleClearAnalytics}
                  className="px-4 py-2 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl text-sm hover:bg-red-500/20 transition"
                  title="Delete all screening history"
                >
                  Clear Analytics
                </button>
              </div>
            </div>
            
            {loading ? (
              <div className="flex justify-center py-20"><div className="animate-spin border-4 border-purple-500 border-t-transparent rounded-full w-10 h-10" /></div>
            ) : analytics ? (
              <>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                  <StatCard icon="💼" label="Total Jobs" value={analytics.total_jobs} />
                  <StatCard icon="🟢" label="Active Jobs" value={analytics.active_jobs} />
                  <StatCard icon="👥" label="Applicants" value={analytics.total_applicants} />
                  <StatCard icon="📈" label="Avg. Match Score" value={`${analytics.average_match_score}%`} />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  {/* Status breakdown */}
                  <div className="p-5 bg-white/3 border border-white/8 rounded-2xl">
                    <h2 className="font-semibold mb-4">Application Status</h2>
                    {Object.entries(analytics.status_breakdown || {}).map(([key, val]) => (
                      <div key={key} className="flex items-center justify-between mb-3">
                        <span className="text-sm capitalize text-gray-300">{key}</span>
                        <div className="flex items-center gap-3">
                          <div className="h-2 bg-white/5 rounded-full w-32 overflow-hidden">
                            <div className="h-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full"
                              style={{ width: `${analytics.total_applicants ? (val / analytics.total_applicants) * 100 : 0}%` }} />
                          </div>
                          <span className="text-sm text-white font-medium w-6">{val}</span>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Top skills */}
                  <div className="p-5 bg-white/3 border border-white/8 rounded-2xl">
                    <h2 className="font-semibold mb-4">Top Skills in Applicants</h2>
                    {analytics.top_skills_in_demand?.length === 0 && <p className="text-gray-400 text-sm">No data yet.</p>}
                    {analytics.top_skills_in_demand?.map((s, i) => (
                      <div key={i} className="flex items-center justify-between mb-2">
                        <span className="text-sm text-gray-300 capitalize">{s.skill}</span>
                        <span className="text-sm text-purple-400 font-medium">{s.count}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Top candidates */}
                <div className="p-5 bg-white/3 border border-white/8 rounded-2xl">
                  <h2 className="font-semibold mb-4">Top Candidates</h2>
                  {analytics.top_candidates?.length === 0 && <p className="text-gray-400 text-sm">No candidates yet.</p>}
                  <div className="space-y-3">
                    {analytics.top_candidates?.map((c, i) => (
                      <div key={c.id} className="flex items-center justify-between p-3 bg-white/3 rounded-xl">
                        <div className="flex items-center gap-3">
                          <span className="w-7 h-7 bg-gradient-to-br from-purple-600 to-blue-600 rounded-full flex items-center justify-center text-xs font-bold">#{i+1}</span>
                          <div>
                            <p className="text-sm font-medium">{c.candidate_name}</p>
                            <p className="text-xs text-gray-400">{c.job_title}</p>
                          </div>
                        </div>
                        <span className="text-sm font-bold text-green-400">{c.match_score?.toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            ) : (
              <p className="text-gray-400 text-center py-20">No analytics data available yet.</p>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
