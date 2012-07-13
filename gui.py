# Imports
import sys
import desktopfile
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtUiTools import QUiLoader

# Main Application Class
class mainApp(QWidget):
  def __init__(self):
    """Constructor."""
    super(mainApp, self).__init__()
    self.initUI()

  def initUI(self):
    # Set the title of the window
    self.setWindowTitle("Desktop File Creator")
    # Load UI
    loader = QUiLoader()
    file = QFile("main_gui.ui")
    file.open(QFile.ReadOnly)
    self.myWidget = loader.load(file, self)
    file.close()
    # Connect things
    self.myWidget.createButton.clicked.connect(self.createClicked)
    # Extra stuff to do to the window
    self.center()
    self.show()

  def createClicked(self):
    print(self.myWidget.nameEdit.text())
    QCoreApplication.quit()

  def center(self):
    """Center the window."""
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

def main():
  app = QApplication(sys.argv)
  ex = mainApp()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
