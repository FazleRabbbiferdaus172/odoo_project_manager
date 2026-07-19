import sys
import getopt

from src.odoo_project_manager.manager import Manager


def cli():
    args = sys.argv
    options = "hs:l:e:n:"
    long_versions = ["help", "output-lcoation=", "edition=", "project-source=", "name="]
    arg_options, arg_vals = getopt.gnu_getopt(args[1:], options, long_versions)
    import pdb

    pdb.set_trace()
    manager = Manager.get_instance(arg_options, arg_vals)
    manager.execute()
