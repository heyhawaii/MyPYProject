# coding: utf-8
from DYProcessManager import ComponentStatus
from component_controler import *

class ComponentsLoad():
    def __init__(self):
        self.Process = ComponentStatus()

    def get_local_components_name(self):
        self.local_components_name = []
        for component_name in self.Process.components:
            self.local_components_name.append(component_name)
        for msgserver_num in self.Process.msgserver:
            msgserver_name = 'MsgServer' + str(msgserver_num)
            self.local_components_name.append(msgserver_name)
        return self.local_components_name

    def getload(self,types):
        for component_nanme in self.local_components_name:
            component = Action(component_nanme)
            component_status = component.isalived()
            if component_status:
                if types == 'cpu':
                    print component_nanme,component_status.cpu_percent(interval=1)
                elif types == 'mem':
                    print component_nanme,component_status.memory_info()
                elif types == 'io':
                    print component_nanme,component_status.io_counters()
                elif types == 'conns':
                    print component_nanme,component_status.connections()



if __name__ == '__main__':
    loads = ComponentsLoad()
    loads.get_local_components_name()
    if len(sys.argv) == 2:
        types = sys.argv[1]
        type_range = ['cpu', 'mem', 'io', 'conns']
        for each_type in  type_range:
            if types == each_type:
                loads.getload(types)
        if types not in type_range:
            print 'Illegal Segment! Now Exit...'
            sys.exit(1)
    else:
        loads.getload('cpu')