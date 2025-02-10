import { createAppKit } from '@reown/appkit'
import { sepolia, hardhat} from '@reown/appkit/networks'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'


const projectId = '5470014818925f68c908758733d9f2e0'

const contractAddress = "0x165BAD87E3eF9e1F4FB9b384f2BD1FaBDc414f17"

export const networks = [ hardhat]
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


const abi = []
export {modal, wagmiAdapter, contractAddress, abi}