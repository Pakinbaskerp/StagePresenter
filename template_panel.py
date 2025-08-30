import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt, QFileSystemWatcher


class TemplatePanel(QWidget):
    def __init__(self, template_dir, on_template_selected=None):
        super().__init__()
        self.template_dir = template_dir
        self.on_template_selected = on_template_selected
        self.current_dir = template_dir
        self.search_text = ""

        layout = QVBoxLayout(self)

        # --- Search box ---
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search templates...")
        self.search_input.textChanged.connect(self.on_search_text_changed)
        layout.addWidget(self.search_input)

        # Scroll area for templates
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

    def on_search_text_changed(self, text):
        """Update search text and reload templates."""
        self.search_text = text.lower()
        self.load_templates()

    def load_templates(self):
        """Load folders and ppt/pptx files, filtered recursively if search is active."""
        if not os.path.exists(self.current_dir):
            return

        # Clear old items
        while self.list_layout.count():
            child = self.list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add 'Back' button if not at root
        if os.path.abspath(self.current_dir) != os.path.abspath(self.template_dir):
            back_btn = QPushButton("⬅️ Back")
            back_btn.clicked.connect(self.go_back)
            self.list_layout.addWidget(back_btn)

        # If search is empty → show normal folder structure
        if not self.search_text:
            self.add_folder_and_files(self.current_dir)
        else:
            # Perform recursive search
            for root, dirs, files in os.walk(self.current_dir):
                # Show matching folders
                for d in dirs:
                    if self.search_text in d.lower():
                        folder_path = os.path.join(root, d)
                        btn = QPushButton(f"📂 {os.path.relpath(folder_path, self.current_dir)}")
                        btn.setStyleSheet("text-align: left; padding: 6px; border: 1px solid #666;")
                        btn.clicked.connect(lambda checked, p=folder_path: self.open_folder(p))
                        self.list_layout.addWidget(btn)
                # Show matching PPT/PPTX files
                for f in files:
                    if f.lower().endswith((".pptx", ".ppt")) and self.search_text in f.lower():
                        file_path = os.path.join(root, f)
                        btn = QPushButton(f"📑 {os.path.relpath(file_path, self.current_dir)}")
                        btn.setStyleSheet("text-align: left; padding: 6px; border: 1px solid #888;")
                        btn.clicked.connect(lambda checked, p=file_path: self.open_template(p))
                        self.list_layout.addWidget(btn)

    def add_folder_and_files(self, folder_path):
        """Add folders and files non-recursively (used when no search)."""
        for item in sorted(os.listdir(folder_path)):
            path = os.path.join(folder_path, item)
            if os.path.isdir(path) and item.lower() != "slides":
                btn = QPushButton(f"📂 {item}")
                btn.setStyleSheet("text-align: left; padding: 6px; border: 1px solid #666;")
                btn.clicked.connect(lambda checked, p=path: self.open_folder(p))
                self.list_layout.addWidget(btn)
        for item in sorted(os.listdir(folder_path)):
            if item.lower().endswith((".pptx", ".ppt")):
                path = os.path.join(folder_path, item)
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
