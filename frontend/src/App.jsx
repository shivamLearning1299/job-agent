import { useState } from "react"
import JDInput from "./components/JDInput"
import ResultCard from "./components/ResultCard"
import GapAnalysis from "./components/GapAnalysis"

// Parses the raw text result from the agent
// into bullets array and gaps array
function parseResult(rawText) {
  const bullets = []
  const gaps = []

  const lines = rawText.split("\n")
  let section = null

  for (const line of lines) {
    const trimmed = line.trim()

    if (trimmed.includes("TAILORED BULLETS")) {
      section = "bullets"
    } else if (trimmed.includes("SKILL GAPS")) {
      section = "gaps"
    } else if (trimmed.startsWith("-") && trimmed.length > 2) {
      const content = trimmed.slice(1).trim()
      if (section === "bullets") bullets.push(content)
      if (section === "gaps") gaps.push(content)
    }
  }

  return { bullets, gaps }
}

function App() {
  const [jdText, setJdText]   = useState("")
  const [bullets, setBullets] = useState([])
  const [gaps, setGaps]       = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)
  const [analyzed, setAnalyzed] = useState(false)

  const handleAnalyze = async () => {
    if (!jdText.trim()) return

    setLoading(true)
    setError(null)
    setBullets([])
    setGaps([])

    try {
      // Call our FastAPI backend
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jd_text: jdText })
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const data = await response.json()

      // Parse the raw text into structured data
      const { bullets: b, gaps: g } = parseResult(data.result)
      setBullets(b)
      setGaps(g)
      setAnalyzed(true)

    } catch (err) {
      setError(err.message || "Something went wrong. Is FastAPI running?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">

      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center gap-3">
          <span className="text-2xl">🤖</span>
          <div>
            <h1 className="text-xl font-bold text-white">
              Job Application Agent
            </h1>
            <p className="text-xs text-gray-400">
              Powered by LangChain · ChromaDB · Ollama · LangFuse
            </p>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            <span className="text-xs text-gray-400">Agent ready</span>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          {/* Left — JD Input */}
          <JDInput
            jdText={jdText}
            setJdText={setJdText}
            onAnalyze={handleAnalyze}
            loading={loading}
          />

          {/* Right — Results */}
          <div className="flex flex-col gap-6">

            {/* Error state */}
            {error && (
              <div className="bg-red-900/30 border border-red-700 
                            rounded-xl p-4 text-red-300 text-sm">
                ❌ {error}
              </div>
            )}

            {/* Loading state */}
            {loading && (
              <div className="bg-gray-800 border border-gray-700 
                            rounded-xl p-8 text-center">
                <div className="w-8 h-8 border-2 border-blue-500 
                              border-t-transparent rounded-full 
                              animate-spin mx-auto mb-4" />
                <p className="text-gray-400 text-sm">
                  Agent is analyzing your JD...
                </p>
                <p className="text-gray-600 text-xs mt-1">
                  This takes 15-30 seconds
                </p>
              </div>
            )}

            {/* Empty state */}
            {!loading && !analyzed && !error && (
              <div className="bg-gray-800 border border-gray-700 border-dashed
                            rounded-xl p-12 text-center">
                <p className="text-4xl mb-4">📋</p>
                <p className="text-gray-400 text-sm">
                  Paste a job description and click Analyze
                </p>
                <p className="text-gray-600 text-xs mt-2">
                  Your tailored bullets and skill gaps will appear here
                </p>
              </div>
            )}

            {/* Results */}
            {!loading && analyzed && (
              <>
                <ResultCard bullets={bullets} />
                <GapAnalysis gaps={gaps} />
              </>
            )}

          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 px-6 py-4 mt-8">
        <div className="max-w-7xl mx-auto text-center text-xs text-gray-600">
          100% local · No data leaves your Mac · Built with LangChain + ChromaDB + Ollama
        </div>
      </footer>

    </div>
  )
}

export default App