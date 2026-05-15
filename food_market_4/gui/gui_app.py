import sys
from PyQt5.QtWidgets import QApplication
from gui.mvc_views import MarketView
from gui.mvc_controllers import MarketController


def run_gui():
    app = QApplication(sys.argv)
    view = MarketView()
    controller = MarketController(view)
    view.show()
    sys.exit(app.exec_())