import os
import tempfile
import shutil
import atexit
import win32com.client

class PPTLoader:
    def __init__(self, pptx_path, out_dir=None):
        # Normalize path
        self.pptx_path = os.path.abspath(pptx_path)

        # Use temp folder if no output directory provided
        if out_dir is None:
            self.out_dir = tempfile.mkdtemp(prefix="slides_")
        else:
            self.out_dir = out_dir

        # Register cleanup on application exit
        atexit.register(self.cleanup)

    def export_slides(self):
        print(f"Exporting slides from: {self.pptx_path}")
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        try:
            safe_path = self.pptx_path.replace("/", "\\")
            presentation = powerpoint.Presentations.Open(safe_path, WithWindow=False)

            slides = []
            for i, slide in enumerate(presentation.Slides, start=1):
                img_path = os.path.join(self.out_dir, f"slide_{i:03}.png")
                slide.Export(os.path.abspath(img_path), "PNG", 800, 600)
                slides.append(img_path)
                print(f"Exported slide {i}: {img_path}")

            presentation.Close()
            return slides

        finally:
            powerpoint.Quit()
            print("PowerPoint application closed.")

    def cleanup(self):
        """Delete temporary slides folder when app closes"""
        if os.path.exists(self.out_dir):
            print(f"Cleaning up temporary slides folder: {self.out_dir}")
            shutil.rmtree(self.out_dir, ignore_errors=True)
