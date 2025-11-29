import useSWR from 'swr'
import API from '../utils/api'
import StatCard from '../components/StatCard'
import Funnel from '../components/Funnel'
import ResponseChart from '../components/ResponseChart'
import ComparisonBar from '../components/ComparisonBar'
import PieStatus from '../components/PieStatus'
import ChannelBar from '../components/ChannelBar'

const fetcher = (url) => API.get(url).then(r=>r.data)

export default function Dashboard(){
  const { data, error } = useSWR('/stats', fetcher)

  if (error) return <div>Failed to load stats</div>
  if (!data) return <div>Loading...</div>

  return
   (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold mb-1">Dashboard</h1>
        <p className="text-slate-400">Übersicht deiner AI-gesteuerten Kommunikation</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <StatCard icon="📞" value={data.total_calls} subtitle="Total Calls" delta="+12%"/>
        <StatCard icon="💬" value={data.total_messages} subtitle="Messages" delta="+18%"/>
        <StatCard icon="👥" value={data.total_contacts} subtitle="Contacts" delta="+24%"/>
        <StatCard icon="📈" value={`${data.ai_success_rate}%`} subtitle="AI Success Rate" delta="+2%"/>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <Funnel data={data.funnel}/>
        <ResponseChart data={data.time_series} />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <ComparisonBar data={data.comparison} />
        <div className="space-y-6">
          <PieStatus data={data.status_pie}/>
          <ChannelBar data={data.channel_bars}/>
        </div>
      </div>
    </div>
  )
}
