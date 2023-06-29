from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.label import Label

import utils.model_utils as model_utils
from utils.yaml_utils import get_local_upgrade

Builder.load_file("graphics/evaluation_frame.kv")

class EvaluationsTab(Widget):
    def new_evaluation(self):
        model_index = len(self.app_root.state['evaluations'])
        evaluation_row = EvaluationRow(app_root=self.app_root, model_index=model_index)
        self.ids.evaluation_results.height += evaluation_row.height
        self.ids.evaluation_results.add_widget(evaluation_row)

        def create_model_and_display(_):
            model = model_utils.create_train_and_evaluate(self.app_root.state['active_upgrades'], self.app_root.state_folder)
            
            self.app_root.state['evaluations'].append(model)
            evaluation_row.loading = False

        Clock.schedule_once(create_model_and_display)


class EvaluationRow(Widget):
    def __init__(self, app_root, model_index, **kwargs):
        super().__init__(**kwargs)

        self.app_root = app_root
        self.model_index = model_index
        self.initialized = True
    
    def purchase_test_model(self):
        if(self.app_root.state['coins'] >= self.test_cost):
            self.app_root.add_coins(-self.test_cost)
            self.ids.purchase_test_button.background_color = (0, 1, 0, 1)

            Clock.schedule_once(self.test_model)

    def test_model(self, _):
        evaluation = self.app_root.state['evaluations'][self.model_index]
        result = model_utils.test(evaluation['model_path'], evaluation['active_upgrades'])

        self.app_root.state['evaluations'][self.model_index]['test_accuracy'] = result
        self.display_test_accuracy()
        
    def display_test_accuracy(self):
        self.children[0].remove_widget(self.ids.purchase_test_button)
        self.children[0].add_widget(Label(text=self.get_accuracy(test=True)))
    
    def get_active_upgrades(self):
        if len(self.app_root.state['evaluations'][self.model_index]['active_upgrades']) == 0:
            return "-"
        
        active_upgrade_ids = self.app_root.state['evaluations'][self.model_index]['active_upgrades']
        active_upgrade_abbreviations = [f"({get_local_upgrade(upgrade_id)['abbreviation']})" for upgrade_id in active_upgrade_ids]
        return ', '.join(active_upgrade_abbreviations)

    def get_accuracy(self, test=False):
        return str(round(self.app_root.state['evaluations'][self.model_index]['test_accuracy' if test else 'train_accuracy'] * 100, 1)) + '%'
