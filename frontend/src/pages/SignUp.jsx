import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function SignUp() {
  const [form, setForm]       = useState({ name: '', email: '', password: '', confirm: '' })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  const onChange = (e) =>
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.name || !form.email || !form.password || !form.confirm) {
      setMessage({ type: 'error', text: 'Please fill in all fields.' })
      return
    }
    if (form.password !== form.confirm) {
      setMessage({ type: 'error', text: 'Passwords do not match.' })
      return
    }
    if (form.password.length < 8) {
      setMessage({ type: 'error', text: 'Password must be at least 8 characters.' })
      return
    }
    setLoading(true); setMessage(null)
    await new Promise(r => setTimeout(r, 1500))   // ← swap with real register call
    setLoading(false)
    setMessage({ type: 'success', text: 'Account created! Welcome to SoundClassify (demo).' })
  }

  const strength = (() => {
    const p = form.password
    if (!p) return 0
    let s = 0
    if (p.length >= 8) s++
    if (/[A-Z]/.test(p)) s++
    if (/[0-9]/.test(p)) s++
    if (/[^A-Za-z0-9]/.test(p)) s++
    return s
  })()

  const strengthLabel = ['', 'Weak', 'Fair', 'Good', 'Strong']
  const strengthColor = ['', 'bg-red-500', 'bg-yellow-500', 'bg-teal-400', 'bg-green-400']

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-16">
      <div className="w-full max-w-md animate-slide-up">

        {/* Icon */}
        <div className="flex justify-center mb-8">
          <div className="p-4 rounded-2xl bg-teal-500/10 border border-teal-500/20">
            <svg width="32" height="32" fill="none" stroke="currentColor" strokeWidth="2"
              viewBox="0 0 24 24" className="text-teal-400">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <line x1="19" y1="8" x2="19" y2="14" />
              <line x1="22" y1="11" x2="16" y2="11" />
            </svg>
          </div>
        </div>

        {/* Heading */}
        <h1 className="text-3xl font-bold text-white text-center mb-2">Create an account</h1>
        <p className="text-slate-400 text-center mb-8">
          Start classifying environmental sounds today
        </p>

        {/* Card */}
        <div className="glass-card p-8">
          <form onSubmit={handleSubmit} className="flex flex-col gap-5" noValidate>

            <div>
              <label htmlFor="signup-name" className="label">Full name</label>
              <input
                id="signup-name"
                type="text"
                name="name"
                value={form.name}
                onChange={onChange}
                placeholder="Jane Doe"
                className="input-field"
                autoComplete="name"
              />
            </div>

            <div>
              <label htmlFor="signup-email" className="label">Email address</label>
              <input
                id="signup-email"
                type="email"
                name="email"
                value={form.email}
                onChange={onChange}
                placeholder="you@example.com"
                className="input-field"
                autoComplete="email"
              />
            </div>

            <div>
              <label htmlFor="signup-password" className="label">Password</label>
              <input
                id="signup-password"
                type="password"
                name="password"
                value={form.password}
                onChange={onChange}
                placeholder="Min. 8 characters"
                className="input-field"
                autoComplete="new-password"
              />
              {/* Password strength bar */}
              {form.password && (
                <div className="mt-2">
                  <div className="flex gap-1 h-1">
                    {[1,2,3,4].map(n => (
                      <div key={n}
                        className={`flex-1 rounded-full transition-colors duration-300
                                    ${n <= strength ? strengthColor[strength] : 'bg-white/10'}`} />
                    ))}
                  </div>
                  <p className={`text-xs mt-1 transition-colors ${
                    strength <= 1 ? 'text-red-400'
                    : strength === 2 ? 'text-yellow-400'
                    : strength === 3 ? 'text-teal-400'
                    : 'text-green-400'
                  }`}>
                    {strengthLabel[strength]}
                  </p>
                </div>
              )}
            </div>

            <div>
              <label htmlFor="signup-confirm" className="label">Confirm password</label>
              <input
                id="signup-confirm"
                type="password"
                name="confirm"
                value={form.confirm}
                onChange={onChange}
                placeholder="Re-enter password"
                className={`input-field ${
                  form.confirm && form.confirm !== form.password
                    ? 'border-red-500/50 focus:ring-red-500/30' : ''
                }`}
                autoComplete="new-password"
              />
              {form.confirm && form.confirm !== form.password && (
                <p className="text-red-400 text-xs mt-1">Passwords do not match</p>
              )}
            </div>

            {/* Feedback message */}
            {message && (
              <div className={`flex items-center gap-2 px-4 py-3 rounded-xl text-sm
                              ${message.type === 'success'
                                ? 'bg-teal-500/10 border border-teal-500/20 text-teal-300'
                                : 'bg-red-500/10 border border-red-500/20 text-red-400'}`}>
                {message.type === 'success' ? '✅' : '⚠️'} {message.text}
              </div>
            )}

            <button
              id="signup-submit"
              type="submit"
              disabled={loading}
              className="btn-primary w-full mt-1"
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10"
                      stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Creating account…
                </>
              ) : 'Create Account'}
            </button>
          </form>
        </div>

        {/* Login link */}
        <p className="text-slate-500 text-sm text-center mt-6">
          Already have an account?{' '}
          <Link to="/login"
            className="text-teal-400 font-medium hover:text-teal-300 transition-colors">
            Sign in →
          </Link>
        </p>

      </div>
    </div>
  )
}
