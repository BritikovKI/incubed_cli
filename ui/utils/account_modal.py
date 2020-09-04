import re

from PySide2.QtWidgets import QDialog, QLabel, QGroupBox, QFormLayout, QLineEdit, QPushButton


class AccountModal(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self)
        self.account_group_box = QGroupBox("Account")
        self.modal_error_label = QLabel("Wrong address, account must be written in form : '0x...'.")
        self.account_group_layout = QFormLayout()
        self.new_addr_line = QLineEdit()
        self.modal_error_label.hide()
        self.account_group_layout.addRow(self.modal_error_label)
        self.parent = parent
        self.account_group_layout.addRow(QLabel("Write your private key:"), self.new_addr_line)
        self.modal_save = QPushButton("Save")
        self.modal_save.clicked.connect(self.modal_save_func)

        self.modal_cancel = QPushButton("Cancel")
        # self.modal_cancel.clicked.connect(self.modal_cancel_func)
        self.account_group_layout.addRow(self.modal_save, self.modal_cancel)

        self.modal_cancel.clicked.connect(self.modal_cancel_func)
        self.setLayout(self.account_group_layout)


    """
    It is function to save private key for the current session
    (private key isn't stored, as it would take a lot of time to provide
    necessary security for such a task.
    """
    def modal_save_func(self):
        new_addr = self.new_addr_line.displayText()
        if re.fullmatch("[0-9a-f]{64}", new_addr):
            self.modal_error_label.hide()
            self.hide()
            self.p_key = new_addr
            self.parent.update_pkey(self.p_key)
        else:
            self.new_addr_line.setText("")
            self.modal_error_label.setText("Wrong address, account must be written in form : 'e91f...'(total length is 64 characters in hexadecimal form).")
            self.modal_error_label.show()

    """
    This method is for the modal window, to return to the main screen from adding private key
    """
    def modal_cancel_func(self):
        self.modal_error_label.hide()
        self.hide()

