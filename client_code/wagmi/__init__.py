from ._anvil_designer import wagmiTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.js
import anvil
import time
mod  = anvil.js.import_from("/_/theme/main.js")
core = anvil.js.import_from('@wagmi/core')
watchContractEvent = core.watchContractEvent
watchBlocks = core.watchBlocks
writeContract = core.writeContract
readContract = anvil.js.import_from("@wagmi/core").readContract
readContracts = anvil.js.import_from("@wagmi/core").readContracts
sendTransaction = anvil.js.import_from("@wagmi/core").sendTransaction
reconnect = anvil.js.import_from("@wagmi/core").reconnect
ethers = anvil.js.import_from("ethers")
getBlock =core.getBlock

class wagmi(wagmiTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.active_page = properties['active_page']
    contracts = app_tables.contracts.search()
    self.contracts = {}
    for c in contracts:
      self.contracts[c['name']]={"abi":c['abi'], 'address':c['address']}
    self.address = None
    self.signer = None
    self.state = {'caipAddress': None, 'address': None, 'isConnected': False, 'status': None, 'network':None}
    self.modal = mod.modal
    self.wagmiAdapter = mod.wagmiAdapter
    reconnect(self.wagmiAdapter.wagmiConfig)
    self.activate()
    reconnect(self.wagmiAdapter.wagmiConfig)
   
    

  def new_account(self, *args):
    state = dict(args[0])
    network = None if state['caipAddress'] is None else state['caipAddress'].split(":")[1]
    state['network'] = network
    self.state = state
    
  def refresh_display(self, refresh_user=True):
    
    pass
    
    
  def activate(self, *args, **event_args):
    self.modal.subscribeAccount(self.new_account)
    
    abb_add = self.contracts['Liteswap']
    self.contract_address = abb_add['address']
    arguments = {**abb_add, "functionName":'_pairIdCount'}
    self.pairIdCount = anvil.js.await_promise(readContract(self.wagmiAdapter.wagmiConfig, arguments))
    tokens = ["GOLD", "SILVER", "BRONZE", "COPPER", "IRON"]
    data = self.read_functions(self.contracts['Factory'], list([(t, []) for t in tokens]))
    for t in tokens:
      address = data[t]
      self.contracts[t]={'abi':self.contracts["ERC20"]['abi'], 'address':address}
    
    #arguments = {**contract, "eventName":"GameEntered", "onLogs":self.log_detected}
    #watchContractEvent(self.wagmiAdapter.wagmiConfig, arguments)
    #watchBlocks(self.wagmiAdapter.wagmiConfig, 
              # {'blockTag':'latest', "onBlock":self.block_detected})
    
  def get_pair_count(self):
    abb_add = self.contracts['Liteswap']
    arguments = {**abb_add, "functionName":'_pairIdCount'}
    self.pairIdCount = anvil.js.await_promise(readContract(self.wagmiAdapter.wagmiConfig, arguments))
    return self.pairIdCount
  def block_detected(self, *args, **eargs):
    timestamp = args[0]['timestamp']
  
  def log_detected(self, *args, **eargs):
    pass
    #self.refresh_display(do_refresh_user)
      
  
  
  

  def button_1_click(self, **event_args):
    reconnect(self.wagmiAdapter.wagmiConfig)

  
      
  
  
  def call(self, abb_add, function_name, args=[]):
    
    ar = {**abb_add, "functionName":function_name, "args":args}
    try:
      a = anvil.js.await_promise(writeContract(self.wagmiAdapter.wagmiConfig, ar))
      return True
    except Exception as e:
      Notification(str(e)).show()
      return False
  def get_balance_approvals(self, token, user):
    abb_add = {'abi':self.contracts['ERC20']['abi'], 'address':token}
    response = self.read_functions(abb_add, [('symbol', []), ("balanceOf", [user]), ("allowance", [user, self.contracts['Liteswap']['address']])])
    response['address']=token
    return response
  def get_balance(self, token, user):
    abb_add = {'abi':self.contracts['ERC20']['abi'], 'address':token}
    arguments = {**abb_add, "functionName":'balanceOf', 'args':[user]}
    
    self.balance = anvil.js.await_promise(readContract(self.wagmiAdapter.wagmiConfig, arguments))

    return self.balance
  def get_test_balances(self):
    calls = []
    tokens = ["GOLD", "SILVER", "BRONZE", "COPPER", "IRON"]
    for t in tokens:
      calls.append({**self.contracts[t], 'functionName':'balanceOf', "args":[self.state['address']]})
    bal = anvil.js.await_promise(readContracts(self.wagmiAdapter.wagmiConfig, {"contracts":calls}))
    balances ={}
    for t in tokens:
      balances[t]=bal[tokens.index(t)]['result']      
    print(balances)
    return balances
  def approve(self, token, spender, amount):
    abb_add = {'abi':self.contracts["ERC20"]['abi'], 'address':token}
    self.call(abb_add, 'approve', [spender, amount])
    
    arguments = {**abb_add, "functionName":'allowance', "args":[self.state['address'], spender]}
    allowance = anvil.js.await_promise(readContract(self.wagmiAdapter.wagmiConfig, arguments))
    print(allowance)
    return allowance
  def read_functions(self, abb_add, functions):
    
    calls = []
    fn_names=[]
    same_names = False
    for f in functions:
      if f[0] in fn_names:
        same_names=True
      fn_names.append(f[0])
      calls.append({**abb_add, "functionName": f[0], "args":f[1]})
    
    data = anvil.js.await_promise(readContracts(self.wagmiAdapter.wagmiConfig, {"contracts":calls}))
    print(data)
    result = {}
    n=0
    for d in data:
      key = "{}".format(functions[n]) if same_names else functions[n][0]
      result[key] = d['result']
      n+=1
    return result

    
  def get_initialized_pairs(self):
    RPC_URL = [n['rpcUrls']['default']['http'][0] for n in self.wagmiAdapter.networks if int(self.state['network']) == n['id']][0]
    provider = ethers.JsonRpcProvider(RPC_URL)
    contract = ethers.Contract(mod.contractAddress, abi, provider)
    filter = contract.filters.PairInitialized()
    es = anvil.js.await_promise(contract.queryFilter(filter))
    events = []
    fn_calls = []
    
    n = 0
    for e in es:
      r = {"pairId":e['args'][0], "token0":e['args'][1], "token1":e['args'][2]}
      events.append(r)
      fn = ("getPairInfo", [r['pairId']])
      fn_calls.append(fn)
      n+=1
    return events
  def get_liquidity_events(self, pairId, address=None):
    RPC_URL = [n['rpcUrls']['default']['http'][0] for n in self.wagmiAdapter.networks if int(self.state['network']) == n['id']][0]
    provider = ethers.JsonRpcProvider(RPC_URL)
    contract = ethers.Contract(mod.contractAddress, abi, provider)
    arg = [pairId, address] if address is not None else [pairId]
    add_filter = contract.filters.LiquidityAdded(*arg)
    rem_filter = contract.filters.LiquidityRemoved(*arg)
    
    add_events = anvil.js.await_promise(contract.queryFilter(add_filter))
    rem_events = anvil.js.await_promise(contract.queryFilter(rem_filter))
    
    adds = [e['args'] for e in add_events]
    rems = [e['args'] for e in rem_events]
    return adds, rems
  def get_swap_events(pairId, address=None):
    RPC_URL = [n['rpcUrls']['default']['http'][0] for n in self.wagmiAdapter.networks if int(self.state['network']) == n['id']][0]
    provider = ethers.JsonRpcProvider(RPC_URL)
    contract = ethers.Contract(mod.contractAddress, abi, provider)
    arg = [pairId, address] if address is not None else [pairId]
    swap_events =contract.filters.Swap(*arg)
  
  