import './styles/globals.css'
import NavBar from './components/NavBar'

export default function App({ Component, pageProps }) {
  return (
    <>
      <NavBar />
      <main className="max-w-6xl mx-auto p-6">
        <Component {...pageProps} />
      </main>
    </>
  )
}
