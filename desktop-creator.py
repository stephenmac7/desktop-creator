#!/usr/share/env python3

# Imports
import os
import sys
from getpass import getuser
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtUiTools import QUiLoader

# Global Constants
userhome = "/home/" + getuser()

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
    if QFile.exists("desktop_creator.ui"):
      file = QFile("desktop_creator.ui")
    elif QFile.exists("/usr/share/desktop_creator/desktop_creator.ui"):
      file = QFile("/usr/share/desktop_creator/desktop_creator.ui")
    else:
      print("The UI file cannot be found. Please check your installation.")
      sys.exit(256)
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
#    userhome = "/home/" + getuser()
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
      toWrite = applicationDesktop(version, name, generic, comment, toExec,
                                   icon, terminal, categories)
    else:
      linkTo = self.mainWidget.protocolCombo.currentText() + self.mainWidget.urlEdit.text().replace("~", userhome)
      toWrite = linkDesktop(version, name, comment, linkTo, icon)
    createDesktop(toWrite, self.mainWidget.filenameEdit.text())
    QCoreApplication.quit()

  def center(self):
    """Center the window."""
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

# Important Functions
def applicationDesktop(version, name, generic, comment, execute,
                       icon, terminal, categories):
  """Put together application the desktop file."""
  # Extra information about parameters:
  # - Version is a string
  # - Terminal is a boolean
  # - Categories is a list
  endFile = []
  endFile += ["[Desktop Entry]"]
  endFile += ["Type=Application"]
  endFile += ["Version=" + version]
  endFile += ["Name=" + name]
  endFile += ["GenericName=" + generic]
  endFile += ["Comment=" + comment]
  endFile += ["Exec=" + execute]
  endFile += ["Icon=" + icon]
  endFile += ["Terminal=" + str(terminal).lower()]
  catString = ""
  for category in categories:
    if category != "":
      catString += category + ";"
  endFile += ["Categories=" + catString]
  return endFile

def linkDesktop(version, name, comment, url, icon):
  """Put together the link desktop file."""
  endFile = []
  endFile += ["[Desktop Entry]"]
  # Version is a string
  endFile += ["Version=" + version]
  endFile += ["Type=Link"]
  endFile += ["Name=" + name]
  endFile += ["Comment=" + comment]
  endFile += ["URL=" + url]
  endFile += ["Icon=" + icon]
  return endFile

def createDesktop(inputList, fname):
  """Create Desktop file and write to it."""
  openFile = open(fname.replace("~", userhome), 'w')
  newlines = (line + "\n" for line in inputList)
  openFile.writelines(newlines)
  openFile.close()
  os.chmod(fname.replace("~", userhome), 0o755)

# Execute the GUI application
def main():
  app = QApplication(sys.argv)
  ex = mainApp()
  sys.exit(app.exec_())

# If this file is run then execute main
if __name__ == '__main__':
  main()
