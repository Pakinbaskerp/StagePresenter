from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ThumbnailPanel(QWidget):
    def __init__(self, load_callback, select_callback):
        super().__init__()
        print("Initializing ThumbnailPanel...")
        self.load_callback = load_callback
        self.select_callback = select_callback

        layout = QVBoxLayout(self)

        # Load Button
        btn_load = QPushButton("Load PPTX")
        btn_load.clicked.connect(self.open_file)
        layout.addWidget(btn_load)
        print("Added Load PPTX button")

        # Scroll area for thumbnails
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.list_widget)

        layout.addWidget(self.scroll_area)
        print("Thumbnail scroll area initialized")

    def open_file(self):
        print("Opening file dialog to select PPTX...")
        file, _ = QFileDialog.getOpenFileName(self, "Open PPTX", "", "PowerPoint Files (*.pptx)")
        if file:
            print(f"Selected file: {file}")
            self.load_callback(file)

    def show_thumbnails(self, slides):
        print("Clearing old thumbnails...")
        # Clear old thumbnails
        for i in reversed(range(self.list_layout.count())):
            widget = self.list_layout.itemAt(i).widget()
            self.list_layout.removeWidget(widget)
            widget.deleteLater()
        print(f"Displaying {len(slides)} thumbnails...")

        # Add new thumbnails
        for i, path in enumerate(slides):
            print(f"Adding thumbnail for slide {i+1}: {path}")
            label = QLabel()
            pixmap = QPixmap(path).scaled(180, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 1px solid gray; margin: 5px; padding: 2px;")
            label.mousePressEvent = lambda event, idx=i: self.select_callback(idx)
            self.list_layout.addWidget(label)
