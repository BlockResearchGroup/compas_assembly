# import argparse
import importlib

from compas_rhino.install import install as rhino_install


PACKAGES = ['compas', 'compas_rhino', 'compas_assembly']


def install():

    print("\n", "-"*10, "Checking packages", "-"*10)

    for p in PACKAGES:
        try:
            importlib.import_module(p)
        except ImportError:
            print(p, "ERROR: cannot be imported, make sure it is installed")
            raise
        else:
            print('   {} {}'.format(p.ljust(20), "OK"))

    rhino_install(packages=PACKAGES)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    # parser = argparse.ArgumentParser(description='Assembly Installation command-line utility.')
    # parser.add_argument('--remove_plugins', action='store_true', help="remove all existing plugins")
    # args = parser.parse_args()

    install()
