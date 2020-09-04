import in3
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from in3 import ClientException

"""
This is listing of nodes, that consists of all urls of incubed
"""


class ServerListing(QGroupBox):

    def __init__(self, client):
        QGroupBox.__init__(self)

        self.client = client
        # Creation of node list in network
        node_list = client.refresh_node_list()
        self.label = QLabel("Incubed nodes listing:")
        self.button = QPushButton("Update list")

        self.nodes_listing = QListWidget()
        self.items = []
        for node in node_list.nodes:
            self.items.append(QListWidgetItem(QIcon(), node.url, self.nodes_listing))

        self.server_listing_layout = QVBoxLayout()
        self.server_listing_layout.addWidget(self.label)

        self.server_listing_layout.addWidget(self.nodes_listing)

        self.server_listing_layout.addWidget(self.button)
        self.setLayout(self.server_listing_layout)
        # Button to update the list with nodes
        self.button.clicked.connect(self.update_list)

    # Function updates the list of incubed nodes
    def update_list(self):
        node_list = self.client.refresh_node_list()
        self.items = []
        self.nodes_listing = QListWidget()
        for node in node_list.nodes:
            self.items.append(QListWidgetItem(QIcon(), node.url, self.nodes_listing))
