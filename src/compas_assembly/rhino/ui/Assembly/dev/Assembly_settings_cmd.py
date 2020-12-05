from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import traceback
import scriptcontext as sc
import Rhino

from compas_rhino.etoforms import SettingsForm


__commandname__ = "Assembly_settings"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        assembly = sc.sticky['compas_assembly']['assembly']
        settings = sc.sticky['compas_assembly']['settings']

        dialog = SettingsForm(settings)

        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            settings.update(dialog.settings)

            if assembly:
                assembly.draw(settings)

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
