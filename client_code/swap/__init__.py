from ._anvil_designer import swapTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class swap(swapTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties['item']
    self.wagmi = properties['wagmi']
    self.invert=False
    self.balance_0 = 0
    self.balance_1=0
    self.allowance_0=0
    self.allowance_1=0
    self.refresh(self.invert)
  def refresh(self, invert):
    self.label_symbol_from.text = "{}".format(self.item['token0_symbol'] if not invert else self.item['token1_symbol'])
    self.label_symbol_to.text= "{}".format(self.item['token1_symbol'] if not invert else self.item['token0_symbol'])
    self.label_exchange_0.text = "{:.5f} {}".format(self.item['0 per 1'] if not invert else self.item['1 per 0'], self.label_symbol_from.text)
    self.label_exchange_1.text = "1 {}".format(self.label_symbol_to.text)
    self.label_balance_from.text =  self.item['token0_symbol'] if not invert else self.item['token1_symbol']
    if self.wagmi.state['address']is None:
      self.button_swap.enabled=False
      self.label_balance_from.text = "0 {}".format(self.label_symbol_from.text)
      self.label_balance_to.text = "0 {}".format(self.label_symbol_to.text)
    else:
      self.balance_0_data = self.wagmi.get_balance_approvals(self.item['token0'], self.wagmi.state['address'])
      self.balance_1_data=self.wagmi.get_balance_approvals(self.item['token1'], self.wagmi.state['address'])
      self.balance_0=self.balance_0_data['balanceOf']
      self.balance_1 = self.balance_1_data['balanceOf']
      self.allowance_0 = self.balance_0_data['allowance']
      self.allowance_1 = self.balance_1_data['allowance']

      self.label_balance_from.text = "{:,.2f} {}".format(self.balance_0/(10**18) if not invert else self.balance_1/(10**18), self.label_symbol_from.text)
      self.label_balance_to.text = "{} {}".format(self.balance_1/(10**18) if not invert else self.balance_0/(10**18), self.label_symbol_to.text)
      self.label_allowance_from.text =  "{} {} approved".format(self.allowance_0/(10**18) if not invert else self.allowance_1/(10**18), self.label_symbol_from.text)
     
    
    

    # Any code you write here will run before the form opens.

  def button_invert_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.invert = not self.invert
    self.refresh(self.invert)

  def text_box_from_change(self, **event_args):
    input= event_args['sender'].text or 0
    self.token_in_amount = int(input*(10**18))
    self.token_in = self.item['token0'] if not self.invert else self.item['token1']
    self.pairId = self.item['pairId']
    ratio = self.item['1 per 0'] if not self.invert else self.item['0 per 1']
    # // Calculate output amount using constant product formula (x * y = k)    dy = (y * dx * 997) / (x * 1000 + dx * 997)
    reserveIn = self.item['reserve0'] if not self.invert else self.item['reserve1']
    actualAmountIn = self.token_in_amount
    reserveOut = self.item['reserve1'] if not self.invert else self.item['reserve0']
    self.amount_out = (reserveOut * ((actualAmountIn * 997) / 1000)) / (reserveIn + ((actualAmountIn * 997) / 1000))

    self.text_box_to.text = float(self.amount_out/(10**18))
    if self.wagmi.state['address'] is not None:
      target = self.allowance_0 if not self.invert else self.allowance_1
      if self.token_in_amount>target:
        self.link_allowance.icon = 'fa:asterisk'
        self.button_swap.enabled=False
      else:
        self.link_allowance.icon = None
        self.button_swap.enabled=True
      tb = self.balance_0 if not self.invert else self.balance_1
      if self.token_in_amount>tb:
        self.text_box_from.role = 'outlined-error'
      else:
        self.text_box_from.role = 'outlined'

  def link_allowance_click(self, **event_args):
    """This method is called when the link is clicked"""
    token = self.item['token0'] if not self.invert else self.item['token1']
    token_symbol = self.item['token0_symbol'] if not self.invert else self.item['token1_symbol']
    spender=self.wagmi.contracts['Liteswap']['address']
    amount = self.token_in_amount
    self.new_allowance = self.wagmi. approve(token, spender, amount)
    Notification("Approved Liteswap to transact {:,.2f} {}".format(amount/(10**18), token_symbol)).show()
    self.refresh(self.invert)
    self.text_box_from_change(sender=self.text_box_from)

  def button_swap_click(self, **event_args):
    """This method is called when the button is clicked"""
    event_args['sender'].enabled=False
    args = [self.pairId, self.token_in, self.token_in_amount, int(self.amount_out*90/100)]
    
    a = self.wagmi.call(self.wagmi.contracts['Liteswap'], 'swap', args)
    if a:
      self.new_item = self.wagmi.get_pair_data(self.item['pairId'])
      self.item['0 per 1'] = self.new_item[2]/self.new_item[3]
      self.item['1 per 0']=1/self.item['0 per 1']
      self.item['reserve0']=self.new_item[2]
      self.item['reserve1']=self.new_item[3]
      
      self.refresh(self.invert)
      self.text_box_from.text=None
      self.text_box_from_change(sender=self.text_box_from)
      
    else:
      event_args['sender'].enabled=True
    
      
    
