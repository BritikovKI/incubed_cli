import sys
import unittest

import in3
from PySide2.QtWidgets import QApplication


from ui.subscreens.contract_activities import ContractActivities


class ContractActivitiesTest(unittest.TestCase):

    app = QApplication(sys.argv)

    def test_send_transact_without_key(self):
        main = ContractActivities(in3.Client("goerli"))
        main.setVisible(True)
        self.assertEqual(main.convict_modal.isVisible(), False)
        self.assertEqual(main.no_key_error_label.isHidden(), True)
        main.people_buttons[1].click()
        self.assertEqual(main.convict_modal.isHidden(), True)
        self.assertEqual(main.no_key_error_label.isHidden(), False)

    def test_send_admin_transact_with_nonadmin_key(self):
        main = ContractActivities(in3.Client("goerli"))
        main.setVisible(True)
        main.p_key = "bae4f8f1b2778d75625157b108d4de1a469ad330f88c6d699703d2b309dd7744"
        self.assertEqual(main.remove_node_modal.isVisible(), False)
        self.assertEqual(main.no_key_error_label.isHidden(), True)
        main.admin_buttons[0].click()
        self.assertEqual(main.remove_node_modal.isHidden(), True)
        self.assertEqual(main.no_key_error_label.isHidden(), False)


if __name__ == '__main__':
    unittest.main()
