from abc import ABC, abstractmethod


class CommandRule(ABC):

    @abstractmethod
    def print_grammer(self, indent=""):
        pass

    @abstractmethod
    def get_valid_rule_set(self) -> list[list[str]]:
        pass


class Command(CommandRule):

    def __init__(self, name):
        self.name = name
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def print_grammer(self, indent=""):
        print(f"{indent} {self.name}")

    def get_valid_rule_set(self) -> list[list[str]]:
        return [[self.name]]


class CommandBook(CommandRule):

    def __init__(self, name):
        self.name = name
        self.commands = []

    def print_grammer(self, indent=""):
        print(f"{indent} {self.name}")
        for command in self.commands:
            command.print_grammer(indent + "--")
        print("")

    def add_command(self, command):
        self.commands.append(command)
        return self

    def remove_command(self, command):
        self.commands.remove(command)
        return self

    def get_valid_rule_set(self) -> list[list[str]]:
        rule_sets = []
        for command in self.commands:
            child_rule_set = command.get_valid_rule_set()
            for crs in child_rule_set:
                crs_copy = crs[:]
                crs_copy.insert(0, self.name)
                rule_sets.append(crs_copy)
        return rule_sets

    def is_valid_rule_set(self, command_list):
        rule_set = self.get_valid_rule_set()
        if command_list in rule_set:
            return True
        else:
            return False


if __name__ == "__main__":
    cb = (
        CommandBook("a")
        .add_command(
            CommandBook("b").add_command(Command("E")).add_command(Command("F"))
        )
        .add_command(CommandBook("C").add_command(Command("D")))
    )
    rule_set = cb.get_valid_rule_set()
    print(rule_set)
    cb.print_grammer()
