from ._anvil_designer import add_liquidityTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..liquidity_position_card import liquidity_position_card

class add_liquidity(add_liquidityTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties['item']
    self.item['0 per 1']=self.item['reserve0']/self.item['reserve1']
    self.item['1 per 0']=1/self.item['0 per 1']
    self.add_component(Label(text=self.item))
    self.wagmi = properties['wagmi']
    self.refresh()
  def refresh(self):
    self.label_token_0.text = self.item['token0_symbol']
    self.label_token_1.text = self.item['token1_symbol']
    self.label_exchange_0.text = "{} {} per {}".format(self.item['1 per 0'], self.item['token1_symbol'], self.item['token0_symbol'])
    if self.wagmi.state['address'] is not None:
      self.token_0_data = self.wagmi.get_balance_approvals(self.item['token0'], self.wagmi.state['address'])
      self.token_1_data = self.wagmi.get_balance_approvals(self.item['token1'], self.wagmi.state['address'])

      self.allowance_0=self.token_0_data['allowance']
      self.allowance_1=self.token_1_data['allowance']
      self.label_balance_0.text = "{:,.2f} {}".format(self.token_0_data['balanceOf']/(10**18), self.token_0_data['symbol'])
      
      self.label_approved_0.text = "{:,.2f} {}".format(self.token_0_data['allowance']/(10**18), self.token_0_data['symbol'])
      self.label_balance_1.text = "{:,.2f} {}".format(self.token_1_data['balanceOf']/(10**18), self.token_1_data['symbol'])
      
      self.label_approved_1.text = "{:,.2f} {}".format(self.token_1_data['allowance']/(10**18), self.token_1_data['symbol'])
      self.user_shares = self.wagmi.get_shares(self.item['pairId'], self.wagmi.state['address'])
      if self.user_shares>0:
        self.column_panel_position.clear()
        self.column_panel_position.add_component(liquidity_position_card(item=self.item, wagmi=self.wagmi, user_shares = self.user_shares, page=self))
    # Any code you write here will run before the form opens.

  def text_box_0_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.input = event_args['sender'].text
    self.input_raw = int(self.input * (10**18))
    self.other = self.input * self.item['1 per 0']
    self.text_box_1.text = self.other
    buffer = 1.05
    self.other_raw = int(self.input_raw * self.item['1 per 0']*buffer)

  def button_add_liquidity_click(self, **event_args):
    if self.wagmi.state['address'] is None:
      Notification("Must be connected with wallet.").show()
      return False
    if self.input_raw>self.allowance_0 or self.other_raw>self.allowance_1:
      Notification("Insufficient allowance, please approve the suggested amount.").show()
      return False
    a = self.wagmi.call(self.wagmi.contracts['Liteswap'], 'addLiquidity', [self.item['pairId'], self.input_raw])
    if a:
      self.refresh()
    else:
      Notification("Transaction not completed.").show()
    
