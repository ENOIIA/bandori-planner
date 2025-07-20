import os
import sys

from PyQt6.QtCore import QDir
from PyQt6.QtWidgets import QApplication

from src.gui.main_window import MainWindow
from src.gui.qss_loader import QSSLoader


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # 设置资源路径
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')

    QDir.addSearchPath('qss', os.path.join(base_path, 'styles'))

    style_sheet = QSSLoader.read_qss_file('qss:style.qss')
    main_window.setStyleSheet(style_sheet)

    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
