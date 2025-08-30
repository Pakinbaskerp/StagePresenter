from PyQt5.QtWidgets import QSplitter, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class PreviewPanel(QSplitter):
    def __init__(self):
        super().__init__(Qt.Vertical)
        print("Initializing PreviewPanel...")

        # Small preview
        self.preview = QLabel("Preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setStyleSheet("background-color: #ddd; border: 1px solid #aaa;")
        self.addWidget(self.preview)
        print("Added small preview area")

        # Large output
        self.output = QLabel("Full Output Area")
        self.output.setAlignment(Qt.AlignCenter)
        self.output.setStyleSheet("background-color: black; color: white; font-size: 24px;")
        self.addWidget(self.output)
        print("Added full output area")

        self.setSizes([300, 600])
        print("PreviewPanel initialized successfully")

    def show_slide(self, path):
        print(f"Displaying slide: {path}")
        pixmap_preview = QPixmap(path).scaled(400, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview.setPixmap(pixmap_preview)
        print("Small preview updated")

        pixmap_output = QPixmap(path).scaled(900, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.output.setPixmap(pixmap_output)
        print("Full output updated")
