from typing import Tuple
from pathlib import Path

from viktor import File
from viktor import ViktorController

from viktor.parametrization import ViktorParametrization
from viktor.parametrization import NumberField
from viktor.parametrization import Text

from viktor.external.dynamo import DynamoFile
from viktor.external.dynamo import convert_geometry_to_glb

from viktor.views import GeometryResult
from viktor.views import GeometryView

class Parametrization(ViktorParametrization):
    intro = Text("# 3D  Dynamo app \n This app parametrically generates and visualises a 3D model of a house using a Dynamo script. \n\n Please fill in the following parameters:")
    
    # Input fields
    number_of_houses = NumberField("Number of houses", max=8.0, min=1.0, variant='slider', step=1.0, default=3.0)
    number_of_floors = NumberField("Number of floors", max=5.0, min=1.0, variant='slider', step=1.0, default=2.0)
    depth = NumberField("Depth", max=10.0, min=5.0, variant='slider', step=1.0, default=8.0, suffix="m")
    width = NumberField("Width", max=6.0, min=4.0, variant='slider', step=1.0, default=5.0, suffix="m")
    height_floor = NumberField("Height floor", max=3.0, min=2.0, variant='slider', step=0.1, default=2.5, suffix='m')
    height_roof = NumberField("Height roof", max=3.0, min=2.0, variant='slider', step=0.1, default=2.5, suffix='m')


class Controller(ViktorController):
    label = 'My Entity Type'
    parametrization = Parametrization

    @staticmethod
    def update_model(params) -> Tuple[File, DynamoFile]:
        """This method updates the nodes of the Dynamo file with the parameters
        from the parametrization class."""

        # First the path to the Dynamo file is specified and loaded
        file_path = Path(__file__).parent / "dynamo_model_sample_app.dyn"
        _file = File.from_path(file_path)
        dyn_file = DynamoFile(_file)

        # Update Dynamo file with parameters from user input
        dyn_file.update("Number of houses", params.number_of_houses)
        dyn_file.update("Number of floors", params.number_of_floors)
        dyn_file.update("Depth", params.depth)
        dyn_file.update("Width", params.width)
        dyn_file.update("Height floor", params.height_floor)
        dyn_file.update("Height roof", params.height_roof)

        # generate updated file
        input_file = dyn_file.generate()

        return input_file, dyn_file

    @GeometryView("Mocked 3d model", duration_guess=1)
    def mocked_geometry_view(self, params, **kwargs):
        # Step 1: Update model
        input_file, dynamo_file = self.update_model(params)

        # Step 2: Running analysis
        file_path = Path(__file__).parent / "Mocked_3d_model.json"
        _3d_file = File.from_path(file_path)

        # Step 3: Processing geometry
        glb_file = convert_geometry_to_glb(_3d_file)

        return GeometryResult(geometry=glb_file)
