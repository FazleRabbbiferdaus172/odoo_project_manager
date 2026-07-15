from src.odoo_project_manager.options import Options
from src.odoo_project_manager.strategy.strategy import Strategy
from src.odoo_project_manager.strategy.pycharm import PycharmStrategy


class Manager:

    def __init__(self, options):
        import pdb

        pdb.set_trace()
        self.options = Options.auto_built(options)
        self._manager_strategy: Strategy | None = None

    @property
    def manager_strategy(self):
        return self._manager_strategy

    @manager_strategy.setter
    def manager_strategy(self, manage_strategy_obj):
        self._manager_strategy = manage_strategy_obj

    def _config_initial_manager(self):
        if self.options.target_ide == "pycharm":
            self.manager_strategy = PycharmStrategy(self, self.options)

    def execute(self):
        if self.manager_strategy:
            self.manager_strategy.execute()

    @classmethod
    def get_instance(cls, options):
        ins = cls(options)
        ins._config_initial_manager()
        return ins
