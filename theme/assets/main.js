import { createAppKit } from '@reown/appkit'
import { sepolia, hardhat, defineChain} from '@reown/appkit/networks'
import { WagmiAdapter } from '@reown/appkit-adapter-wagmi'


const projectId = '5470014818925f68c908758733d9f2e0'

const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
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


const abi = [
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "BadRatio",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InsufficientLiquidity",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InsufficientShares",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InvalidAmount",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InvalidFillAmount",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InvalidProportions",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "InvalidTokenAddress",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "NoPosition",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "NotOrderMaker",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "OrderDoesNotExist",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "OrderNotActive",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "PairAlreadyExists",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "PairDoesNotExist",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "ReentrancyGuardReentrantCall",
      "type": "error"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "token",
          "type": "address"
        }
      ],
      "name": "SafeERC20FailedOperation",
      "type": "error"
    },
    {
      "inputs": [],
      "name": "TransferFailed",
      "type": "error"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "orderId",
          "type": "uint256"
        }
      ],
      "name": "LimitOrderCancelled",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "orderId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "filler",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amountFilled",
          "type": "uint256"
        }
      ],
      "name": "LimitOrderFilled",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "orderId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "maker",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "address",
          "name": "offerToken",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "address",
          "name": "desiredToken",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "offerAmount",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "desiredAmount",
          "type": "uint256"
        }
      ],
      "name": "LimitOrderPlaced",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "liquidityProvider",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "shares",
          "type": "uint256"
        }
      ],
      "name": "LiquidityAdded",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "liquidityProvider",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "shares",
          "type": "uint256"
        }
      ],
      "name": "LiquidityRemoved",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        }
      ],
      "name": "PairInitialized",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "reserveA",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "reserveB",
          "type": "uint256"
        }
      ],
      "name": "ReservesUpdated",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "user",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "address",
          "name": "tokenIn",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "address",
          "name": "tokenOut",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "amountOut",
          "type": "uint256"
        }
      ],
      "name": "Swap",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "_pairIdCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        }
      ],
      "name": "addLiquidity",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "shares",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "orderId",
          "type": "uint256"
        }
      ],
      "name": "cancelLimitOrder",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "orderId",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountDesiredToFill",
          "type": "uint256"
        }
      ],
      "name": "fillLimitOrder",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "filled",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        }
      ],
      "name": "getPairId",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        }
      ],
      "name": "getPairInfo",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "reserveA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "reserveB",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "totalShares",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "user",
          "type": "address"
        }
      ],
      "name": "getUserShareBps",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        }
      ],
      "name": "initializePair",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "orderId",
          "type": "uint256"
        }
      ],
      "name": "limitOrders",
      "outputs": [
        {
          "internalType": "address",
          "name": "maker",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "offerToken",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "desiredToken",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "offerAmount",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "desiredAmount",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "active",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "liquidityProvider",
          "type": "address"
        }
      ],
      "name": "liquidityProviderPositions",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "shares",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "hasPosition",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        }
      ],
      "name": "pairs",
      "outputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "reserveA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "reserveB",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "totalShares",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "initialized",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "offerToken",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "offerAmount",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "desiredAmount",
          "type": "uint256"
        }
      ],
      "name": "placeLimitOrder",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "orderId",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "sharesToBurn",
          "type": "uint256"
        }
      ],
      "name": "removeLiquidity",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountA",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountB",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "pairId",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "tokenIn",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amountIn",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "minAmountOut",
          "type": "uint256"
        }
      ],
      "name": "swap",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "amountOut",
          "type": "uint256"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "tokenA",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "tokenB",
          "type": "address"
        }
      ],
      "name": "tokenPairId",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]
export {modal, wagmiAdapter, contractAddress, abi}