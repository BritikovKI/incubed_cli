import sys

from PySide2.QtWidgets import QApplication
from ui.main_screen import MainForm
from ui.network_pick import NetPick

'''
    Main part of application, at first it runs a window to get the info
    about network, on which user wants to work, then it runs the main app
    (I've wanted to change network "as we go", but I've encountered bug, where
    I cannot create another connection if I have already connected to some network
    (at least in python).
'''
if __name__ == "__main__":
    # initial request to understand which network to use
    app = QApplication(sys.argv)
    network_pick = NetPick()
    network_pick.show()
    app.exec_()
    # start main application
    network = network_pick.network
    widget = MainForm(network)
    widget.resize(1000, 800)

    widget.show()

    sys.exit(app.exec_())
