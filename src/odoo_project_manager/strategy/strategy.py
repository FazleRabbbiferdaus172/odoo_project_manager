import os
import subprocess
import logging
from abc import ABC, abstractmethod

from src.odoo_project_manager.options import Options

_logging = logging.getLogger(__name__)


class Strategy(ABC):
    def __init__(self, manager, options: Options):
        self.manager = manager
        self.options = options
        self.set_root_directory()
        self.set_bin_directory()
        self.set_project_path()

    def set_root_directory(self):
        current_file = os.path.abspath(__file__)
        self.root_directory = os.path.dirname(os.path.dirname(current_file))

    def set_project_path(self):
        self.project_path = os.path.join(
            self.options.output_location, self.options.project_name
        )

    def set_bin_directory(self):
        self.bin_directory = os.path.join(self.root_directory, "bin")

    def create_directory(self):
        try:
            os.mkdir(self.project_path)
        except Exception as error:
            _logging.warning(error)

    def run_create(self):
        self.create_directory()
        self.pull_source()
        self.create_virtual_env()
        self.install_requirements()
        self.copy_configuration_file()

    def pull_source(self):
        git_pull_script = os.path.join(self.bin_directory, "git_pull.sh")
        subprocess.call(
            [
                git_pull_script,
                self.options.source_location,
                self.project_path,
            ]
        )

    def create_virtual_env(self):
        script_path = os.path.join(self.bin_directory, "create_virtual_env.sh")
        subprocess.call([script_path, self.project_path])

    def install_requirements(self):
        pass

    def copy_configuration_file(self):
        pass

    def execute(self):
        self.pre_execute()
        if self.manager.commands == ["create", "project"]:
            self.run_create()

        self.post_execute()

    def pre_execute(self):
        """
        ment to be overriden by concreate classes
        """
        pass

    def post_execute(self):
        """
        ment to be overriden by concreate classes
        """
        pass
