from ._anvil_designer import pair_feedTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..wagmi import wagmi
import anvil.js
from ..initialize_liquidity import initialize_liquidity

class pair_feed(pair_feedTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.wagmi = properties['wagmi']
    self.get_pairs()
    self.wagmi.get_test_balances()
  def get_pairs(self):
    self.count = self.wagmi.get_pair_count()
    functions = []
    for i in range(1, self.count):
      print(i)
      #read_functions(self, abb_add, functions)
      function = ("pairs", [i])
      functions.append(function)
    print(functions)
    data = self.wagmi.read_functions(self.wagmi.contracts['Liteswap'], functions)
    
    pairs = []
    print(data)
    n=1
    for k, d in data.items():
      pair = {"token0":d[0], 'token1':d[1], "reserve0":d[2], 'reserve1':d[3], 'shares':d[4], 'pairId':n}
      n+=1
      pairs.append(pair)
   
    self.repeating_panel_1.items = pairs
  
    # Any code you write here will run before the form opens.

  def button_faucet_click(self, **event_args):
    a = anvil.js.await_promise(self.wagmi.call(self.wagmi.contracts['Factory'], 'faucet'))
    print(dir(a))

  def button_initialize_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    self.init_liquidity_page = initialize_liquidity(wagmi=self.wagmi)
    alert(self.init_liquidity_page, large=True, buttons=[])
    