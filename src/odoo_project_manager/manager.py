from odoo_project_manager.options import Options
from odoo_project_manager.grammer import CommandLibraryFactory
from odoo_project_manager.strategy.strategy import Strategy
from odoo_project_manager.strategy.pycharm import PycharmStrategy
from odoo_project_manager.exception import InvalidCommandError


class Manager:
    command_library = CommandLibraryFactory.get_command_library()

    def __init__(self, options):
        self.options = Options.auto_built(options)
        self.commands = []
        self._manager_strategy: Strategy | None = None

    def varify_command(self, commands):
        if self.command_library.is_valid_rule_set(commands):
            return True
        else:
            raise InvalidCommandError(f"{commands} is not a valid set of command")

    def set_command(self, commands):
        try:
            self.varify_command(commands)
            self.commands = commands
        except InvalidCommandError as error:
            raise error

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
    def get_instance(cls, options, command):
        ins = cls(options)
        try:
            ins.set_command(command)
        except InvalidCommandError as error:
            raise error
        ins._config_initial_manager()
        return ins
