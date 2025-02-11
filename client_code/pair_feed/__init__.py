from ._anvil_designer import pair_feedTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..wagmi import wagmi

class pair_feed(pair_feedTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.wagmi = properties['wagmi']
    self.get_pairs()
  def get_pairs(self):
    print(self.wagmi.pairIdCount)
  
    # Any code you write here will run before the form opens.

  def button_faucet_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.wagmi.call('Factory', 'faucet')
