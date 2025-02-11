from ._anvil_designer import add_liquidityTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class add_liquidity(add_liquidityTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = properties['item']
    self.wagmi = properties['wagmi']
    

    # Any code you write here will run before the form opens.
