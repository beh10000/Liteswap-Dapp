from ._anvil_designer import add_liquidityTemplate
from anvil import *


class add_liquidity(add_liquidityTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
