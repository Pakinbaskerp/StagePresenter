import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton
from PyQt5.QtCore import Qt, QFileSystemWatcher


class TemplatePanel(QWidget):
    def __init__(self, template_dir, on_template_selected=None):
        super().__init__()
        self.template_dir = template_dir
        self.on_template_selected = on_template_selected  # callback when user clicks
        self.current_dir = template_dir  # current navigation folder

        layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.list_widget)
        layout.addWidget(QLabel("📑 PPT Templates"))
        layout.addWidget(self.scroll_area)

        # File system watcher → refresh on changes
        self.watcher = QFileSystemWatcher()
        self.watcher.addPath(self.current_dir)
        self.watcher.directoryChanged.connect(self.load_templates)

        self.load_templates()

    def load_templates(self):
        """Load folders and only ppt/pptx files in current directory."""
        if not os.path.exists(self.current_dir):
            return

        # Clear old items
        while self.list_layout.count():
            child = self.list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # --- Add 'Back' button if not at root ---
        if os.path.abspath(self.current_dir) != os.path.abspath(self.template_dir):
            back_btn = QPushButton("⬅️ Back")
            back_btn.clicked.connect(self.go_back)
            self.list_layout.addWidget(back_btn)

        # --- Show folders first ---
        for item in sorted(os.listdir(self.current_dir)):
            path = os.path.join(self.current_dir, item)
            if os.path.isdir(path) and item.lower() != "slides":  # 👈 hide "Slides" folder
                btn = QPushButton(f"📂 {item}")
                btn.setStyleSheet("text-align: left; padding: 6px; border: 1px solid #666;")
                btn.clicked.connect(lambda checked, p=path: self.open_folder(p))
                self.list_layout.addWidget(btn)

        # --- Show only ppt/pptx files ---
        for item in sorted(os.listdir(self.current_dir)):
            if item.lower().endswith((".pptx", ".ppt")):
                path = os.path.join(self.current_dir, item)
                if os.path.isfile(path):
                    btn = QPushButton(f"📑 {item}")
                    btn.setStyleSheet("text-align: left; padding: 6px; border: 1px solid #888;")
                    btn.clicked.connect(lambda checked, p=path: self.open_template(p))
                    self.list_layout.addWidget(btn)

    def open_template(self, file_path):
        print("Selected template:", file_path)
        if self.on_template_selected:
            self.on_template_selected(file_path)

    def open_folder(self, folder_path):
        """Navigate into folder and reload contents."""
        self.current_dir = folder_path
        self.watcher.removePaths(self.watcher.directories())
        self.watcher.addPath(self.current_dir)
        self.load_templates()

    def go_back(self):
        """Go up one directory level (but not above root)."""
        parent = os.path.dirname(self.current_dir)
        if os.path.commonpath([parent, self.template_dir]) == os.path.abspath(self.template_dir):
            self.current_dir = parent
            self.watcher.removePaths(self.watcher.directories())
            self.watcher.addPath(self.current_dir)
            self.load_templates()
