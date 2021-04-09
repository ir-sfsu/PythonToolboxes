from TessellatePoints import *

class Toolbox(object):
    def __init__(self):
        """Define the toolbox"""
        self.label = "Tessellate Points"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [TessellatePoints]
