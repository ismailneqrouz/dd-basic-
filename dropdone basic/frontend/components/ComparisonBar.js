import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function ComparisonBar({ data=[] }) {
  return (
    <div className="bg-card-dark rounded-xl p-6 border border-slate-800">
      <h3 className="text-xl font-bold mb-4">AI vs Human Performance</h3>
      <div style={{ height: 260 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart layout="vertical" data={data}>
            <XAxis type="number" tick={{ fill: '#9ca3af' }} />
            <YAxis type="category" dataKey="name" tick={{ fill: '#9ca3af' }} width={160} />
            <CartesianGrid strokeDasharray="3 3" stroke="#0f1724"/>
            <Tooltip />
            <Bar dataKey="ai" stackId="a" fill="#11cbd6" radius={[10,10,10,10]} />
            <Bar dataKey="human" stackId="a" fill="#8b5cf6" radius={[10,10,10,10]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
