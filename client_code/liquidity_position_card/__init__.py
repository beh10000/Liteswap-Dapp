from ._anvil_designer import liquidity_position_cardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class liquidity_position_card(liquidity_position_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties["item"]
    self.wagmi = properties["wagmi"]
    self.user_shares = properties['user_shares']
    self.page = properties['page']
    self.refresh()

  def refresh(self):
    
    self.percent_filled = (
      100
      * self.user_shares
      / self.item["shares"]
    )
    self.label_description.text = "You own {:,.2f} of {:,.2f} total liquidity pool shares, roughly {:.2f}%.".format(
      self.user_shares / (10**18),
      self.item["shares"] / (10**18),
      self.percent_filled
    )
    
    self.label_progress.text = "Your shares can currently claim {:,.2f} {} and {:,.2f} {}.".format(int(self.percent_filled*self.item['reserve0']/((10**18)*100)), self.item['token0_symbol'],int(self.percent_filled*self.item['reserve1']/((10**18)*100)), self.item['token1_symbol'])
    

    # Any code you write here will run before the form opens.

  def button_cancel_click(self, **event_args):
    """This method is called when the button is clicked"""
    args = [self.item["pairId"], int((10**18)*self.text_box_shares.text)]
    a = self.wagmi.call(self.wagmi.contracts["Liteswap"], "removeLiquidity", args)
    if a:
      self.page.refresh()
