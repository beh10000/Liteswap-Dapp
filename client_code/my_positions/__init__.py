from ._anvil_designer import my_positionsTemplate
from anvil import *


class my_positions(my_positionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
