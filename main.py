import sys
from PyQt5.QtWidgets import QApplication
from control_window import ControlWindow

if __name__ == "__main__":
    print("Starting PPT Presenter application...")
    app = QApplication(sys.argv)
    
    print("Initializing main window...")
    window = ControlWindow()
    window.showMaximized()
    print("Main window displayed")
    
    exit_code = app.exec_()
    print(f"Application exited with code {exit_code}")
    sys.exit(exit_code)
