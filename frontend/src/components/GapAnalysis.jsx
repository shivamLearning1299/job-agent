// GapAnalysis.jsx — shows skill gaps

const GapAnalysis = ({ gaps }) => {
  if (!gaps.length) return null

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xl">⚠️</span>
        <h2 className="text-lg font-semibold text-white">
          Skill Gaps to Address
        </h2>
        <span className="ml-auto text-xs bg-red-900 text-red-300 
                        px-2 py-1 rounded-full">
          {gaps.length} gaps found
        </span>
      </div>

      <ul className="space-y-2">
        {gaps.map((gap, i) => (
          <li
            key={i}
            className="flex items-center gap-3 text-sm text-gray-300
                       bg-gray-900 rounded-lg p-3 border border-red-900"
          >
            <span className="text-red-400 flex-shrink-0">✗</span>
            <span>{gap}</span>
          </li>
        ))}
      </ul>

      <p className="mt-4 text-xs text-gray-500">
        💡 Consider adding these to your resume or cover letter
      </p>
    </div>
  )
}

export default GapAnalysis