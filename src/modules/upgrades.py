from kivy.properties import BooleanProperty, StringProperty
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from utils.yaml_utils import get_local_upgrade

Builder.load_file("graphics/upgrades_frame.kv")

class UpgradesTab(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_kv_post(self, base_widget):
        upgrades = get_local_upgrade()

        for upgrade in upgrades:
            self.ids.permanent_upgrades.add_widget(PurchasableUpgrade(upgrade, upgrades[upgrade], self.app_root))
        self.ids.permanent_upgrades.add_widget(Widget())

        return super().on_kv_post(base_widget)

class PurchasableUpgrade(Widget):
    is_purchased = BooleanProperty(False)
    full_display_name = StringProperty('')

    def __init__(self, upgrade_id, upgrade, app_root, **kwargs):
        super().__init__(**kwargs)

        self.upgrade_id = upgrade_id
        self.display_name = upgrade['display_name']
        self.abbreviation = upgrade['abbreviation']
        self.full_display_name = f"({self.abbreviation}) {self.display_name}"

        self.app_root = app_root
    
    def purchase(self):
        self.is_purchased = True
        self.ids.purchase_row.remove_widget(self.ids.purchase_button)
        self.ids.purchase_row.add_widget(Label(text=f"({self.abbreviation})", size_hint=(.5, 1)))
        self.ids.active_switch.active = True
        self.update_active_state()

    def update_active_state(self):
        if self.ids.active_switch.active:
            self.app_root.state['active_upgrades'].add(self.upgrade_id)
        else:
            self.app_root.state['active_upgrades'].discard(self.upgrade_id)

class OneTimeUpgrade(Widget):
    pass
