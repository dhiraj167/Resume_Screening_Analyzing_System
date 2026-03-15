import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { uploadResume, getResumes, getResumeAnalysis, getJobRecommendations, getJobs, getSkillGap } from '../services/api'

const ScoreRing = ({ score, size = 80, label }) => {
  const r = size / 2 - 8
  const circumference = 2 * Math.PI * r
  const offset = circumference - (score / 100) * circumference
  const color = score >= 75 ? '#22c55e' : score >= 50 ? '#f59e0b' : '#ef4444'
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size}>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="#ffffff10" strokeWidth="8" />
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circumference} strokeDashoffset={offset}
          strokeLinecap="round" transform={`rotate(-90 ${size/2} ${size/2})`}
          style={{ transition: 'stroke-dashoffset 1s ease' }} />
        <text x="50%" y="54%" textAnchor="middle" fill="white" fontSize="16" fontWeight="bold">{score?.toFixed(0)}</text>
      </svg>
      {label && <span className="text-xs text-gray-400">{label}</span>}
    </div>
  )
}

const SidebarItem = ({ icon, label, active, onClick }) => (
  <button onClick={onClick}
    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${active ? 'bg-purple-600/20 text-purple-300 border border-purple-500/20' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
    <span className="text-xl">{icon}</span>{label}
  </button>
)

export default function JobSeekerDashboard() {
  const { user, logout } = useAuth()
  const [activeTab, setActiveTab] = useState('upload')
  const [resumes, setResumes] = useState([])
  const [selectedResume, setSelectedResume] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [recommendations, setRecommendations] = useState([])
  const [jobs, setJobs] = useState([])
  const [searchQ, setSearchQ] = useState('')
  const [skillGap, setSkillGap] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const fileRef = useRef()

  useEffect(() => { loadResumes() }, [])

  const loadResumes = async () => {
    try { const r = await getResumes(); setResumes(r.results || r) } catch {}
  }

  const handleUpload = async (file) => {
    if (!file) return
    setUploading(true); setError(''); setSuccess('')
    const fd = new FormData(); fd.append('file', file)
    try {
      const res = await uploadResume(fd)
      setSuccess('Resume uploaded and analyzed!')
      setSelectedResume(res.resume)
      setAnalysis(res.resume)
      await loadResumes()
      setActiveTab('analysis')
    } catch (e) { setError(e.message) }
    finally { setUploading(false) }
  }

  const loadAnalysis = async (resumeId) => {
    setLoading(true); setError('')
    try {
      const a = await getResumeAnalysis(resumeId)
      setAnalysis(a)
    } catch (e) { setError(e.message) }
    setLoading(false)
  }

  const loadRecommendations = async () => {
    setLoading(true); setError('')
    try {
      const r = await getJobRecommendations(selectedResume?.id)
      setRecommendations(r.recommendations || [])
    } catch (e) { setError(e.message) }
    setLoading(false)
  }

  const loadJobs = async (q) => {
    setLoading(true)
    try { const j = await getJobs(q); setJobs(j.results || j) } catch {}
    setLoading(false)
  }

  const loadSkillGap = async (jobId) => {
    if (!selectedResume) return
    try {
      const sg = await getSkillGap(selectedResume.id, jobId)
      setSkillGap(sg)
    } catch {}
  }

  const handleTabClick = (tab) => {
    setActiveTab(tab)
    if (tab === 'jobs') loadJobs('')
    if (tab === 'recommendations' && selectedResume) loadRecommendations()
  }

  return (
    <div className="min-h-screen bg-gray-950 flex text-white">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900/60 border-r border-white/5 flex flex-col">
        <div className="p-6 border-b border-white/5">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center text-xs font-bold">AI</div>
            <span className="font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">ResumeAI</span>
          </div>
          <p className="text-xs text-gray-500 mt-1">Job Seeker Portal</p>
        </div>
        <div className="flex-1 p-4 space-y-1">
          <SidebarItem icon="📤" label="Upload Resume" active={activeTab==='upload'} onClick={() => setActiveTab('upload')} />
          <SidebarItem icon="📊" label="My Analysis" active={activeTab==='analysis'} onClick={() => setActiveTab('analysis')} />
          <SidebarItem icon="🎯" label="Job Match" active={activeTab==='recommendations'} onClick={() => handleTabClick('recommendations')} />
          <SidebarItem icon="🔍" label="Browse Jobs" active={activeTab==='jobs'} onClick={() => handleTabClick('jobs')} />
          <SidebarItem icon="📚" label="Skill Gap" active={activeTab==='skillgap'} onClick={() => setActiveTab('skillgap')} />
        </div>
        <div className="p-4 border-t border-white/5">
          <div className="px-4 py-3 bg-white/3 rounded-xl mb-3">
            <p className="text-sm font-medium text-white truncate">{user?.email}</p>
            <p className="text-xs text-gray-400">Job Seeker</p>
          </div>
          <button onClick={logout} className="w-full text-sm text-red-400 hover:text-red-300 py-2 transition text-left px-4">→ Logout</button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 p-8 overflow-auto">
        {error && <div className="mb-4 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 text-sm">{error}</div>}
        {success && <div className="mb-4 p-4 bg-green-500/10 border border-green-500/20 rounded-xl text-green-400 text-sm">{success}</div>}

        {/* UPLOAD TAB */}
        {activeTab === 'upload' && (
          <div className="max-w-2xl">
            <h1 className="text-2xl font-bold mb-2">Upload Your Resume</h1>
            <p className="text-gray-400 mb-8">Upload a PDF, DOCX, or TXT file to get instant AI analysis.</p>
            <div
              id="drop-zone"
              className="border-2 border-dashed border-white/15 rounded-2xl p-16 text-center hover:border-purple-500/50 transition-all cursor-pointer group"
              onDragOver={e => { e.preventDefault() }}
              onDrop={e => { e.preventDefault(); const f = e.dataTransfer.files[0]; if (f) handleUpload(f) }}
              onClick={() => fileRef.current?.click()}
            >
              <input id="resume-file-input" ref={fileRef} type="file" accept=".pdf,.docx,.doc,.txt" className="hidden" onChange={e => handleUpload(e.target.files[0])} />
              {uploading ? (
                <div className="flex flex-col items-center gap-4">
                  <div className="animate-spin border-4 border-purple-500 border-t-transparent rounded-full w-12 h-12" />
                  <p className="text-purple-400 font-medium">Analyzing your resume with AI…</p>
                </div>
              ) : (
                <>
                  <p className="text-6xl mb-4">📄</p>
                  <p className="text-xl font-semibold mb-2 group-hover:text-purple-300 transition">Drop your resume here</p>
                  <p className="text-gray-500">or click to browse • PDF, DOCX, TXT supported</p>
                </>
              )}
            </div>

            {resumes.length > 0 && (
              <div className="mt-8">
                <h2 className="text-lg font-semibold mb-4">Your Resumes</h2>
                <div className="space-y-3">
                  {resumes.map(r => (
                    <div key={r.id} onClick={() => { setSelectedResume(r); loadAnalysis(r.id); setActiveTab('analysis') }}
                      className="flex items-center justify-between p-4 bg-white/3 border border-white/8 rounded-xl hover:border-purple-500/30 cursor-pointer transition">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">📄</span>
                        <div>
                          <p className="font-medium text-sm">{r.original_filename}</p>
                          <p className="text-xs text-gray-500">{r.name || 'Unknown'} • Score: {r.score?.toFixed(0)}/100</p>
                        </div>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${r.score >= 75 ? 'bg-green-500/20 text-green-400' : r.score >= 50 ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'}`}>
                        {r.score?.toFixed(0)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ANALYSIS TAB */}
        {activeTab === 'analysis' && (
          <div className="max-w-3xl">
            <h1 className="text-2xl font-bold mb-6">Resume Analysis</h1>
            {!analysis ? (
              <div className="text-gray-400 text-center py-20">Upload a resume to see your analysis.</div>
            ) : loading ? (
              <div className="flex justify-center py-20"><div className="animate-spin border-4 border-purple-500 border-t-transparent rounded-full w-10 h-10" /></div>
            ) : (
              <>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                  {[
                    { label: 'Resume Score', score: analysis.score },
                    { label: 'ATS Score', score: analysis.ats_score },
                  ].map((s, i) => (
                    <div key={i} className="p-5 bg-white/3 border border-white/8 rounded-2xl flex flex-col items-center gap-2">
                      <ScoreRing score={s.score || 0} label={s.label} />
                    </div>
                  ))}
                  <div className="p-5 bg-white/3 border border-white/8 rounded-2xl col-span-2">
                    <p className="text-xs text-gray-400 mb-2">Extracted Name</p>
                    <p className="font-semibold">{analysis.name || '—'}</p>
                    <p className="text-xs text-gray-400 mt-3 mb-1">Skills Found</p>
                    <div className="flex flex-wrap gap-1">
                      {(analysis.skills || []).slice(0, 12).map(s => (
                        <span key={s} className="px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded-full text-xs">{s}</span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Suggestions */}
                {(analysis.improvement_suggestions || []).length > 0 && (
                  <div className="p-6 bg-white/3 border border-white/8 rounded-2xl mb-6">
                    <h2 className="font-semibold mb-4 flex items-center gap-2">💡 Improvement Suggestions</h2>
                    <ul className="space-y-2">
                      {analysis.improvement_suggestions.map((s, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                          <span className="text-yellow-400 mt-0.5">→</span>{s}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Keyword optimizer */}
                {(analysis.keyword_suggestions || []).length > 0 && (
                  <div className="p-6 bg-white/3 border border-white/8 rounded-2xl mb-6">
                    <h2 className="font-semibold mb-4 flex items-center gap-2">🔤 Keyword Optimizer</h2>
                    {analysis.keyword_suggestions.map((kw, i) => (
                      <div key={i} className="mb-3 p-3 rounded-xl bg-white/3">
                        <p className="text-xs text-red-400 mb-1 line-through">"{kw.original}"</p>
                        <p className="text-xs text-green-400">✓ "{kw.improved}"</p>
                      </div>
                    ))}
                  </div>
                )}

                {/* Education & Certifications */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {analysis.education?.length > 0 && (
                    <div className="p-5 bg-white/3 border border-white/8 rounded-2xl">
                      <h2 className="font-semibold mb-3 text-sm">🎓 Education</h2>
                      {analysis.education.map((e, i) => <p key={i} className="text-xs text-gray-300 mb-1">{e}</p>)}
                    </div>
                  )}
                  {analysis.certifications?.length > 0 && (
                    <div className="p-5 bg-white/3 border border-white/8 rounded-2xl">
                      <h2 className="font-semibold mb-3 text-sm">🏅 Certifications</h2>
                      {analysis.certifications.map((c, i) => <p key={i} className="text-xs text-gray-300 mb-1">{c}</p>)}
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        )}

        {/* JOB RECOMMENDATIONS TAB */}
        {activeTab === 'recommendations' && (
          <div className="max-w-3xl">
            <h1 className="text-2xl font-bold mb-2">AI Job Recommendations</h1>
            <p className="text-gray-400 mb-8">Jobs ranked by semantic similarity to your resume.</p>
            {loading ? (
              <div className="flex justify-center py-20"><div className="animate-spin border-4 border-purple-500 border-t-transparent rounded-full w-10 h-10" /></div>
            ) : recommendations.length === 0 ? (
              <p className="text-gray-400 text-center py-20">No recommendations yet. Upload a resume first.</p>
            ) : (
              <div className="space-y-4">
                {recommendations.map((r, i) => (
                  <div key={r.job.id} className="p-6 bg-white/3 border border-white/8 rounded-2xl hover:border-purple-500/30 transition">
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="font-semibold">{r.job.title}</h3>
                        <p className="text-sm text-gray-400">{r.job.company} • {r.job.location}</p>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className={`px-3 py-1 rounded-full text-sm font-bold ${r.match_score >= 70 ? 'bg-green-500/20 text-green-400' : r.match_score >= 50 ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-400'}`}>
                          {r.match_score?.toFixed(1)}% match
                        </span>
                        {i < 3 && <span className="text-xs text-purple-400 mt-1">#{i+1} pick</span>}
                      </div>
                    </div>
                    <p className="text-sm text-gray-400 mb-3 line-clamp-2">{r.job.description}</p>
                    <div className="flex flex-wrap gap-1 mb-3">
                      {r.matched_skills?.map(s => <span key={s} className="px-2 py-0.5 bg-green-500/15 text-green-400 rounded-full text-xs">✓ {s}</span>)}
                      {r.missing_skills?.slice(0, 3).map(s => <span key={s} className="px-2 py-0.5 bg-red-500/15 text-red-400 rounded-full text-xs">✗ {s}</span>)}
                    </div>
                    <button onClick={() => { loadSkillGap(r.job.id); setActiveTab('skillgap') }}
                      className="text-xs text-purple-400 hover:text-purple-300 transition">View Skill Gap →</button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* BROWSE JOBS TAB */}
        {activeTab === 'jobs' && (
          <div className="max-w-3xl">
            <h1 className="text-2xl font-bold mb-6">Browse Jobs</h1>
            <div className="flex gap-3 mb-6">
              <input id="job-search-input" value={searchQ} onChange={e => setSearchQ(e.target.value)} placeholder="Search jobs, e.g. Data Scientist"
                onKeyDown={e => e.key === 'Enter' && loadJobs(searchQ)}
                className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition" />
              <button id="job-search-btn" onClick={() => loadJobs(searchQ)}
                className="px-6 py-3 bg-purple-600 hover:bg-purple-500 rounded-xl transition">Search</button>
            </div>
            {jobs.length === 0 ? (
              <p className="text-gray-400 text-center py-16">No jobs found. Try a different search.</p>
            ) : (
              <div className="space-y-4">
                {jobs.map(job => (
                  <div key={job.id} className="p-5 bg-white/3 border border-white/8 rounded-2xl hover:border-purple-500/30 transition">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-semibold">{job.title}</h3>
                        <p className="text-sm text-gray-400">{job.company} • {job.location} • {job.job_type}</p>
                      </div>
                      {job.salary && <span className="text-sm text-green-400 font-medium">{job.salary}</span>}
                    </div>
                    <p className="text-sm text-gray-400 mt-2 line-clamp-2">{job.description}</p>
                    <div className="flex flex-wrap gap-1 mt-3">
                      {job.required_skills?.slice(0, 6).map(s => (
                        <span key={s} className="px-2 py-0.5 bg-white/5 text-gray-300 rounded-full text-xs">{s}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* SKILL GAP TAB */}
        {activeTab === 'skillgap' && (
          <div className="max-w-2xl">
            <h1 className="text-2xl font-bold mb-6">Skill Gap Analysis</h1>
            {!skillGap ? (
              <div className="text-center py-20">
                <p className="text-gray-400">Select a job from recommendations to analyze your skill gap.</p>
                <button onClick={() => handleTabClick('recommendations')}
                  className="mt-4 px-6 py-2 bg-purple-600 rounded-xl text-sm hover:bg-purple-500 transition">
                  View Recommendations
                </button>
              </div>
            ) : (
              <>
                <h2 className="text-lg font-semibold mb-2">{skillGap.job_title}</h2>
                <div className="flex gap-4 mb-6">
                  <div className="flex-1 p-4 bg-green-500/10 border border-green-500/20 rounded-2xl">
                    <p className="text-3xl font-bold text-green-400">{skillGap.match_percentage?.toFixed(0)}%</p>
                    <p className="text-xs text-gray-400">Skill Match</p>
                  </div>
                  <div className="flex-1 p-4 bg-white/3 border border-white/8 rounded-2xl">
                    <p className="text-3xl font-bold">{skillGap.matched_skills?.length}</p>
                    <p className="text-xs text-gray-400">Skills Matched</p>
                  </div>
                  <div className="flex-1 p-4 bg-red-500/10 border border-red-500/20 rounded-2xl">
                    <p className="text-3xl font-bold text-red-400">{skillGap.missing_skills?.length}</p>
                    <p className="text-xs text-gray-400">Skills Missing</p>
                  </div>
                </div>

                {skillGap.learning_resources?.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-4">📚 Learning Resources for Missing Skills</h3>
                    {skillGap.learning_resources.map((lr) => (
                      <div key={lr.skill} className="p-5 bg-white/3 border border-white/8 rounded-2xl mb-4">
                        <p className="font-medium text-purple-300 mb-3">⚠️ {lr.skill}</p>
                        <div className="grid grid-cols-2 gap-2">
                          {Object.entries(lr.resources).map(([type, url]) => (
                            <a key={type} href={url} target="_blank" rel="noopener noreferrer"
                              className="flex items-center gap-2 p-2 bg-white/5 rounded-lg text-xs text-gray-300 hover:text-white hover:bg-white/10 transition">
                              {type === 'youtube' ? '▶️' : type === 'coursera' ? '🎓' : type === 'docs' ? '📖' : '💻'}
                              {type.charAt(0).toUpperCase() + type.slice(1)}
                            </a>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
