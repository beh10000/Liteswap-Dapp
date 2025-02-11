from ._anvil_designer import pair_feedTemplate
from anvil import *
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
