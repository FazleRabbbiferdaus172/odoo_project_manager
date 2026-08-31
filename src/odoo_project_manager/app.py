import sys
import getopt
import typer

from odoo_project_manager.manager import Manager
from odoo_project_manager.command.project import app as project_app

app = typer.Typer()


@app.command()
def cli():
    args = sys.argv
    options = "hs:l:e:n:"
    long_versions = ["help", "output-lcoation=", "edition=", "project-source=", "name="]
    arg_options, arg_vals = getopt.gnu_getopt(args[1:], options, long_versions)
    manager = Manager.get_instance(arg_options, arg_vals)
    manager.execute()


app.add_typer(project_app)

if __name__ == "__main__":
    app()
