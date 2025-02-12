from ._anvil_designer import limit_order_cardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class limit_order_card(limit_order_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties['item']
    self.wagmi = properties['wagmi']
    self.refresh()
  def refresh(self):
    self.label_order_id.text = "Order ID #{}".format(self.item['orderId'])
    self.label_description.text = "Offered {:,.2f} {} for {:,.2f} {}".format(self.item['offerAmount']/(10**18), self.item['offerTokenSymbol'], self.item['desiredAmount']/(10**18), self.item['desiredTokenSymbol'])
    self.percent_filled = 100*(self.item['desiredAmount']-self.item['amountRemaining'])/self.item['desiredAmount']
    if self.item['active']:
      self.label_progress.text = "{:.2f}% Filled".format(self.percent_filled)
    else:
      self.label_progress.text = "Order Cancelled"
      self.button_cancel.visible=False
    
    # Any code you write here will run before the form opens.

  def button_cancel_click(self, **event_args):
    """This method is called when the button is clicked"""
    args = [
      self.item['pairId'],
      self.item['orderId']
    ]
    a = self.wagmi.call(self.wagmi.contracts["Liteswap"], "cancelLimitOrder", args)
    if a:
      self.item['active']=False
      self.refresh()