from src.odoo_project_manager.options import Options
from src.odoo_project_manager.strategy.strategy import Strategy


class PycharmStrategy(Strategy):

    def __init__(self, options: Options):
        self.options = options

    def execute(self):
        print("executed")
