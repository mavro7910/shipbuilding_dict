#!/usr/bin/env python3
"""
조선업 축약어 사전 애플리케이션
메인 진입점
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """애플리케이션 실행"""
    app = QApplication(sys.argv)
    app.setApplicationName('조선업 사전')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()