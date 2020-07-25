from gui import Gui
from cube import Cube


if __name__ == "__main__":
    cube = Cube(3)
    gui = Gui(cube)
    gui.run()