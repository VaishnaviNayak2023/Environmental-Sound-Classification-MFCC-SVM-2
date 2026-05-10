import { Link, useLocation } from 'react-router-dom'

const SoundIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
    strokeLinecap="round" strokeLinejoin="round" className="text-teal-400">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
    <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
    <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
  </svg>
)

export default function Navbar() {
  const { pathname } = useLocation()

  const isActive = (path) => pathname === path

  return (
    <nav className="sticky top-0 z-50 border-b border-white/8 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">

          {/* Brand */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="p-1.5 rounded-lg bg-teal-500/10 border border-teal-500/20 
                            group-hover:bg-teal-500/20 transition-colors duration-200">
              <SoundIcon />
            </div>
            <span className="font-bold text-white text-lg tracking-tight">
              Sound<span className="text-teal-400">Classify</span>
            </span>
          </Link>

          {/* Nav links */}
          <div className="flex items-center gap-1">
            <Link to="/"
              className={isActive('/') ? 'nav-link-active' : 'nav-link'}>
              Home
            </Link>
            <Link to="/login"
              className={isActive('/login') ? 'nav-link-active' : 'nav-link'}>
              Login
            </Link>
            <Link to="/signup"
              className={isActive('/signup') ? 'btn-primary !py-2 !px-4 ml-2' : 'nav-link'}>
              Sign Up
            </Link>
          </div>

        </div>
      </div>
    </nav>
  )
}
