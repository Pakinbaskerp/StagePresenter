import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QProgressDialog, QApplication
from PyQt5.QtCore import Qt

from thumbnail_panel import ThumbnailPanel
from template_panel import TemplatePanel
from preview_panel import PreviewPanel
from ppt_loader import PPTLoader


class ControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projex")
        self.setGeometry(200, 200, 1400, 800)

        print("Initializing ControlWindow...")

        # Core state
        self.slides = []
        self.current_index = 0

        # ---- Layout ----
        widget = QWidget()
        main_layout = QHBoxLayout(widget)

        # Panels
        print("Creating ThumbnailPanel")
        self.thumbnail_panel = ThumbnailPanel(self.load_pptx, self.on_slide_selected)

        print("Creating TemplatePanel")
        # Dynamically get Documents/Templates path
        documents_path = os.path.join(os.path.expanduser("~"), "Documents")
        templates_path = os.path.join(documents_path, "Templates")
        os.makedirs(templates_path, exist_ok=True)  # Create if missing
        print(f"Using templates path: {templates_path}")

        self.template_panel = TemplatePanel(
            templates_path,
            on_template_selected=self.load_pptx
        )

        print("Creating PreviewPanel")
        self.preview_panel = PreviewPanel()

        # Add with ratios (Template first, then thumbnails, then preview wide)
        main_layout.addWidget(self.template_panel, 1)
        main_layout.addWidget(self.thumbnail_panel, 1)
        main_layout.addWidget(self.preview_panel, 4)

        self.setCentralWidget(widget)
        print("ControlWindow initialized successfully")

    def load_pptx(self, file_path):
        """Load PPTX, export slides, and populate thumbnails with loader."""
        if not file_path:
            print("No file_path provided to load_pptx")
            return

        print(f"Loading PPTX: {file_path}")
        out_dir = os.path.join(os.path.dirname(file_path), "slides")
        os.makedirs(out_dir, exist_ok=True)
        print(f"Slides output directory: {out_dir}")

        # Show loader
        print("Showing loader dialog")
        loader_dialog = QProgressDialog("Loading PowerPoint...", None, 0, 0, self)
        loader_dialog.setWindowModality(Qt.ApplicationModal)
        loader_dialog.setWindowTitle("Please wait")
        loader_dialog.setCancelButton(None)
        loader_dialog.show()
        QApplication.processEvents()

        try:
            loader = PPTLoader(file_path, out_dir)
            print("Exporting slides from PPTX")
            self.slides = loader.export_slides()
            print(f"Exported {len(self.slides)} slides")
        except Exception as e:
            print(f"Error loading PPTX: {e}")
            raise
        finally:
            loader_dialog.close()
            print("Loader dialog closed")

        self.current_index = 0
        print("Showing thumbnails in ThumbnailPanel")
        self.thumbnail_panel.show_thumbnails(self.slides)  # populate thumbnails
        self.show_slide()  # show first slide in preview

    def show_slide(self):
        """Show the current slide in the preview panel."""
        if not self.slides:
            print("No slides available to show")
            return
        slide_path = self.slides[self.current_index]
        print(f"Showing slide {self.current_index + 1}: {slide_path}")
        self.preview_panel.show_slide(slide_path)

    def on_slide_selected(self, index):
        """Called when user clicks a thumbnail."""
        if index < 0 or index >= len(self.slides):
            print(f"Invalid slide index selected: {index}")
            return
        self.current_index = index
        print(f"Slide selected: {index + 1}")
        self.show_slide()   # 👈 show clicked slide immediately
