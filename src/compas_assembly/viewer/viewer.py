from typing import List

from compas.data import Data

from compas_view2.app import App
from compas_view2.objects import Object
from compas_view2.objects import MeshObject
from compas_view2.objects import NetworkObject

from compas_assembly.datastructures import Block
from compas_assembly.datastructures import Assembly

Object.register(Block, MeshObject)
Object.register(Assembly, NetworkObject)


class Viewer(App):

    def add(self, data: Data, **kwargs) -> List[Object]:
        """Add a COMPAS object.

        Parameters
        ----------
        data: :class:`compas.geometry.Primitive` | :class:`compas.geometry.Shape` | :class:`compas.geometry.Datastructure`

        Returns
        -------
        :class:`compas_view2.objects.Object`
        """
        if isinstance(data, Assembly):
            assemblyobj = Object.build(data, **kwargs)
            objs = [assemblyobj]
            for node in data.nodes():
                block = data.node_attribute(node, 'block')
                blockobj = Object.build(block, **kwargs)
                objs.append(blockobj)
            for obj in objs:
                self.view.objects[obj] = obj
                self.selector.add(obj)
                if self.view.isValid():
                    obj.init()
            return objs
        obj = Object.build(data, **kwargs)
        self.view.objects[obj] = obj
        self.selector.add(obj)
        if self.view.isValid():
            obj.init()
        return [obj]
