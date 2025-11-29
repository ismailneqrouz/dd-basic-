import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

export default function ResponseChart({ data = [] }) {
  return (
    <div className="bg-card-dark rounded-xl p-6 border border-slate-800">
      <h3 className="text-xl font-bold mb-4">AI Response Times (24h)</h3>
      <div style={{ height: 320 }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorCall" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#11cbd6" stopOpacity={0.9}/>
                <stop offset="95%" stopColor="#0b2740" stopOpacity={0.1}/>
              </linearGradient>
              <linearGradient id="colorMsg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.9}/>
                <stop offset="95%" stopColor="#0b1830" stopOpacity={0.1}/>
              </linearGradient>
            </defs>
            <XAxis dataKey="time" tick={{fill:'#9ca3af'}}/>
            <YAxis tick={{fill:'#9ca3af'}}/>
            <CartesianGrid strokeDasharray="3 3" stroke="#0f1724"/>
            <Tooltip />
            <Area type="monotone" dataKey="call" stroke="#11cbd6" fill="url(#colorCall)" dot={false}/>
            <Area type="monotone" dataKey="message" stroke="#8b5cf6" fill="url(#colorMsg)" dot={false}/>
            <Legend verticalAlign="bottom" align="center" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="bg-slate-900 p-4 rounded-xl">
          <div className="text-slate-400">Avg Call Response</div>
          <div className="text-2xl text-cyan-300 font-bold">2.7s</div>
        </div>
        <div className="bg-slate-900 p-4 rounded-xl">
          <div className="text-slate-400">Avg Message Response</div>
          <div className="text-2xl text-violet-400 font-bold">1.9s</div>
        </div>
      </div>
    </div>
  )
}
