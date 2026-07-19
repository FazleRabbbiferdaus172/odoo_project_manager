from src.odoo_project_manager.options import Options
from src.odoo_project_manager.strategy.strategy import Strategy


class PycharmStrategy(Strategy):

    def __init__(self, manager, options: Options):
        super().__init__(manager, options)

    def execute(self):
        super().execute()
        print(f"executed:  {self.manager.commands} options {self.manager.options}")
