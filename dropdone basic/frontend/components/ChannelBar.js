import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
export default function ChannelBar({ data=[] }) {
  return (
    <div className="bg-card-dark rounded-xl p-6 border border-slate-800">
      <h3 className="text-xl font-bold mb-4">Messages nach Kanal</h3>
      <div style={{height:260}}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="channel" tick={{fill:'#9ca3af'}}/>
            <YAxis tick={{fill:'#9ca3af'}}/>
            <CartesianGrid stroke="#0f1724" strokeDasharray="3 3"/>
            <Tooltip/>
            <Bar dataKey="value" fill="#60a5fa" radius={[8,8,8,8]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
