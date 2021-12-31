import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel

from __init__ import __version__

version = str(__version__)


class AboutDialog(QDialog):
    def __init__(self) -> None:
        super(AboutDialog, self).__init__()

        QBtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QGridLayout()

        title = QLabel("Chaser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title, 0, 1)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join("assets", "icons", "cookie.png")))
        layout.addWidget(logo, 0, 0)

        layout.addWidget(QLabel(f"Version {version}"), 1, 0, 1, 1)
        layout.addWidget(QLabel("Copyright (c) 2021 luciferchase"), 2, 0, 2, 1)

        for i in range(layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
