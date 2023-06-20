import '../styles/globals.css'
import 'bootstrap/dist/css/bootstrap.min.css';

import { Inter } from '@next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function MyApp({ Component, pageProps }) {
  return (
    <div className={inter.className}>
    <Component {...pageProps} />
    </div>  )
  }


