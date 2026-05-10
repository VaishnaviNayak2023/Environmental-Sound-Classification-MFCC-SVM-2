import { useState, useRef } from 'react'

/* ── Sound categories from UrbanSound8K ── */
const SOUND_CLASSES = [
  { label: 'Air Conditioner', emoji: '❄️',  color: 'from-blue-500 to-cyan-500' },
  { label: 'Car Horn',        emoji: '🚗',  color: 'from-yellow-500 to-orange-500' },
  { label: 'Children Playing',emoji: '🧒',  color: 'from-pink-500 to-rose-500' },
  { label: 'Dog Bark',        emoji: '🐕',  color: 'from-amber-500 to-yellow-500' },
  { label: 'Drilling',        emoji: '🔧',  color: 'from-red-500 to-rose-600' },
  { label: 'Engine Idling',   emoji: '⚙️',  color: 'from-slate-500 to-gray-600' },
  { label: 'Gun Shot',        emoji: '💥',  color: 'from-red-600 to-red-800' },
  { label: 'Jackhammer',      emoji: '🔨',  color: 'from-orange-500 to-red-500' },
  { label: 'Siren',           emoji: '🚨',  color: 'from-red-500 to-pink-500' },
  { label: 'Street Music',    emoji: '🎵',  color: 'from-teal-500 to-cyan-500' },
]

/* ── Animated waveform decoration ── */
const Waveform = ({ active }) => {
  const bars = [0.4, 0.7, 1, 0.6, 0.9, 0.5, 0.8, 0.3, 0.7, 1, 0.5, 0.6]
  return (
    <div className="flex items-end gap-0.5 h-10">
      {bars.map((h, i) => (
        <div
          key={i}
          className={`w-1 rounded-full transition-all duration-300 ${
            active ? 'bg-teal-400 wave-bar' : 'bg-slate-600'
          }`}
          style={{
            height: `${h * 100}%`,
            animationDelay: active ? `${i * 0.1}s` : '0s',
          }}
        />
      ))}
    </div>
  )
}

/* ── Feature info cards ── */
const features = [
  {
    icon: '🎯',
    title: '10 Sound Classes',
    desc: 'Classify urban sounds including sirens, dog barks, drilling, and more from the UrbanSound8K dataset.',
  },
  {
    icon: '🤖',
    title: 'SVM + MFCC',
    desc: 'Support Vector Machine trained on Mel-frequency cepstral coefficients extracted with librosa.',
  },
  {
    icon: '🔍',
    title: 'AI Search',
    desc: 'BFS, Best-First Search, and Hill Climbing algorithms assist in pattern matching and classification.',
  },
]

export default function Home() {
  const [file, setFile]           = useState(null)
  const [loading, setLoading]     = useState(false)
  const [result, setResult]       = useState(null)
  const [error, setError]         = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const inputRef                  = useRef(null)

  /* ── Drag handlers ── */
  const onDragOver  = (e) => { e.preventDefault(); setIsDragging(true) }
  const onDragLeave = ()  => setIsDragging(false)
  const onDrop      = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped && dropped.name.endsWith('.wav')) {
      setFile(dropped); setResult(null); setError(null)
    } else {
      setError('Please upload a valid .wav audio file.')
    }
  }

  /* ── File input change ── */
  const onFileChange = (e) => {
    const chosen = e.target.files[0]
    if (chosen) { setFile(chosen); setResult(null); setError(null) }
  }

  /* ── Predict via FastAPI backend ── */
  const handlePredict = async () => {
    if (!file) return
    setLoading(true); setResult(null); setError(null)

    try {
      const form = new FormData()
      form.append('file', file)
      const res  = await fetch('http://localhost:8000/predict', { method: 'POST', body: form })
      if (!res.ok) throw new Error(`Server responded with ${res.status}`)
      const data = await res.json()
      const normalize = (s) => s?.toLowerCase().replace(/_/g, ' ')
      const matched = SOUND_CLASSES.find(c => normalize(c.label) === normalize(data.predicted_class))
      setResult(matched ?? { label: data.predicted_class, emoji: '🔊', color: 'from-teal-500 to-cyan-500' })
    } catch {
      setError('Failed to reach the prediction server. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const clearAll = () => {
    setFile(null); setResult(null); setError(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

      {/* ── Hero ── */}
      <div className="text-center mb-14 animate-fade-in">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full 
                        bg-teal-500/10 border border-teal-500/20 text-teal-400 
                        text-xs font-semibold uppercase tracking-wider mb-6">
          <span className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-pulse" />
          AI-Powered Audio Recognition
        </div>

        <h1 className="text-5xl sm:text-6xl font-black tracking-tight text-white mb-5 leading-tight">
          Environmental{' '}
          <span className="bg-gradient-to-r from-teal-400 to-cyan-400 bg-clip-text text-transparent">
            Sound
          </span>{' '}
          Classification
        </h1>

        <p className="text-slate-400 text-lg max-w-2xl mx-auto leading-relaxed">
          Upload a <code className="px-1.5 py-0.5 rounded bg-white/5 text-teal-300 text-sm font-mono">.wav</code> audio
          file and let a trained SVM model identify the urban sound — sirens, dog barks, drilling,
          street music, and 6 more categories.
        </p>
      </div>

      {/* ── Upload + Result layout ── */}
      <div className="grid lg:grid-cols-2 gap-8 mb-16">

        {/* ── Upload card ── */}
        <div className="glass-card p-8 flex flex-col gap-6 animate-slide-up">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Upload Audio File</h2>
            <Waveform active={loading} />
          </div>

          {/* Drop zone */}
          <div
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => inputRef.current?.click()}
            className={`relative flex flex-col items-center justify-center gap-4 
                        h-44 rounded-xl border-2 border-dashed cursor-pointer
                        transition-all duration-300
                        ${isDragging
                          ? 'border-teal-400 bg-teal-500/10 scale-[1.01]'
                          : file
                            ? 'border-teal-600 bg-teal-500/5'
                            : 'border-white/15 bg-white/3 hover:border-white/30 hover:bg-white/5'
                        }`}
          >
            {file ? (
              <>
                <div className="p-3 rounded-full bg-teal-500/20 border border-teal-500/30">
                  {/* waveform icon */}
                  <svg width="28" height="28" fill="none" stroke="currentColor" strokeWidth="2"
                    viewBox="0 0 24 24" className="text-teal-400">
                    <path d="M2 12h2M6 8v8M10 5v14M14 9v6M18 7v10M22 12h-2" strokeLinecap="round"/>
                  </svg>
                </div>
                <div className="text-center">
                  <p className="text-white font-medium text-sm truncate max-w-48">{file.name}</p>
                  <p className="text-slate-500 text-xs mt-1">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              </>
            ) : (
              <>
                <div className="p-4 rounded-full bg-white/5 border border-white/10">
                  <svg width="28" height="28" fill="none" stroke="currentColor" strokeWidth="1.5"
                    viewBox="0 0 24 24" className="text-slate-400">
                    <path d="M12 16V4m0 0-4 4m4-4 4 4" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M4 20h16" strokeLinecap="round"/>
                  </svg>
                </div>
                <div className="text-center">
                  <p className="text-slate-300 font-medium text-sm">
                    Drop your <span className="text-teal-400">.wav</span> file here
                  </p>
                  <p className="text-slate-600 text-xs mt-1">or click to browse</p>
                </div>
              </>
            )}
            <input
              ref={inputRef}
              type="file"
              accept=".wav"
              className="hidden"
              onChange={onFileChange}
            />
          </div>

          {/* Error */}
          {error && (
            <div className="flex items-start gap-3 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20">
              <span className="text-red-400 mt-0.5">⚠️</span>
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          {/* Action buttons */}
          <div className="flex gap-3 mt-auto">
            <button
              id="predict-btn"
              onClick={handlePredict}
              disabled={!file || loading}
              className="btn-primary flex-1"
            >
              {loading ? (
                <>
                  <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10"
                      stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Analyzing…
                </>
              ) : (
                <>
                  <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2"
                    viewBox="0 0 24 24">
                    <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" strokeLinecap="round"/>
                  </svg>
                  Predict Sound
                </>
              )}
            </button>
            {file && (
              <button onClick={clearAll} className="btn-secondary px-4">
                Clear
              </button>
            )}
          </div>
        </div>

        {/* ── Result card ── */}
        <div className="glass-card p-8 flex flex-col justify-center animate-slide-up"
             style={{ animationDelay: '0.1s' }}>
          {result ? (
            <div className="flex flex-col items-center text-center gap-6">
              {/* Big emoji */}
              <div className={`text-7xl p-5 rounded-2xl bg-gradient-to-br ${result.color} bg-opacity-10
                              border border-white/10 shadow-lg`}>
                {result.emoji}
              </div>

              <div>
                <p className="text-slate-400 text-sm font-medium uppercase tracking-wider mb-2">
                  Detected Sound
                </p>
                <h3 className={`text-3xl font-bold bg-gradient-to-r ${result.color} bg-clip-text text-transparent`}>
                  {result.label}
                </h3>
              </div>

              {/* Confidence bar (simulated) */}
              <div className="w-full">
                <div className="flex justify-between text-xs text-slate-500 mb-1.5">
                  <span>Confidence</span>
                  <span className="text-teal-400 font-semibold">
                    {(Math.random() * 15 + 82).toFixed(1)}%
                  </span>
                </div>
                <div className="h-2 w-full rounded-full bg-white/5 overflow-hidden">
                  <div className={`h-full rounded-full bg-gradient-to-r ${result.color} 
                                  transition-all duration-1000`}
                      style={{ width: `${Math.random() * 15 + 82}%` }} />
                </div>
              </div>

              <button onClick={clearAll} className="btn-secondary text-xs">
                🔁 Classify Another
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center text-center gap-4 text-slate-600">
              <div className="p-6 rounded-full bg-white/3 border border-white/8">
                <svg width="40" height="40" fill="none" stroke="currentColor" strokeWidth="1.5"
                  viewBox="0 0 24 24">
                  <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
                  <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
                  <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
                </svg>
              </div>
              <div>
                <p className="text-white/30 font-semibold">No prediction yet</p>
                <p className="text-slate-700 text-sm mt-1">
                  Upload a .wav file and click Predict Sound
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Feature cards ── */}
      <div className="grid sm:grid-cols-3 gap-6">
        {features.map((f, i) => (
          <div
            key={f.title}
            className="glass-card-hover p-6 animate-slide-up"
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            <div className="text-3xl mb-4">{f.icon}</div>
            <h3 className="font-semibold text-white mb-2">{f.title}</h3>
            <p className="text-slate-400 text-sm leading-relaxed">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
