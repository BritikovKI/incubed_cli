import json
import re
import time

import in3
from PySide2.QtWidgets import QDialog, QGroupBox, QLabel, QFormLayout, QLineEdit, QPushButton
from in3 import ClientException

from blockchain.functions_signatures import REGISTER_NODE
# TODO: Inheritance
"""
This is the modal window to register new node
"""
class RegisterNode(QDialog):
    def __init__(self, client):
        # Creating modal window to form request for contract
        QDialog.__init__(self)
        self.client = client
        self.contract = ""
        self.modal_group_box = QGroupBox("Node")
        self.modal_error_label = QLabel("Wrong address, account must be written in form : '0x...'.")
        self.hash_label = QLabel("")
        self.modal_group_layout = QFormLayout()
        self.url_line = QLineEdit()
        self.properties_line = QLineEdit()
        self.weight_line = QLineEdit()
        self.deposit_line = QLineEdit()
        self.modal_error_label.hide()
        self.hash_label.hide()
        self.modal_group_layout.addRow(QLabel("Add node:"))
        self.modal_group_layout.addRow(self.modal_error_label)
        self.modal_group_layout.addRow(self.hash_label)
        self.modal_group_layout.addRow(QLabel("Url:"), self.url_line)
        self.modal_group_layout.addRow(QLabel("Properties:"), self.properties_line)
        self.modal_group_layout.addRow(QLabel("Weight:"), self.weight_line)
        self.modal_group_layout.addRow(QLabel("Deposit:"), self.deposit_line)
        self.modal_add = QPushButton("Add")
        self.p_key = ""
        # self.settings.clicked.connect(self.modal_add_func)

        self.modal_cancel = QPushButton("Close")
        self.modal_cancel.clicked.connect(self.modal_cancel_func)
        self.modal_add.clicked.connect(self.modal_add_node)
        self.modal_group_layout.addRow(self.modal_add, self.modal_cancel)
        self.setLayout(self.modal_group_layout)

    """
     Cancel function closes modal window
    """
    def modal_cancel_func(self):
        self.modal_error_label.hide()
        self.hide()


    """
    This function checks input data(url, properties, weight and deposit) and sends transaction to the registry instance
    """
    def modal_add_node(self):
        if not re.match(".*\\.[A-Za-z]*", self.url_line.text()) and \
            re.match("[0-9]*", self.properties_line.text()) and \
            re.match("[0-9]*", self.weight_line.text()) and \
            re.match("[0-9]*", self.deposit_line.text()):
            self.modal_error_label.setText("Wrong input. Url should be written like 'derpaz.eth', everything else is integer.")
            self.modal_error_label.show()
            return
        self.modal_error_label.hide()
        add_node_abi = REGISTER_NODE
        sender = self.client.eth.account.recover('0x'+self.p_key)
        add_node_tx = {
            "to": self.contract,
            "gasLimit": 400000,
            "data": self.client.eth.contract.encode(add_node_abi,self.url_line.text(), int(self.properties_line.text(),10), int(self.weight_line.text(),10), int(self.deposit_line.text(),10))
        }

        # bfbfbb1ed01fe85d529582b556e398a735c6a4110e7f9cce414d0d92ca7ca5c3
        # self.client.eth.account.call()
        try:
            tx_hash = self.client.eth.account.send_transaction(sender,in3.eth.NewTransaction(**add_node_tx))
            self.hash_label.setText("Latest transaction hash is: " + tx_hash)
            self.hash_label.show()
        except ClientException as ex:
            self.modal_error_label.setText(
                ex.__str__())
            self.modal_error_label.show()
