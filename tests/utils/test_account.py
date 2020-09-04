import unittest

from PySide2.QtWidgets import QApplication

from ui.main_screen import MainForm
from ui.utils.account_modal import AccountModal


class AccountTests(unittest.TestCase):
    app = QApplication()

    def test_wrong_account_creation(self):
        main = MainForm()
        acc = AccountModal(main)
        self.assertEqual(acc.isVisible(), False)
        acc.setVisible(True)
        acc.new_addr_line.setText("Hello darkness")
        acc.modal_save.click()
        # self.assertEqual(acc.isHidden(), True)
        self.assertEqual(acc.modal_error_label.isVisible(),True)
        self.assertEqual(acc.new_addr_line.text(),"")

    def test_correct_account_creation(self):
        main = MainForm()
        acc = AccountModal(main)
        self.assertEqual(acc.isVisible(), False)
        acc.setVisible(True)
        acc.new_addr_line.setText("e91f3df976f5d92e4e317be29645fb501f224954aad37661e012552d32ab9f68")
        acc.modal_save.click()
        # self.assertEqual(acc.isHidden(), True)
        self.assertEqual(acc.modal_error_label.isVisible(), False)
        self.assertEqual(acc.new_addr_line.text(), "e91f3df976f5d92e4e317be29645fb501f224954aad37661e012552d32ab9f68")




if __name__ == '__main__':
    unittest.main()
