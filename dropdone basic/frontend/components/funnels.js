export default function Funnel({ data = [] }) {
  return (
    <div className="bg-card-dark rounded-xl p-6 border border-slate-800">
      <h3 className="text-xl font-bold mb-4">Lead Conversion Funnel</h3>
      <div className="space-y-4">
        {data.map((d,i)=>(
          <div key={i} className="flex items-center justify-between">
            <div className="w-2/3">
              <div className={`rounded-xl py-3 px-4`} style={{background:d.color, color:'#fff', boxShadow:'inset 0 -20px 40px rgba(0,0,0,0.15)'}}>
                <div className="text-lg font-bold">{d.label}</div>
              </div>
            </div>
            <div className="w-1/3 text-right text-slate-400">{d.count} contacts ({d.rate} conversion)</div>
          </div>
        ))}
      </div>
      <div className="mt-6 bg-slate-900 p-4 rounded-xl">
        <div className="text-slate-400">Overall Conversion Rate:</div>
        <div className="text-3xl font-bold text-cyan-300">100%</div>
      </div>
    </div>
  )
}
