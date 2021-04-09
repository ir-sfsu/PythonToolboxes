import arcpy
from arcpy import management as MN
from arcpy import analysis as AN
import os

class TessellatePoints(object):
    def __init__(self):
        """Define the tool"""
        self.label = "Tessellate Points"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        inpoints = arcpy.Parameter(
            displayName = "Input points",
            name = "input_points",
            datatype = "Feature Layer",
            parameterType = "Required",
            direction = "Input"
            )
        shape = arcpy.Parameter(
            displayName = "Shape",
            name = "shape",
            datatype = "String",
            parameterType = "Required",
            direction = "Input"
            )
        shape.value = "HEXAGON"
        size = arcpy.Parameter(
            displayName = "Size",
            name = "size",
            datatype = "String",
            parameterType = "Required",
            direction = "Input"
            )
        params = [inpoints, shape, size]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        inpoints = parameters[0].valueAsText(0)
        shape = parameters[1].valueAsText(1)
        size = parameters[2].valueAsText(2)
        ext = arcpy.Describe(inpoints).extent
        in_dir = os.path.dirname(inpoints)
        tessellate_out = os.path.join(in_dir, "tessellated")
        MN.GenerateTessellation(tessellate_out, ext, shape, size)
        tessellated_points_out = os.path.join(in_dir, "points_in_tessellation")
        AN.SpatialJoin(tessellate_out, inpoints, tessellated_points_out, "JOIN_ONE_TO_ONE","KEEP_ALL", "","COMPLETELY_CONTAINS")