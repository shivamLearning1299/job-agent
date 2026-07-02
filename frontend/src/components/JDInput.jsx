// JDInput.jsx — Left side: where user pastes the JD

const JDInput = ({ jdText, setJdText, onAnalyze, loading }) => {
  return (
    <div className="flex flex-col h-full gap-4">
      <div>
        <h2 className="text-lg font-semibold text-white mb-1">
          Paste Job Description
        </h2>
        <p className="text-sm text-gray-400">
          Paste any JD and the agent will tailor your resume to it
        </p>
      </div>

      <textarea
        className="flex-1 w-full bg-gray-800 text-gray-100 border border-gray-700 
                   rounded-xl p-4 text-sm resize-none focus:outline-none 
                   focus:border-blue-500 placeholder-gray-500 min-h-[400px]"
        placeholder="Paste job description here...

Example:
We are looking for a Senior Backend Engineer with:
- Python and FastAPI experience
- RAG pipeline development
- Vector database knowledge
- AWS deployment experience"
        value={jdText}
        onChange={(e) => setJdText(e.target.value)}
      />

      <button
        onClick={onAnalyze}
        disabled={loading || !jdText.trim()}
        className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 
                   disabled:bg-gray-700 disabled:cursor-not-allowed
                   text-white font-semibold rounded-xl transition-all
                   duration-200 flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <div className="w-4 h-4 border-2 border-white border-t-transparent 
                          rounded-full animate-spin" />
            Agent is thinking...
          </>
        ) : (
          "⚡ Analyze JD"
        )}
      </button>
    </div>
  )
}

export default JDInput