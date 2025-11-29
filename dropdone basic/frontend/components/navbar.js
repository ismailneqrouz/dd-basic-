import React from 'react'

export default function NavBar(){
  return (
    <header className="bg-transparent py-3 px-6 border-b border-slate-800 sticky top-0 z-40">
      <div className="max-w-6xl mx-auto flex items-center gap-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-cyan-400 flex items-center justify-center text-white font-bold shadow-lg">★</div>
          <div className="text-2xl font-bold text-cyan-400">Dropdone</div>
        </div>

        <nav className="flex-1 flex items-center gap-6">
          <button className="bg-slate-800 text-cyan-200 px-3 py-2 rounded-md">📊 Dashboard</button>
          <button className="text-slate-300">📞 KI-Anrufe</button>
          <button className="text-slate-300">💬 Nachrichten</button>
          <button className="text-slate-300">👥 CRM</button>
          <button className="text-slate-300">⚙ Einstellungen</button>
        </nav>

        <div className="flex items-center gap-3">
          <div className=
          "w-9 h-9 rounded-full bg-gradient-to-br from-sky-400 to-blue-600 flex items-center justify-center text-white">i</div>
          <div className="text-sm">
            <div className="font-semibold">ismail neqrouz</div>
            <div className="text-xs text-slate-400">n17ismail@gmail.com</div>
          </div>
        </div>
      </div>
    </header>
  )
}
