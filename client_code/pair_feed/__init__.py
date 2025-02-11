from ._anvil_designer import pair_feedTemplate
from anvil import *


class pair_feed(pair_feedTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
