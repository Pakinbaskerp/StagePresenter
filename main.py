import sys
from PyQt5.QtWidgets import QApplication
from control_window import ControlWindow

if __name__ == "__main__":
    print("Starting Projex application...")
    app = QApplication(sys.argv)

    # Apply dark/black theme globally
    app.setStyleSheet("""
        QWidget {
            background-color: #121212;  /* dark black background */
            color: #ffffff;            /* white text */
            font-family: Arial, Helvetica, sans-serif;
        }
        QPushButton {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 5px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #333333;
        }
        QLabel {
            color: #ffffff;
        }
        QScrollArea {
            background-color: #121212;
        }
        QProgressDialog {
            background-color: #1e1e1e;
            color: #ffffff;
        }
    """)

    print("Initializing main window...")
    window = ControlWindow()
    window.showMaximized()
    print("Main window displayed")

    exit_code = app.exec_()
    print(f"Application exited with code {exit_code}")
    sys.exit(exit_code)
