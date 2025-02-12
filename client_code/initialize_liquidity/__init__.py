from ._anvil_designer import initialize_liquidityTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class initialize_liquidity(initialize_liquidityTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.wagmi=properties['wagmi']
    self.tokens = ["GOLD", "SILVER", "BRONZE", "COPPER", "IRON"]
    self.token_1_data=None
    self.token_2_data=None
    self.amount_1_raw = 0
    self.amount_2_raw = 0
    self.dd = []
    for t in self.tokens:
      r = (t, self.wagmi.contracts[t]['address'])
      self.dd.append(r)
    self.drop_down_1.items = self.dd
    self.drop_down_2.items = self.dd
    

    # Any code you write here will run before the form opens.

  def drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    if event_args['sender']==self.drop_down_1:
      self.text_box_1.text =event_args['sender'].selected_value
      self.text_box_1_change(sender=self.text_box_1)
    if event_args['sender']==self.drop_down_2:
      self.text_box_2.text = event_args['sender'].selected_value
      self.text_box_2_change(sender=self.text_box_2)
      
    if self.text_box_1.text == self.text_box_2.text:
      self.text_box_2.role = 'outlined-error'
    else:
      self.text_box_2.role = 'outlined'

  
  def text_box_amount_1_change(self, **event_args):
    if event_args['sender'].text in [None, ""]:
      self.amount_1_input = 0
    else:
      self.amount_1_input = event_args['sender'].text
    self.amount_1_raw =int(self.amount_1_input*(10**18))
    self.a_good = self.token_1_data['allowance']>self.amount_1_raw

  
  def text_box_2_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.token_2_data = self.wagmi.get_balance_approvals(self.text_box_2.text, self.wagmi.state['address'])
    self.label_balance_2.text = "{:,.2f} {}".format(self.token_2_data['balanceOf']/(10**18), self.token_2_data['symbol'])
    self.text_box_amount_2.enabled = self.text_box_2.text not in [None, ""]
    self.label_approved_b.text = "{:,.2f} {}".format(self.token_2_data['allowance']/(10**18), self.token_2_data['symbol'])
    self.b_good = self.token_2_data['allowance']>self.amount_2_raw

  def button_initialize_click(self, **event_args):
    """This method is called when the button is clicked"""
    a = None not in [self.token_1_data, self.token_2_data]
    if a:
      pass
    else:
      Notification("Must Select Two Tokens").show()
      return False
    b = 0 not in [self.amount_1_raw, self.amount_2_raw]
    if not b:
      Notification("Must be greater than 0.").show()
    c = all([self.token_1_data['allowance']>=self.amount_1_raw, self.token_2_data['allowance']>=self.amount_2_raw])
    if not c:
      Notification("Allowances must be greater than or equal to input amount.").show()
    if all([a,b,c]):
      #address tokenA, address tokenB, uint256 amountA, uint256 amountB
      a = self.wagmi.call(self.wagmi.contracts['Liteswap'], "initializePair",[self.token_1_data['address'], self.token_2_data['address'], self.amount_1_raw, self.amount_2_raw] )
      if a:
        self.raise_event("x-close-alert", value=True)
        get_open_form().menu_click(sender=get_open_form().link_all_pairs)
    else:
      Notification("Must have adequate approvals for selected tokens").show()
      return False
  def text_box_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    
    self.token_1_data = self.wagmi.get_balance_approvals(self.text_box_1.text, self.wagmi.state['address'])
    self.label_balance_1.text = "{:,.2f} {}".format(self.token_1_data['balanceOf']/(10**18), self.token_1_data['symbol'])
    self.text_box_amount_1.enabled = self.text_box_1.text not in [None, ""]
    self.label_approved_a.text = "{:,.2f} {}".format(self.token_1_data['allowance']/(10**18), self.token_1_data['symbol'])
  def text_box_amount_2_change(self, **event_args):
    if event_args['sender'].text in [None, ""]:
      self.amount_2_input = 0
    else:
      self.amount_2_input = event_args['sender'].text
    self.amount_2_raw =int(self.amount_2_input*(10**18))
    self.b_good = self.token_2_data['allowance']>self.amount_2_raw

  def button_approve_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    token = self.token_1_data['address']
    spender = self.wagmi.contracts['Liteswap']['address']
    amount=self.amount_1_raw
    new_allowance = self.wagmi.approve(token, spender, amount)
    
    self.token_1_data['allowance']=new_allowance
    self.label_approved_a.text = "{:,.2f} {}".format(self.token_1_data['allowance']/(10**18), self.token_1_data['symbol'])
    self.a_good = self.token_1_data['allowance']>self.amount_1_raw

  def button_approve_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    token = self.token_2_data['address']
    spender = self.wagmi.contracts['Liteswap']['address']
    amount=self.amount_2_raw
    new_allowance = self.wagmi.approve(token, spender, amount)
    
    self.token_2_data['allowance']=new_allowance
    self.label_approved_b.text = "{:,.2f} {}".format(self.token_2_data['allowance']/(10**18), self.token_2_data['symbol'])
    self.b_good = self.token_2_data['allowance']>self.amount_2_raw