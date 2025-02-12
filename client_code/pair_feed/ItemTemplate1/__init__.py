from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...swap import swap
from ...add_liquidity import add_liquidity
from ...limit_order import limit_order

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.wagmi = get_open_form().wagmi
    self.default=True
    self.refresh_display()
    
  def get_info(self):
    
    abb_add={'abi':self.wagmi.contracts['ERC20']['abi'], 'address':self.item['token0']}
    data0 = self.wagmi.read_functions(abb_add, [("name", []), ("symbol", [])])
    abb_add={'abi':self.wagmi.contracts['ERC20']['abi'], 'address':self.item['token1']}
    data1 = self.wagmi.read_functions(abb_add, [("name", []), ("symbol", [])])
    self.item['token0_name']=data0['name']
    self.item['token0_symbol']=data0['symbol']
    self.item['token1_name']=data1['name']
    self.item['token1_symbol']=data1['symbol']
    self.item['0 per 1']=self.item['reserve0']/self.item['reserve1']
    self.item['1 per 0']=1/self.item['0 per 1']
    
  def refresh_display(self):
    self.get_info()
    self.label_pair_symbols.text = "{}/{}".format(self.item['token0_symbol'], self.item['token1_symbol'])
    self.label_pair_names.text = "{}/{}".format(self.item['token0_name'], self.item['token1_name'])
    self.label_token_a.text = self.item['token0_symbol']
    self.label_token_b.text = self.item['token1_symbol']
    self.label_ca_a.text = "{}...{}".format(self.item['token0'][0:4], self.item['token0'][-4:])
    self.label_ca_b.text = "{}...{}".format(self.item['token1'][0:4], self.item['token1'][-4:])
    if self.default:
      self.label_pair_ratio.text = "{:.3f} {} per {}".format(self.item['0 per 1'], self.item['token0_symbol'], self.item['token1_symbol'])
    else:
      self.label_pair_ratio.text = "{:.3f} {} per {}".format(self.item['1 per 0'], self.item['token1_symbol'], self.item['token0_symbol'])

    # Any code you write here will run before the form opens.

  def menu_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.selected = event_args['sender']
    
      
    if self.selected ==self.button_trade:
      self.page = swap(wagmi=self.wagmi, item=self.item)
      title = "Swap Tokens"
    if self.selected==self.button_lp:
      self.page = add_liquidity(wagmi=self.wagmi, item=self.item)
      title = "Manage Liquidity"
    if self.selected==self.button_limit_order:
      self.page = limit_order(wagmi=self.wagmi, item=self.item)
      title = "Place Limit Order"
    #self.column_panel_actions.clear()
    #self.column_panel_actions.add_component(self.page)
    alert(self.page, large=True,title=title, buttons=None)

  def link_switch_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.default=not self.default
    if self.default:
      self.label_pair_ratio.text = "{:.3f} {} per {}".format(self.item['0 per 1'], self.item['token0_symbol'], self.item['token1_symbol'])
    else:
      self.label_pair_ratio.text = "{:.3f} {} per {}".format(self.item['1 per 0'], self.item['token1_symbol'], self.item['token0_symbol'])
