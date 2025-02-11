from ._anvil_designer import Form1Template
from anvil import *
from ..wagmi import wagmi
from ..pair_feed import pair_feed
class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.wagmi = wagmi(active_page = self)
    self.add_wallet_button()
  def add_wallet_button(self):
    html = """
      <center id="c">
        <div id="app" style="display: flex; gap: 10px; padding:7px; margin-top:5px; justify-content: center;">
          <appkit-button" ><appkit-button />
        </div>
      </center>
      <script type="module" src="_/theme/main.js"></script>
    """
    self.flow_panel_1.add_component(HtmlTemplate(html=html))
    # Any code you write here will run before the form opens.

  def menu_click(self, **event_args):
    """This method is called when the link is clicked"""
    if event_args['sender'] == self.link_all_pairs:
      self.page = pair_feed(wagmi=self.wagmi)
    elif event_args['sender'] ==self.link_my_positions:
      pass
    self.content_panel.clear()
    self.content_panel.add_component(self.page)