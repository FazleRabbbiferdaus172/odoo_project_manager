import sys
import getopt
import pdb

from src.odoo_project_manager.manager import Manager


def cli():
    args = sys.argv
    options = "hs:l:e:n:"
    long_versions = ["help", "output-lcoation", "edition", "project-source", "name"]
    arg_options, arg_vals = getopt.getopt(args[1:], options, long_versions)
    print(arg_options, arg_vals)
    manager = Manager.get_instance(arg_options)
    manager.execute()
    pdb.set_trace()
