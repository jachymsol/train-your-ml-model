from kivy.properties import BooleanProperty, StringProperty
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget

from utils.yaml_utils import get_local_upgrade

Builder.load_file("graphics/upgrades_frame.kv")

class UpgradesTab(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def on_kv_post(self, base_widget):
        upgrades = get_local_upgrade()

        for upgrade in upgrades:
            if upgrades[upgrade]['type'] == 'permanent':
                self.ids.permanent_upgrades.add_widget(PurchasableUpgrade(upgrade, upgrades[upgrade], self.app_root))
            elif upgrades[upgrade]['type'] == 'single_use':
                self.ids.single_use_upgrades.add_widget(SingleUseUpgrade(upgrade, upgrades[upgrade], self.app_root))
        self.ids.permanent_upgrades.add_widget(Widget())
        self.ids.single_use_upgrades.add_widget(Widget())

        return super().on_kv_post(base_widget)

class PurchasableUpgrade(Widget):
    is_purchased = BooleanProperty(False)
    full_display_name = StringProperty('')

    def __init__(self, upgrade_id, upgrade, app_root, **kwargs):
        super().__init__(**kwargs)

        self.upgrade_id = upgrade_id
        self.display_name = upgrade['display_name']
        self.abbreviation = upgrade['abbreviation']
        self.cost = upgrade['cost']

        self.app_root = app_root
    
    def purchase(self):
        if self.app_root.state['coins'] >= self.cost:
            self.app_root.add_coins(-self.cost)
            self.is_purchased = True
            self.ids.purchase_row.remove_widget(self.ids.purchase_button)
            self.ids.purchase_row.add_widget(Widget())
            self.ids.active_switch.state = 'down'
            self.update_active_state()

    def update_active_state(self):
        if self.ids.active_switch.state == 'down':
            self.app_root.state['active_upgrades'].add(self.upgrade_id)
        else:
            self.app_root.state['active_upgrades'].discard(self.upgrade_id)

class SingleUseUpgrade(Widget):
    def __init__(self, upgrade_id, upgrade, app_root, **kwargs):
        super().__init__(**kwargs)

        self.upgrade_id = upgrade_id
        self.display_name = upgrade['display_name']
        self.cost = upgrade['cost']
        self.callback = upgrade['callback']

        self.app_root = app_root
    
    def purchase(self):
        if(self.app_root.state['coins'] >= self.cost):
            self.app_root.add_coins(-self.cost)
            self.ids.purchase_button.disabled = True
            self.ids.purchase_button.background_color = (0, 1, 0, 1)
            # eval(self.callback)
            Clock.schedule_once(self.enable_purchase, 1)
    
    def enable_purchase(self, _):
        self.ids.purchase_button.disabled = False
        self.ids.purchase_button.background_color = (1, 1, 1, 1)
