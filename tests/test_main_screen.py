import sys
import unittest

from PySide2.QtWidgets import QApplication

from ui.main_screen import MainForm


class MainScreenTests(unittest.TestCase):

    app = QApplication(sys.argv)

    def test_add_account_click(self):
        main_form = MainForm()
        self.assertEqual(main_form.add_account_modal.isHidden(), True)
        main_form.settings.click()
        self.assertEqual(main_form.add_account_modal.isHidden(), False)


if __name__ == '__main__':
    unittest.main()
