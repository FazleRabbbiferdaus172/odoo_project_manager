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
        self.get_odoo_source_directory()

    def set_root_directory(self):
        """
        sets program root directory, that help with determining bin directory and sample directory.
        """
        current_file = os.path.abspath(__file__)
        self.root_directory = os.path.dirname(os.path.dirname(current_file))

    def set_project_path(self):
        """
        sets the root path of project to be created
        """
        self.project_path = os.path.join(
            self.options.output_location, self.options.project_name
        )

    def set_bin_directory(self):
        """
        sets the bin directory path
        """
        self.bin_directory = os.path.join(self.root_directory, "bin")

    def get_odoo_source_directory(self):
        """
        calls the script to determine the odoo path in current machine and sets the odoo path.
        """
        get_odoo_source_script = os.path.join(self.bin_directory, "get_odoo_source.sh")
        resutl = subprocess.run(
            [get_odoo_source_script, self.options.version],
            text=True,
            capture_output=True,
        )
        self.odoo_path = os.path.join("" + resutl.stdout.strip())

    def run_create(self):
        """
        handles project creattion and coresponds to create project command.
        """
        self.create_directory()
        self.pull_source()
        self.create_virtual_env()
        self.install_requirements()
        self.copy_or_generate_configuration_file()

    def create_directory(self):
        """
        creates a project directory.
        """
        try:
            os.mkdir(self.project_path)
        except Exception as error:
            _logging.warning(error)

    def pull_source(self):
        """
        pull the source code of project in a sub project directory.
        """
        to_clone_path = os.path.join(
            self.project_path, self.options.project_name.upper()
        )
        git_pull_script = os.path.join(self.bin_directory, "git_pull.sh")
        subprocess.call(
            [
                git_pull_script,
                self.options.source_location,
                to_clone_path,
            ]
        )

    def create_virtual_env(self):
        """
        create a virual env in the project root directory
        """
        script_path = os.path.join(self.bin_directory, "create_virtual_env.sh")
        subprocess.call([script_path, self.project_path])

    def install_requirements(self):
        """
        installs the required odoo packages in the virtual env
        """
        script_path = os.path.join(self.bin_directory, "install_odoo_requirement.sh")
        venv_path = os.path.join(self.project_path, ".venv", "bin")
        subprocess.call([script_path, self.odoo_path, venv_path])

    def copy_or_generate_configuration_file(self):
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
