export default function StatCard({ icon, title, value, subtitle, delta }) {
  return (
    <div className="bg-card-dark border border-slate-800 rounded-xl p-6 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center text-white text-xl">{icon}</div>
        <div>
          <div className="text-white text-3xl font-bold">{value}</div>
          <div className="text-slate-400">{subtitle}</div>
        </div>
      </div>
      <div className="text-green-400 font-semibold">{delta}</div>
    </div>
  )
}
