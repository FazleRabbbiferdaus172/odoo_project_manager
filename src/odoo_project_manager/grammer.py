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


class CommandLibrary:

    def __init__(self) -> None:
        self._books = {}

    def is_valid_rule_set(self, command_list):
        for book in self._books.values():
            if book.is_valid_rule_set(command_list):
                return True
        return False

    def add_book(self, name, book: CommandBook, forced=False):
        if name in self._books and not forced:
            raise Exception("Book already exists")
        self._books[name] = book
        return self


class CommandLibraryFactory:

    @staticmethod
    def get_command_library():
        cl = CommandLibrary()
        cb_create = CommandBook("create").add_command(Command("project"))
        cl.add_book("create", cb_create)
        return cl


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
    cl = CommandLibraryFactory.get_command_library()
