import re

import in3
from PySide2.QtWidgets import QDialog, QGroupBox, QLabel, QFormLayout, QLineEdit, QPushButton

from blockchain.functions_signatures import CONVICT

"""
This is the modal window to convict other node
"""
class Convict(QDialog):

    def __init__(self, client):
        # Creating modal window to form request for contract
        QDialog.__init__(self)
        self.client = client
        self.modal_group_box = QGroupBox("Node")
        self.modal_error_label = QLabel("Wrong address, account must be written in form : '0x...'.")
        self.modal_group_layout = QFormLayout()
        self.hash_line = QLineEdit()
        self.modal_error_label.hide()

        self.hash_label = QLabel("")
        self.hash_label.hide()

        self.modal_group_layout.addRow(QLabel("Convict node:"))
        self.modal_group_layout.addRow(self.modal_error_label)
        self.modal_group_layout.addRow(self.hash_label)
        self.modal_group_layout.addRow(QLabel("Hash:"), self.hash_line)
        self.modal_convict_btn = QPushButton("Convict")
        self.p_key = ""
        self.contract = ""

        self.modal_cancel = QPushButton("Close")
        self.modal_cancel.clicked.connect(self.modal_cancel_func)
        self.modal_convict_btn.clicked.connect(self.modal_convict)
        self.modal_group_layout.addRow(self.modal_convict_btn, self.modal_cancel)
        self.setLayout(self.modal_group_layout)

    """
     Cancel function closes modal window
    """
    def modal_cancel_func(self):
        self.modal_error_label.hide()
        self.hide()

    """
    This function checks input data(hash provded) and sends transaction to the registry instance
    """
    def modal_convict(self):
        if not re.match("0x[0-9A-Fa-f]{64}", self.hash_line.text()):
            self.modal_error_label.setText("Wrong input. Hash should be written in the hexadecimal form(64 symbols of hash) in format: 0x...")
            self.modal_error_label.show()
            return

        self.modal_error_label.hide()
        convict_node_abi = CONVICT
        sender = self.client.eth.account.recover('0x'+self.p_key)
        convict_node_tx = {
            "to": self.contract,
            "gasLimit": 200000,
            "data": self.client.eth.contract.encode(convict_node_abi, self.hash_line.text())
        }

        tx_hash = self.client.eth.account.send_transaction(sender, in3.eth.NewTransaction(**convict_node_tx))
        self.hash_label.setText("Latest transaction hash is: " + tx_hash)
        self.hash_label.show()

# a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
# bfbfbb1ed01fe85d529582b556e398a735c6a4110e7f9cce414d0d92ca7ca5c3