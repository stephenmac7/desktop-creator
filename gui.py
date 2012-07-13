# Imports
import sys
import desktopFile
from getpass import getuser
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
    self.mainWidget = loader.load(file, self)
    file.close()
    # Connect things
    self.mainWidget.createButton.clicked.connect(self.createClicked)
    # Stop from resizing window
    self.setFixedSize(self.mainWidget.size())
    # Extra stuff to do to the window
    self.center()
    self.show()

  def createClicked(self):
    userhome = "/home/" + getuser()
    version = self.mainWidget.versionEdit.text()
    name = self.mainWidget.nameEdit.text()
    comment = self.mainWidget.commentEdit.text()
    icon = self.mainWidget.iconEdit.text().replace("~", userhome)
    terminal = self.mainWidget.terminalBox.isChecked()
    if self.mainWidget.appRadio.isChecked():
      categories = [x.text() for x in self.mainWidget.findChildren(QCheckBox) if x.isChecked()]
      if self.mainWidget.otherEdit1.text() != "":
        categories += [self.mainWidget.otherEdit1.text()]
      if self.mainWidget.otherEdit2.text() != "":
        categories += [self.mainWidget.otherEdit2.text()]
      if self.mainWidget.otherEdit3.text() != "":
        categories += [self.mainWidget.otherEdit3.text()]
      generic = self.mainWidget.genericEdit.text()
      toExec = self.mainWidget.execEdit.text()
      toWrite = desktopFile.applicationDesktop(version, name, generic, comment, toExec,
                                               icon, terminal, categories)
    else:
      linkTo = self.mainWidget.protocolCombo.currentText() + self.mainWidget.urlEdit.text().replace("~", userhome)
      toWrite = desktopFile.linkDesktop(version, name, comment, linkTo, icon)
    desktopFile.createDesktop(toWrite, self.mainWidget.filenameEdit.text())
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
