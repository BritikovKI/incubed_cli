import unittest

import in3
from PySide2.QtWidgets import QApplication

from ui.subscreens.contract_activities import ContractActivities
from ui.utils.contract_modal import ContractModal


class ContractTests(unittest.TestCase):
    app = QApplication()

    def test_wrong_contract_addition(self):
        main = ContractActivities(in3.Client("goerli"))
        cont = ContractModal(main)
        self.assertEqual(cont.isVisible(), False)
        cont.setVisible(True)
        cont.new_addr_line.setText("Hello darkness")
        cont.modal_add.click()
        # self.assertEqual(acc.isHidden(), True)
        self.assertEqual(cont.modal_error_label.isVisible(), True)
        self.assertEqual(cont.new_addr_line.text(), "")

    def test_correct_account_addition(self):
        main = ContractActivities(in3.Client("goerli"))
        cont = ContractModal(main)
        self.assertEqual(cont.isVisible(), False)
        cont.setVisible(True)
        cont.new_addr_line.setText("0xFB55cC4bE5496629169219FeeEFDF98d423AFf8B")
        cont.modal_add.click()
        # self.assertEqual(acc.isHidden(), True)
        self.assertEqual(cont.modal_error_label.isVisible(), False)
        self.assertEqual(cont.new_addr_line.text(), "")


if __name__ == '__main__':
    unittest.main()
