from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget

import utils.model_utils as model_utils

Builder.load_file("graphics/evaluation_frame.kv")

class EvaluationsTab(Widget):
    def new_evaluation(self):
        model_index = len(self.app_root.state['evaluations'])
        evaluation_row = EvaluationRow(app_root=self.app_root, model_index=model_index)
        self.ids.evaluation_results.height += evaluation_row.height
        self.ids.evaluation_results.add_widget(evaluation_row)

        def create_model_and_display(_):
            model = model_utils.create_train_and_evaluate(self.app_root.state['active_upgrades'])
            
            self.app_root.state['evaluations'].append(model)
            evaluation_row.loading = False

        Clock.schedule_once(create_model_and_display)


class EvaluationRow(Widget):
    def __init__(self, app_root, model_index, **kwargs):
        super().__init__(**kwargs)

        self.app_root = app_root
        self.model_index = model_index
        self.initialized = True
    
    def get_active_upgrades(self):
        if len(self.app_root.state['active_upgrades']) == 0:
            return "None"
        return ', '.join(self.app_root.state['active_upgrades'])

    def get_accuracy(self):
        return str(round(self.app_root.state['evaluations'][self.model_index]['accuracy'], 2) * 100) + '%'
