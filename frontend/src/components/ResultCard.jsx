// ResultCard.jsx — shows tailored bullets

const ResultCard = ({ bullets }) => {
  if (!bullets.length) return null

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xl">✅</span>
        <h2 className="text-lg font-semibold text-white">
          Tailored Resume Bullets
        </h2>
      </div>

      <ul className="space-y-3">
        {bullets.map((bullet, i) => (
          <li
            key={i}
            className="flex items-start gap-3 text-sm text-gray-300 
                       bg-gray-900 rounded-lg p-3 border border-gray-700"
          >
            <span className="text-blue-400 mt-0.5 flex-shrink-0">→</span>
            <span>{bullet}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ResultCard