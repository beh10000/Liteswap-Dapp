import { createAppKit } from '@reown/appkit'
import { sepolia, hardhat, defineChain} from '@reown/appkit/networks'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'


const projectId = '5470014818925f68c908758733d9f2e0'

const gchainrpc = "https://98cec6b5a5d4.ngrok.app"


const customNetwork = defineChain({
  id: 8675309,
  caipNetworkId: 'eip155:8675309',
  chainNamespace: 'eip155',
  name: 'hardhat',
  nativeCurrency: {
    decimals: 18,
    name: 'Ethereum',
    symbol: 'ETH',
  },
  rpcUrls: {
    default: {
      http: [gchainrpc],
      webSocket: [gchainrpc],
    },
  },
  blockExplorers: {
    default: { name: 'Explorer', url: 'BLOCK_EXPLORER_URL' },
  },
  
})
export const networks = [ customNetwork, sepolia]
const wagmiAdapter = new WagmiAdapter({
  projectId,
  networks
})
const metadata = {
  name: 'Liteswap',
  description: 'Simple DEX.',
  url: '', // origin must match your domain & subdomain
  icons: ['_/theme/Liteswap.png']
}
const modal = createAppKit({
  adapters: [wagmiAdapter],
  networks: networks,
  metadata,
  projectId,
  features: {
    analytics: true, // Optional - defaults to your Cloud configuration
    email: false, // default to true
    socials: [],
    emailShowWallets: false, // default to true
  },
  themeVariables: {
  '--w3m-accent':"#7c17fc",
    '--w3m-font-family':"Jura",
    '--w3m-color-mix': '#000000',
    '--w3m-color-mix-strength': 40
  }
})



export {modal, wagmiAdapter}