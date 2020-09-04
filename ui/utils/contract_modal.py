import re

from PySide2.QtWidgets import QDialog, QLabel, QGroupBox, QFormLayout, QLineEdit, QPushButton


class ContractModal(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self)

        # This is modal window to add new contract to work with
        self.modal_group_box = QGroupBox("Contract")
        self.modal_error_label = QLabel("Wrong address, account must be written in form : '0x...'.")
        self.modal_group_layout = QFormLayout()
        self.new_addr_line = QLineEdit()
        self.modal_error_label.hide()
        self.modal_group_layout.addRow(self.modal_error_label)

        self.modal_group_layout.addRow(QLabel("Write address of new contract:"), self.new_addr_line)
        self.modal_add = QPushButton("Add")

        self.modal_add.clicked.connect(self.modal_add_func)
        self.modal_cancel = QPushButton("Cancel")
        self.modal_cancel.clicked.connect(self.modal_cancel_func)
        self.modal_group_layout.addRow(self.modal_add, self.modal_cancel)
        self.parent = parent
        self.setLayout(self.modal_group_layout)


    """
     This method adds address from textbox(in the modal window) to the list, and checks if it satisfies needed format
    """
    def modal_add_func(self):
        new_addr = self.new_addr_line.displayText()
        if re.fullmatch("0x[0-9A-Fa-f]{40}", new_addr):
            self.modal_error_label.hide()
            self.new_addr_line.setText("")
            self.hide()
            self.parent.add_cont_address(new_addr)
        else:
            self.new_addr_line.setText("")
            self.modal_error_label.setText("Wrong address, account must be written in form : '0x...'.")
            self.modal_error_label.show()

    """
    This method is for the modal window, to return to the main screen from adding new Registry smart contract
    """
    def modal_cancel_func(self):
        self.modal_error_label.hide()
        self.hide()


