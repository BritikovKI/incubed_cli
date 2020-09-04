from PySide2.QtWidgets import QWidget, QComboBox, QPushButton, QFormLayout, QLabel

from ui.main_screen import MainForm

"""
This is a window to pick the network for the application,
it is being shown before an actual app
"""
class NetPick(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.network_pick_combobox = QComboBox()
        self.network = "goerli"
        self.network_pick_combobox.addItem("goerli")
        self.network_pick_combobox.addItem("mainnet")
        self.network_pick_combobox.addItem("kovan")
        self.ok_button = QPushButton("Ok")

        self.main_layout = QFormLayout()
        self.main_layout.addRow(QLabel("Network:"), self.network_pick_combobox)
        self.main_layout.addRow(self.ok_button)

        self.ok_button.clicked.connect(self.pick_network)
        self.setLayout(self.main_layout)


    """
    This is local method, which changes network depending on the pick
    in the ComboBox
    """
    def pick_network(self):
            self.network = self.network_pick_combobox.currentText()
            self.close()
