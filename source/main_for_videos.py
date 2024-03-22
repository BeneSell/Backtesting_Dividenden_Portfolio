from visualization.second_scene import DataFrameTransformation
import data_preprocessing.preproccess_classes as pre



# not really a good way to use this class, but i dont know how to use it in a better way
# the problem is that the python package manim wants a class and i dont want to write the class in the overview file
# so i have inherited from the manim class Scene
# also if you want to start the scene from there source folder the imports arent working
# with this solution good imports and the class is in the right place
class DataFrameTransformation_Copy(DataFrameTransformation):
    pass