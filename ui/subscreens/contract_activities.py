
import re
from datetime import datetime
from functools import wraps

from PySide2.QtGui import QIcon, Qt
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QPushButton, QFormLayout, \
    QComboBox, QToolButton, QDialog, QLineEdit
from in3 import ClientException

from ui.contract_functions.convict_modal import Convict
from ui.contract_functions.register_node_modal import RegisterNode
from ui.contract_functions.remove_node_modal import RemoveNode

# TODO: finish all other functions of the smart contract
from ui.utils.contract_modal import ContractModal

"""
This module is placed on the screen to the right, it consists of work with contract,
Here it is possible to add new registry contract, displayed info about it,and work with it by transactions
"""
class ContractActivities(QGroupBox):

    def __init__(self, client):
        QGroupBox.__init__(self)
        # This parameters are displaying information about picked contract
        self.block_registry = ""
        self.node_registry = ""
        self.timeout = ""
        self.admin_key = ""
        self.max_deposit = 0
        self.min_deposit = 0

        self.p_key = ""
        self.client = client


        # Those are modals to work with contract functions
        self.register_node_modal = RegisterNode(self.client)
        self.convict_modal = Convict(self.client)
        self.remove_node_modal = RemoveNode(self.client)

        self.main = QGroupBox()






        # This layout is done to add new contracts(it is ComboBox)
        self.top_horisontal_layout = QVBoxLayout()

        self.contract_group_box = QGroupBox("Contract")
        self.contract_group_layout = QFormLayout()
        self.contract_group_layout.addRow(QLabel("Select contract or add new one:"))
        self.butt = QToolButton()
        self.butt.setIcon(QIcon("./resources/plus.jpeg"))
        self.butt.clicked.connect(self.add_new_address)
        self.contracts_pick = QComboBox()

        self.no_key_error_label = QLabel("Enter your private key first(button top right corner).")


        self.add_cont_address("0x6C095A05764A23156eFD9D603eaDa144a9B1AF33")
        self.add_cont_address("0xfAFB978544b6D0610641cd936a005009fecc2f25")
        self.no_key_error_label.hide()

        self.contracts_pick.currentTextChanged.connect(self.change_contract_addr)
        self.contract_group_layout.addRow(self.butt, self.contracts_pick)
        self.contract_group_box.setLayout(self.contract_group_layout)


        # This part of layout are buttons for Admin functionality
        self.admin_button_group_box = QGroupBox("Admin functionality")
        self.admin_buttons_listing_layout = QVBoxLayout()
        self.admin_buttons = []
        self.admin_buttons.append(QPushButton("Remove node"))
        self.admin_buttons.append(QPushButton("Update logic"))
        for i in range(len(self.admin_buttons)):
            self.admin_buttons_listing_layout.addWidget(self.admin_buttons[i - 1])

        self.admin_button_group_box.setLayout(self.admin_buttons_listing_layout)

        # This part of layout are buttons for common functionality
        self.people_button_group_box = QGroupBox("Common functionality")
        self.people_buttons_listing_layout = QVBoxLayout()
        self.people_buttons = []
        self.people_buttons.append(QPushButton("Convict"))
        self.people_buttons.append(QPushButton("Register node"))
        self.people_buttons.append(QPushButton("Return deposit"))
        self.people_buttons.append(QPushButton("Reveal convict_modal"))
        self.people_buttons.append(QPushButton("Transfer ownership"))
        self.people_buttons.append(QPushButton("Unregister node"))
        self.people_buttons.append(QPushButton("Update node"))
        for i in range(len(self.people_buttons)):
            self.people_buttons_listing_layout.addWidget(self.people_buttons[i - 1])

        # This part of layout is a gtoup box which stores and shows all information about registry smart contract
        self.people_button_group_box.setLayout(self.people_buttons_listing_layout)

        self.admin_key_label = QLabel(self.admin_key)
        self.block_registry_label = QLabel(self.block_registry)
        self.node_registry_label = QLabel(self.node_registry)
        self.timeout_label = QLabel(str(self.timeout))
        self.max_deposit_label = QLabel(str(self.max_deposit) + " tokens")
        self.min_deposit_label = QLabel(str(self.min_deposit) + " tokens")

        self.contract_info_box = QGroupBox()
        self.contract_info_layout = QFormLayout()
        self.contract_info_layout.addRow(QLabel("Owner:"), self.admin_key_label)
        self.contract_info_layout.addRow(QLabel("Block Registry:"), self.block_registry_label)
        self.contract_info_layout.addRow(QLabel("Node Registry:"), self.node_registry_label)
        self.contract_info_layout.addRow(QLabel("Timeout:"), self.timeout_label)
        self.contract_info_layout.addRow(QLabel("Max deposit:"), self.max_deposit_label)
        self.contract_info_layout.addRow(QLabel("Min deposit:"), self.min_deposit_label)
        self.contract_info_box.setLayout(self.contract_info_layout)

        # Establishing overall view of the layout
        self.top_horisontal_layout.addWidget(self.contract_group_box)
        self.top_horisontal_layout.addWidget(self.contract_info_box)
        self.top_horisontal_layout.addWidget(self.no_key_error_label)
        self.top_horisontal_layout.addWidget(self.admin_button_group_box)
        self.top_horisontal_layout.addWidget(self.people_button_group_box)
        self.setLayout(self.top_horisontal_layout)

        for i in range(2, len(self.people_buttons)):
            self.people_buttons[i].setEnabled(False)

        for i in range(1, len(self.admin_buttons)):
            self.admin_buttons[i].setEnabled(False)

        self.add_address = ContractModal(self)

        # connecting buttons with functionality
        self.people_buttons[1].clicked.connect(self.register_new_node)
        self.people_buttons[0].clicked.connect(self.convict_node)
        self.admin_buttons[0].clicked.connect(self.remove_node)

    """
    This decorator assures that private key that is written in the app is a private key of an admin(for contract methods that require admin account),
    in other case it shows warning on the screen
    """
    def _admin_only(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            # storing time before function execution
            sender = self.client.eth.account.recover('0x' + self.p_key)
            if sender.address.lower() != '0x'+self.admin_key.lower():
                self.no_key_error_label.setText("Only admin address is allowed to execute this function")
                self.no_key_error_label.show()
            else:
                func(self, *args, **kwargs)

        return inner


    """
    This decorator assures that private key is already written in the app and contract is chosen,
    in other case it shows warning on the screen
    """
    def _with_key_and_contract_only(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            # storing time before function execution
            if self.p_key == "" or self.contracts_pick.currentText() == "":
                self.no_key_error_label.setText("Enter your private key(button in the top right corner) and pick up "
                                                "the contract first.")
                self.no_key_error_label.show()
            else:
                func(self, *args, **kwargs)

        return inner

    """
    This method opens modal window responsible for removing node
    """
    @_with_key_and_contract_only
    @_admin_only
    def remove_node(self):
        self.no_key_error_label.hide()
        self.remove_node_modal.show()

    """
    This method opens modal window responsible for convicting node
    """
    @_with_key_and_contract_only
    def convict_node(self):
        self.no_key_error_label.hide()
        self.convict_modal.show()

    """
    This method opens modal window responsible for registering new node
    """
    @_with_key_and_contract_only
    def register_new_node(self):
        self.no_key_error_label.hide()
        self.register_node_modal.show()

    """
    This method opens modal window to add new contract address
    """
    def add_new_address(self):
        self.add_address.show()


    """
    This method adds new registry address into the ComboBox, it checks if new contract is registry contract before addition
    (by the fields of the registry, it actually could and should be done by comparing bytecodes, but I don't have time to do evetything I want)
    str new_addr - is an address of added smart contract in format "0x..."(40 symbols)
    """
    def add_cont_address(self, new_addr):
        try:
            # TODO: rewrite check using bytecode of Smart Contract
            self.block_registry = self.client.eth.contract.storage_at(str(new_addr), 0)[26:]
            self.node_registry = self.client.eth.contract.storage_at(str(new_addr), 1)[26:]
            self.timeout = int.from_bytes(
                bytes.fromhex(self.client.eth.contract.storage_at(str(new_addr), 2)[2:]),
                "big")
            self.admin_key = self.client.eth.contract.storage_at(str(new_addr), 3)[26:]
            # print(self.client.eth.contract.storage_at(str(new_addr), 6))
            self.max_deposit = int(self.client.eth.contract.storage_at(str(new_addr), 6), 16)

            self.min_deposit = int(self.client.eth.contract.storage_at(str(new_addr), 7)[2:], 16)
            self.contracts_pick.addItem(new_addr)
            self.register_node_modal.contract = self.contracts_pick.currentText()
            self.remove_node_modal.contract = self.contracts_pick.currentText()
            self.convict_modal.contract = self.contracts_pick.currentText()
        except (ClientException, ValueError):
            self.no_key_error_label.setText("Wrong address, this account isn't registry account")
            self.no_key_error_label.show()


    """
    This method is needed to update information(in the labels) when another contract is picked in the ComboBox
    and to update information about the contract in the different modal windows
    """
    def change_contract_addr(self):
        self.register_node_modal.contract = self.contracts_pick.currentText()
        self.remove_node_modal.contract = self.contracts_pick.currentText()
        self.convict_modal.contract = self.contracts_pick.currentText()
        self.block_registry = self.client.eth.contract.storage_at(str(self.contracts_pick.currentText()), 0)[26:]
        self.node_registry = self.client.eth.contract.storage_at(str(self.contracts_pick.currentText()), 1)[26:]
        self.timeout = int(self.client.eth.contract.storage_at(str(self.contracts_pick.currentText()), 2)[2:], 16)
        self.admin_key = self.client.eth.contract.storage_at(str(self.contracts_pick.currentText()), 3)[26:]
        self.max_deposit = int(self.client.eth.contract.storage_at(str(self.contracts_pick.currentText()), 6)[2:], 16)
        self.min_deposit = int(self.client.eth.contract.storage_at(str(self.contracts_pick.currentText()), 7)[2:], 16)

        self.admin_key_label.setText(self.admin_key)
        self.block_registry_label.setText(self.block_registry)
        self.node_registry_label.setText(self.node_registry)
        self.max_deposit_label.setText(str(self.max_deposit) + " tokens")
        self.min_deposit_label.setText(str(self.min_deposit) + " tokens")
        self.timeout_label.setText(datetime.fromtimestamp(self.timeout).__str__())

    """
    This is function to update private keys for all modal windows
    that call smart contract(actually I could've created new modal window 
    each time I clicked button, but in my opinion this approach should work faster
    (no memory reallocation for the whole object).
    str pkey - private key in format of "0x....."(64 symbols)
    """
    def update_pkey(self, pkey):
        self.p_key = pkey
        self.register_node_modal.p_key = pkey
        self.remove_node_modal.p_key = pkey
        self.convict_modal.p_key = pkey
