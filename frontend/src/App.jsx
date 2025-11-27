import { useState, useRef } from 'react'

export default function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const resultRef = useRef(null)

  const handleAnalyze = async () => {
    if (!url) return
    setLoading(true)
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
      })
      const data = await response.json()
      setResult(data)
      setTimeout(() => resultRef.current?.scrollIntoView({ behavior: 'smooth' }), 100)
    } catch (error) {
      alert("Erreur serveur. Vérifiez que le backend Python tourne.")
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    if (status === 'success') return 'border-emerald-500/50 text-emerald-400 bg-emerald-500/10'
    if (status === 'warning') return 'border-orange-500/50 text-orange-400 bg-orange-500/10'
    return 'border-red-500/50 text-red-400 bg-red-500/10'
  }

  const getStatusDot = (status) => {
    if (status === 'success') return 'bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]'
    if (status === 'warning') return 'bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.5)]'
    return 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.5)]'
  }

  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans flex flex-col items-center relative p-6 pb-20">
      
      <div className="absolute top-[-20%] left-[20%] w-[500px] h-[500px] bg-purple-900/20 rounded-full blur-[120px] pointer-events-none" />
      
      <main className="z-10 w-full max-w-6xl mx-auto flex flex-col items-center">
        
        {/* HERO */}
        {!result && (
          <div className="text-center mt-20 mb-16 animate-fade-in">
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8 leading-tight">
              Optimisez votre expérience. <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">
                Instantanément.
              </span>
            </h1>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto font-light leading-relaxed">
              Détectez les erreurs qui font fuir vos visiteurs. SEO, UX, Performance : tout est analysé par l'IA.
            </p>
          </div>
        )}

        {/* INPUT */}
        <div className={`w-full max-w-3xl relative group transition-all duration-500 ${result ? 'mt-8 mb-12' : ''}`}>
          <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full opacity-20 blur transition duration-1000 group-hover:opacity-40"></div>
          <div className="relative flex items-center bg-[#0a0a0a] border border-white/10 rounded-full p-2 pl-6 shadow-2xl">
            <input 
              type="text" 
              placeholder="https://www.monsite.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 bg-transparent border-none text-gray-200 focus:outline-none placeholder-gray-600 h-10 font-normal"
            />
            <button 
              onClick={handleAnalyze}
              disabled={loading}
              className="bg-white text-black px-6 py-2 rounded-full font-bold text-sm hover:bg-gray-200 transition-all uppercase tracking-wide"
            >
              {loading ? 'Analyse...' : 'AUDITER'}
            </button>
          </div>
        </div>

        {/* DASHBOARD RESULTATS */}
        {result && (
          <div ref={resultRef} className="w-full animate-fade-in-up">
            
            {/* Header Score */}
            <div className="flex flex-col md:flex-row gap-6 mb-10">
              <div className="bg-[#0f0f0f] border border-white/10 p-6 rounded-2xl flex flex-col items-center justify-center min-w-[200px]">
                <span className={`text-7xl font-black ${
                    result.score_global > 80 ? 'text-emerald-400' : result.score_global > 50 ? 'text-orange-400' : 'text-red-400'
                  }`}>
                    {result.score_global}
                </span>
                <span className="text-xs font-bold uppercase tracking-widest text-gray-500 mt-2">Score Global</span>
              </div>

              <div className="flex-1 bg-[#0f0f0f] border border-white/10 p-6 rounded-2xl flex flex-col justify-center">
                <span className="text-gray-500 text-xs font-bold uppercase tracking-widest mb-2">Audit de l'URL</span>
                <p className="text-xl text-white font-mono break-all line-clamp-2">
                  {result.url}
                </p>
              </div>
            </div>

            {/* Grille Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-5 mb-10">
              {result.critiques.map((item, index) => (
                <div key={index} className="bg-[#0f0f0f] border border-white/5 p-6 rounded-xl hover:bg-white/[0.02] transition-colors group relative">
                  <div className="flex justify-between items-start mb-4">
                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">{item.cat}</span>
                    <div className={`w-3 h-3 rounded-full ${getStatusDot(item.status)}`}></div>
                  </div>
                  <div className="flex items-center gap-2 mb-3">
                    <h4 className="text-xl font-bold text-white">{item.label}</h4>
                    <div className="relative group/tooltip cursor-help">
                      <div className="w-4 h-4 rounded-full border border-gray-600 text-gray-400 flex items-center justify-center text-[10px] hover:border-white hover:text-white transition-colors font-serif italic">i</div>
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-3 bg-gray-800 text-xs text-gray-300 rounded-lg shadow-xl opacity-0 group-hover/tooltip:opacity-100 pointer-events-none transition-opacity z-50 border border-white/10 leading-relaxed">
                        {item.expl}
                        <div className="absolute top-full left-1/2 -translate-x-1/2 border-8 border-transparent border-t-gray-800"></div>
                      </div>
                    </div>
                  </div>
                  <div className={`inline-block px-3 py-1.5 rounded text-sm font-bold border ${getStatusColor(item.status)}`}>
                    {item.val}
                  </div>
                </div>
              ))}
            </div>

            {/* --- SYNTHÈSE GLOBALE --- */}
            <div className="bg-[#0f0f0f] border border-white/10 rounded-2xl p-8 animate-fade-in mt-8 shadow-2xl">
              
              <div className="flex items-center gap-3 mb-8 border-b border-white/10 pb-6">
                 <h2 className="text-3xl font-bold text-white">Plan d'action prioritaire</h2>
              </div>
              
              <div className="grid md:grid-cols-2 gap-12">
                
                {/* COLONNE GAUCHE : IA STRATÉGIQUE (NOUVELLE COULEUR) */}
                <div>
                  {/* Titre changé et couleur changée */}
                  <h3 className="text-indigo-400 font-bold uppercase tracking-widest text-sm mb-6 flex items-center gap-2">
                    🤖 L'avis de l'Expert IA
                  </h3>
                  
                  {result.ai_analysis ? (
                    <div 
                      // Style CSS pour forcer l'espacement et la couleur propre
                      className="prose prose-invert prose-p:text-gray-300 prose-p:mb-4 prose-headings:text-white prose-headings:mb-2 prose-headings:text-lg prose-strong:text-indigo-300 text-sm leading-relaxed"
                      dangerouslySetInnerHTML={{ __html: result.ai_analysis }} 
                    />
                  ) : (
                    <p className="text-gray-500 italic">Analyse IA indisponible pour ce site.</p>
                  )}
                </div>

                {/* COLONNE DROITE : CORRECTIFS TECHNIQUES */}
                <div>
                  <h3 className="text-orange-400 font-bold uppercase tracking-widest text-sm mb-6 flex items-center gap-2">
                    🛠️ Correctifs Techniques
                  </h3>
                  
                  <div className="space-y-4">
                    {result.critiques.filter(c => c.status !== 'success').length > 0 ? (
                      result.critiques.filter(c => c.status !== 'success').map((c, i) => (
                        <div key={i} className="flex gap-4 p-4 rounded-lg bg-white/5 border border-white/5 hover:border-white/10 transition-all">
                          <span className={`text-xs font-bold uppercase mt-1 min-w-[70px] ${
                            c.status === 'danger' ? 'text-red-400' : 'text-orange-400'
                          }`}>
                            {c.status === 'danger' ? 'Urgent' : 'À faire'}
                          </span>
                          <div>
                            <h4 className="font-bold text-gray-200 mb-1 text-sm">{c.label}</h4>
                            <p className="text-gray-400 text-xs leading-relaxed">
                              {c.reco}
                            </p>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-400 text-sm">
                        ✅ Aucun défaut technique majeur détecté.
                      </div>
                    )}
                  </div>
                </div>

              </div>
            </div>

          </div>
        )}

      </main>
    </div>
  )
}