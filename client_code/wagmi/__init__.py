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
abi  = mod.abi
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
    self.abb_add = {'abi':abi, 'address':mod.contractAddress}
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
    self.contract_address = mod.contractAddress
    
    arguments = {**self.abb_add, "functionName":'_pairIdCount'}
    self.pairIdCount = anvil.js.await_promise(readContract(self.wagmiAdapter.wagmiConfig, arguments))
    
    #arguments = {**contract, "eventName":"GameEntered", "onLogs":self.log_detected}
    #watchContractEvent(self.wagmiAdapter.wagmiConfig, arguments)
    #watchBlocks(self.wagmiAdapter.wagmiConfig, 
              # {'blockTag':'latest', "onBlock":self.block_detected})
    
    
  def block_detected(self, *args, **eargs):
    timestamp = args[0]['timestamp']
  
  def log_detected(self, *args, **eargs):
    pass
    #self.refresh_display(do_refresh_user)
      
  
  
  

  def button_1_click(self, **event_args):
    reconnect(self.wagmiAdapter.wagmiConfig)

  
      
  
  
  def call(self, function_name, args):
    
    ar = {**self.abb_add, "functionName":function_name, "args":args}
    try:
      a = anvil.js.await_promise(writeContract(self.wagmiAdapter.wagmiConfig, ar))
    except Exception as e:
      Notification(str(e)).show()
    
  
  def read_functions(self, functions):
    calls = []
    for f in functions:
      calls.append({**self.abb_add, "functionName": f[0], "args":f[1]})
    
    data = anvil.js.await_promise(readContracts(self.wagmiAdapter.wagmiConfig, calls))
    result = {}
    n=0
    for d in data:
      result[functions.index(n)[0]] = d['result']
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
  
  