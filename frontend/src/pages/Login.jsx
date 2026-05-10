import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function Login() {
  const [form, setForm]       = useState({ email: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null) // { type: 'success'|'error', text }

  const onChange = (e) =>
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.email || !form.password) {
      setMessage({ type: 'error', text: 'Please fill in all fields.' })
      return
    }
    setLoading(true); setMessage(null)
    await new Promise(r => setTimeout(r, 1500))   // ← swap with real auth call
    setLoading(false)
    setMessage({ type: 'success', text: 'Logged in successfully! (demo)' })
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-16">
      <div className="w-full max-w-md animate-slide-up">

        {/* Icon */}
        <div className="flex justify-center mb-8">
          <div className="p-4 rounded-2xl bg-teal-500/10 border border-teal-500/20">
            <svg width="32" height="32" fill="none" stroke="currentColor" strokeWidth="2"
              viewBox="0 0 24 24" className="text-teal-400">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>
        </div>

        {/* Heading */}
        <h1 className="text-3xl font-bold text-white text-center mb-2">Welcome back</h1>
        <p className="text-slate-400 text-center mb-8">
          Sign in to your SoundClassify account
        </p>

        {/* Card */}
        <div className="glass-card p-8">
          <form onSubmit={handleSubmit} className="flex flex-col gap-5" noValidate>

            <div>
              <label htmlFor="login-email" className="label">Email address</label>
              <input
                id="login-email"
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
              <div className="flex items-center justify-between mb-1.5">
                <label htmlFor="login-password" className="label !mb-0">Password</label>
                <button type="button"
                  className="text-xs text-teal-400 hover:text-teal-300 transition-colors">
                  Forgot password?
                </button>
              </div>
              <input
                id="login-password"
                type="password"
                name="password"
                value={form.password}
                onChange={onChange}
                placeholder="••••••••"
                className="input-field"
                autoComplete="current-password"
              />
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
              id="login-submit"
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
                  Signing in…
                </>
              ) : 'Sign In'}
            </button>
          </form>
        </div>

        {/* Sign-up link */}
        <p className="text-slate-500 text-sm text-center mt-6">
          Don't have an account?{' '}
          <Link to="/signup"
            className="text-teal-400 font-medium hover:text-teal-300 transition-colors">
            Create one free →
          </Link>
        </p>

      </div>
    </div>
  )
}
