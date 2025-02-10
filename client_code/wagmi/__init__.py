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
    contract = {'abi':abi, 'address':mod.contractAddress}
    arguments = {"contracts":[{**contract, "functionName":'gameId'}, {**contract, "functionName":'entryAmount'}, {**contract, "functionName":'deadline'}]}
    self.data = anvil.js.await_promise(readContracts(self.wagmiAdapter.wagmiConfig, arguments))
    n=0
    self.contract_data = {}
    for d in self.data:
      self.contract_data[arguments['contracts'][n]['functionName']] = d['result']
      n+=1
    self.game_data = self.get_game_data(self.contract_data['gameId'])
    arguments = {**contract, "eventName":"GameEntered", "onLogs":self.log_detected}
    watchContractEvent(self.wagmiAdapter.wagmiConfig, arguments)
    #watchBlocks(self.wagmiAdapter.wagmiConfig, 
              # {'blockTag':'latest', "onBlock":self.block_detected})
    
    
  def block_detected(self, *args, **eargs):
    timestamp = args[0]['timestamp']
    if timestamp>self.game_data['lastTimestamp']+self.contract_data['deadline']:
      self.activate()
  
  def log_detected(self, *args, **eargs):
    self.existing= self.game_data['lastTimestamp']
    self.current_id = self.game_data['gameId']
    a=dict(args[0][0]['args'])
    
    self.game_data['gameId']=a['gameId']
    self.game_data['lastTimestamp']=a['timestamp']
    self.game_data['getNumWinners'] = a['num_winners']
    self.game_data['prizePool']=a['prizePool']
    self.game_data['entrantCount']=a['entrantCount']
    self.game_data['isGameOver'] = False
    
    do_refresh_user=a['entrant'] == self.state['address']
    if self.existing != self.game_data['lastTimestamp']:
      self.refresh_display(do_refresh_user)
      
  def get_game_data(self, gameId):
    contract = {'abi':abi, 'address':mod.contractAddress}
    arguments = {"contracts":[{**contract, "functionName":"getNumWinners", "args":[gameId]}, 
                              {**contract, "functionName":'entrantCount', "args":[gameId]},
                              {**contract, "functionName":'lastTimestamp', "args":[gameId]},
                              {**contract, "functionName":'prizePerWinner', "args":[gameId]},
                              {**contract, "functionName":'prizePool', "args":[gameId]},
                              {**contract, "functionName":"isGameOver", "args":[]}]
                 }
    data = anvil.js.await_promise(readContracts(self.wagmiAdapter.wagmiConfig, arguments))
    n=0
    game_data = {'gameId':gameId}
    for d in data:
      game_data[arguments['contracts'][n]['functionName']] = d['result']
      n+=1
    
    return game_data
  
  

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    num_entries = event_args['num_entries']
    t = 10 if self.game_data['entrantCount']<9 else 1
    a = self.contract_data['entryAmount']*num_entries * t
    tx = {"to":mod.contractAddress, "value":a, "chainId":int(self.state['network'])}
    b = anvil.js.await_promise(sendTransaction(self.wagmiAdapter.wagmiConfig, tx))
    reconnect(self.wagmiAdapter.wagmiConfig)

  
      
  def is_current_complete(self):
    timestamp = anvil.js.await_promise(getBlock(self.wagmiAdapter.wagmiConfig, {"blockTag":"latest"})).timestamp
    return timestamp > self.game_data['lastTimestamp'] + self.contract_data['deadline']    
  def get_all_rounds(self):
    rounds = []
    
    if self.is_current_complete():
      top = self.game_data['gameId']
    else:
      top = self.game_data['gameId']-1
    for n in range(top):
      gd = self.get_game_data(n+1)
      gd['prizePoolFormatted']="{:,} PLS".format(int(gd['prizePool']/(10**18)))
      rounds.append(gd)
    return rounds
  
  def batchClaimVirality(self, args):
    contract = {'abi':abi, 'address':mod.contractAddress}
    ar = {**contract, "functionName":"batchClaimAdoptionBonusPrize", "args":args}
    try:
      a = anvil.js.await_promise(writeContract(self.wagmiAdapter.wagmiConfig, ar))
    except Exception as e:
      Notification(str(e)).show()
  def claimPrize(self, ident):
    game_id = ident[0]
    entryId = ident[1]
    contract = {'abi':abi, 'address':mod.contractAddress}
    ar = {**contract, "functionName":"claimPrize", "args":[game_id, entryId]}
    try:
      a = anvil.js.await_promise(writeContract(self.wagmiAdapter.wagmiConfig, ar))
    except Exception as e:
      Notification(str(e)).show()
  def getWinnerAddress(self, ident):
    game_id = ident[0]
    entryId = ident[1]
    contract = {'abi':abi, 'address':mod.contractAddress}
    arguments = {"contracts":[{**contract, "functionName":"entrants", "args":[game_id, entryId]}, 
                              {**contract, "functionName":'isWinner', "args":[game_id, entryId]},
                              {**contract, "functionName":'hasClaimed', "args":[game_id, entryId]}]}
    data = anvil.js.await_promise(readContracts(self.wagmiAdapter.wagmiConfig, arguments))
    d = {"address":data[0]['result'], 'isWinner':data[1]['result'], 'hasClaimed':data[2]['result']}
    return d

    
  def getUserEntries(self, address, gameId):
    RPC_URL = [n['rpcUrls']['default']['http'][0] for n in self.wagmiAdapter.networks if int(self.state['network']) == n['id']][0]
    provider = ethers.JsonRpcProvider(RPC_URL)
    entrant = address
    contract = ethers.Contract(mod.contractAddress, abi, provider)
    filter = contract.filters.GameEntered(gameId,entrant) 

    es = anvil.js.await_promise(contract.queryFilter(filter, 22630536))
    events = []
    groups = []
    for e in es:
      r = dict(e)['args']
      first = r[3]-(r[7]-1)
      last = r[3]
      groups.append((first, last, dict(e)['transactionHash']))
      for n in range(r[7]):
        events.append(r[3]-n)
    events.sort()
    return groups
  def get_points(self, address):
    contract = {'abi':abi, 'address':mod.contractAddress}
    arguments = {"contracts":[{**contract, "functionName":"participantRecord", "args":[address]},
                             {**contract, "functionName":"leaderboard", "args":[address]}]}
    points = anvil.js.await_promise(readContracts(self.wagmiAdapter.wagmiConfig, arguments))
    d = {"reg points": points[0]['result'], "chad points":points[1]['result']}
    return d
  def getAdoptionBonusClaim(self, game_data, address):
    RPC_URL = [n['rpcUrls']['default']['http'][0] for n in self.wagmiAdapter.networks if int(self.state['network']) == n['id']][0]
    provider = ethers.JsonRpcProvider(RPC_URL)
    gameId = game_data['gameId']
    contract = ethers.Contract(mod.contractAddress, abi, provider)
    filter = contract.filters.ClaimedAdoptionBonus(gameId, address)
    es = anvil.js.await_promise(contract.queryFilter(filter))
    events = []
    payload = []
    claimed = 0
    for e in es:
      
      event = {}
      r = dict(e)['args']
      event["entry_id"] = r[2]
      event["cohort_id"] = r[3]
      event["prize"] = {"raw":r[4], "formatted":r[4]/(10**18)}
      events.append(event)
      payload.append([r[3], r[2]])
      
      claimed+=event['prize']['formatted']
    return events, claimed, payload
  def getAdoptionBonusData(self, game_data):
    gameId = game_data['gameId']
    contract = {'abi':abi, 'address':mod.contractAddress}
    gabd = []
    display_data = {}
    a = []
    b = {}
    
    for n in range(2, (game_data['getNumWinners']  or 1)+2):

      cohort_id = n
      
      kwargs = {"functionName":"adoptionBonusPrizePool", "args":[gameId, cohort_id]}
      b[cohort_id] = {kwargs['functionName']:0}
      a.append(kwargs)
      gabd.append({**contract, **kwargs})
      kwargs = { "functionName":"getAdoptionBonusPrizePerTeam", "args":[gameId, cohort_id]}
      b[cohort_id] = {kwargs['functionName']:0}
      a.append(kwargs)
      gabd.append({**contract, **kwargs})

    data = anvil.js.await_promise(readContracts(self.wagmiAdapter.wagmiConfig, {"contracts":gabd}))
    

    for d in data:
      cohort = a[data.index(d)]['args'][1]
      b[cohort]["split_amongst"]=cohort - 1
      b[cohort][a[data.index(d)]['functionName']] = {"raw":d['result'], "formatted":(d['result'] or 0)/10**18}

    return b
