from kivy.properties import BooleanProperty
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget

Builder.load_file("graphics/upgrades_frame.kv")

class UpgradesTab(Widget):
    pass

class PurchasableUpgrade(Widget):
    is_purchased = BooleanProperty(False)
    
    def purchase(self):
        self.is_purchased = True
        self.ids.purchase_row.remove_widget(self.ids.purchase_button)
        self.ids.active_switch.active = True
        self.update_active_state()

    def update_active_state(self):
        if self.ids.active_switch.active:
            self.app_root.state['active_upgrades'].add(self.upgrade_id)
        else:
            self.app_root.state['active_upgrades'].discard(self.upgrade_id)

class OneTimeUpgrade(Widget):
    pass
