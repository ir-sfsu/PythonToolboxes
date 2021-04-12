import arcpy
from arcpy import management as MN
from arcpy import analysis as AN
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox"""
        self.label = "Tessellate Points"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [TessellatePoints]

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
            datatype = "Areal Unit",
            parameterType = "Required",
            direction = "Input"
            )
        spatial_ref = arcpy.Parameter(
            displayName = "Spatial Reference",
            name = "spatial_ref",
            datatype = "Spatial Reference",
            parameterType = "Optional",
            direction = "Input"
            )

        params = [inpoints, shape, size, spatial_ref]
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
        arcpy.AddMessage("Starting tool...")
        inpoints = parameters[0].valueAsText
        shape = parameters[1].valueAsText
        size = parameters[2].valueAsText
        spatial_ref = parameters[3].valueAsText
        inpointsDesc = arcpy.Describe(inpoints)
        ext = inpointsDesc.extent
        if spatial_ref is None:
            spatial_ref = inpointsDesc.spatialReference
        in_dir = os.path.dirname(inpoints)
        base_name = os.path.basename(inpoints)
        tessellate_out = os.path.join(in_dir, "tessellated")
        arcpy.AddMessage("Generating {} tessellation of {}...".format(shape, size))
        MN.GenerateTessellation(tessellate_out, ext, shape, size, spatial_ref)
        out_base_name = base_name + "_tessellated"
        tessellated_points_out = os.path.join(in_dir, out_base_name)
        arcpy.AddMessage("Joining {} to tessellation...".format(base_name))
        AN.SpatialJoin(tessellate_out, inpoints, tessellated_points_out, "JOIN_ONE_TO_ONE","KEEP_ALL", "","COMPLETELY_CONTAINS")
        arcpy.AddMessage("Cleaning up...")
        MN.Delete(tessellate_out)
        arcpy.AddMessage("Done!")
