import json
import re
import time

import in3
from PySide2.QtWidgets import QDialog, QGroupBox, QLabel, QFormLayout, QLineEdit, QPushButton

from blockchain.functions_signatures import REMOVE_NODE

"""
This is the modal window to remove node
"""
class RemoveNode(QDialog):
    def __init__(self, client):
        QDialog.__init__(self)
        self.client = client
        self.contract = ""
        self.modal_group_box = QGroupBox("Remove node")
        self.modal_error_label = QLabel("Wrong address, account must be written in form : '0x...'.")
        self.hash_label = QLabel("")
        self.modal_group_layout = QFormLayout()
        self.signer_line = QLineEdit()
        self.modal_error_label.hide()
        self.hash_label.hide()
        self.modal_group_layout.addRow(QLabel("Remove node:"))
        self.modal_group_layout.addRow(self.modal_error_label)
        self.modal_group_layout.addRow(self.hash_label)
        self.modal_group_layout.addRow(QLabel("Signer:"), self.signer_line)
        self.modal_remove = QPushButton("Remove")
        self.p_key = ""

        self.modal_cancel = QPushButton("Close")
        self.modal_cancel.clicked.connect(self.modal_cancel_func)
        self.modal_remove.clicked.connect(self.modal_remove_node)
        self.modal_group_layout.addRow(self.modal_remove, self.modal_cancel)
        self.setLayout(self.modal_group_layout)

    """
     Cancel function closes modal window
    """
    def modal_cancel_func(self):
        self.modal_error_label.hide()
        self.hide()


    """
    This function checks input data(signer address) and sends transaction to the registry instance
    """
    def modal_remove_node(self):
        if not re.match("0x[A-Fa-f0-9]{40}", self.signer_line.text()):
            self.modal_error_label.setText("Wrong input. Account must be written in form : '0x...'.")
            self.modal_error_label.show()
            return
        self.modal_error_label.hide()
        remove_node_abi = REMOVE_NODE
        sender = self.client.eth.account.recover('0x'+self.p_key)
        remove_node_tx = {
            "to": self.contract,
            "gasLimit": 200000,
            "data": self.client.eth.contract.encode(remove_node_abi,self.signer_line.text())
        }

        tx_hash = self.client.eth.account.send_transaction(sender,in3.eth.NewTransaction(**remove_node_tx))
        self.hash_label.setText("Latest transaction hash is: " + tx_hash)
        self.hash_label.show()