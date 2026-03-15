const API_BASE = 'http://localhost:8000/api'

const getHeaders = (isForm = false) => {
  const token = localStorage.getItem('access_token')
  const headers = { 'Authorization': `Bearer ${token}` }
  if (!isForm) headers['Content-Type'] = 'application/json'
  return headers
}

const handleResponse = async (response) => {
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || data.error || JSON.stringify(data) || 'Request failed')
  return data
}

// Auth
export const registerUser = (data) =>
  fetch(`${API_BASE}/auth/register/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(handleResponse)

export const loginUser = (data) =>
  fetch(`${API_BASE}/auth/login/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(handleResponse)

// Resume
export const uploadResume = (formData) =>
  fetch(`${API_BASE}/resume/upload/`, { method: 'POST', headers: getHeaders(true), body: formData }).then(handleResponse)

export const getResumes = () =>
  fetch(`${API_BASE}/resume/list/`, { headers: getHeaders() }).then(handleResponse)

export const getResumeAnalysis = (id) =>
  fetch(`${API_BASE}/resume/${id}/analysis/`, { headers: getHeaders() }).then(handleResponse)

// Jobs
export const getJobs = (q = '') =>
  fetch(`${API_BASE}/jobs/${q ? `?q=${encodeURIComponent(q)}` : ''}`, { headers: getHeaders() }).then(handleResponse)

export const getJobRecommendations = (resumeId) =>
  fetch(`${API_BASE}/jobs/recommendations/${resumeId ? `?resume_id=${resumeId}` : ''}`, { headers: getHeaders() }).then(handleResponse)

export const getSkillGap = (resumeId, jobId) =>
  fetch(`${API_BASE}/jobs/skill-gap/?resume_id=${resumeId}&job_id=${jobId}`, { headers: getHeaders() }).then(handleResponse)

// Recruiter
export const getRecruiterJobs = () =>
  fetch(`${API_BASE}/recruiter/jobs/`, { headers: getHeaders() }).then(handleResponse)

export const createJob = (data) =>
  fetch(`${API_BASE}/recruiter/jobs/`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse)

export const updateJob = (id, data) =>
  fetch(`${API_BASE}/recruiter/jobs/${id}/`, { method: 'PATCH', headers: getHeaders(), body: JSON.stringify(data) }).then(handleResponse)

export const deleteJob = (id) =>
  fetch(`${API_BASE}/recruiter/jobs/${id}/`, { method: 'DELETE', headers: getHeaders() })

export const screenCandidates = (formData) =>
  fetch(`${API_BASE}/recruiter/screen/`, { method: 'POST', headers: getHeaders(true), body: formData }).then(handleResponse)

export const getRecruiterAnalytics = (jobId = null) =>
  fetch(`${API_BASE}/recruiter/analytics/${jobId ? `?job_id=${jobId}` : ''}`, { headers: getHeaders() }).then(handleResponse)

export const clearRecruiterAnalytics = (jobId = null) =>
  fetch(`${API_BASE}/recruiter/analytics/${jobId ? `?job_id=${jobId}` : ''}`, { method: 'DELETE', headers: getHeaders() }).then(handleResponse)
