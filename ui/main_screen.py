import random
import re

import in3
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QLabel, QPushButton,
                               QVBoxLayout, QWidget, QGroupBox,
                               QToolButton, QDialog, QFormLayout, QLineEdit, QComboBox)
from PySide2.QtCore import Slot, Qt
from in3 import ClientException

from ui.subscreens.contract_activities import ContractActivities
from ui.subscreens.server_listing import ServerListing
from ui.utils.account_modal import AccountModal

"""
This is an overall view of the applicarion, 
it consists of the account button, part to the left(server listing)
and part to the right(work with contract). 
"""
class MainForm(QWidget):

    def __init__(self, network = "goerli"):
        QWidget.__init__(self)

        # check if the app is connected to the network
        self.client = in3.Client(network)
        try:
            check = self.client.eth.block_number()
        except ClientException:
            print("Unable to connect to the" + network)
            return


        self.p_key = ""
        self.server_listing_box = ServerListing(self.client)
        self.buttons_listing_box = ContractActivities(self.client)
        self.server_listing_box.setMinimumWidth(800)

        # Private key setup button creation(assigned to the top right corner)
        self.top = QWidget()
        self.account_layout = QVBoxLayout()
        self.settings_button = QToolButton()
        self.settings_button.setIcon(QIcon("./resources/account.png"))
        self.account_layout.addWidget(self.settings_button)
        self.account_layout.setAlignment(Qt.AlignRight)
        self.top.setLayout(self.account_layout)

        # Main layout, with all of the functionality on it
        self.main_layout = QFormLayout()
        self.main_layout.addRow(QLabel("Network: "+network), self.top)
        self.main_layout.addRow(self.server_listing_box, self.buttons_listing_box)
        self.setLayout(self.main_layout)

        # Connecting the signal
        self.settings_button.clicked.connect(self.account_click)

        # Modal window to set up user's account
        self.add_account_modal = AccountModal(self)


    """
    This method displays modal window which allows to add private key.
    """
    @Slot()
    def account_click(self):
       self.add_account_modal.show()


    def update_pkey(self, pkey):
        self.p_key = pkey
        self.buttons_listing_box.update_pkey(pkey)



# e91f3df976f5d92e4e317be29645fb501f224954aad37661e012552d32ab9f68