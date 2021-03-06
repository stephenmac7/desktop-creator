#!/usr/bin/env python3

# Imports
import os
from getpass import getuser

# Global Constants
userhome = "/home/" + getuser()

# Input with Keyboard Interrupt
def kInput(pText):
  try:
    return input(pText)
  except KeyboardInterrupt:
    print("\nExiting")
    exit()

# The Important Functions
def createDesktop(inputList, fname):
  """Create Desktop file and write to it."""
  openFile = open(fname.replace("~", userhome), 'w')
  newlines = (line + "\n" for line in inputList)
  openFile.writelines(newlines)
  openFile.close()
  os.chmod(fname.replace("~", userhome), 0o755)


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

# Only for non-GUI run!
def getYN(prompt):
  userInput = kInput(prompt)
  if userInput.lower() == "y" or userInput.lower() == "yes":
    return True
  elif userInput.lower() == "n" or userInput.lower() == "no":
    return False
  else:
    print("For some reason or another your answer cannot",
          "be understood, please use a y/n next time.")
    exit()


def getDataFromCLI():
  """Get Information from the user in the Terminal."""
  print("""
Please choose a type of desktop file below:
1. Application (A shortcut to an application)
2. Link (A shortcut to a web link.)
  """)
  desktopType = int(kInput("Your option: "))
  if desktopType == 1:
    # Get the categories for the desktop file (application type):
    # Set the variable for the while loop and create an empty list.
    catInput = "nothing"
    categories = []
    # Give the user some instructions.
    print("\nAdd the categories for your application.",
          "When you have finished leave and empty line.")
    # Execute the while loop to add to the categories
    while catInput != "":
      catInput = kInput("Category: ")
      categories += [catInput]
    terminal = getYN("Open terminal on execute (y/n): ")
    desktopFile = applicationDesktop(kInput("Desktop File Version: "),
                                     kInput("Name: "),
                                     kInput("Generic Name: "),
                                     kInput("Comment/Description: "),
                                     kInput("File to execute: "),
                                     kInput("Icon: "), terminal, categories)
  elif desktopType == 2:
    desktopFile = linkDesktop(kInput("Desktop File Version: "),
                                     kInput("Name: "),
                                     kInput("Comment/Description: "),
                                     kInput("URL (Use protocol://): ").replace("~", userhome),
                                     kInput("Icon: ").replace("~", userhome))
  else:
    print("Your option was invalid.")
    exit()
  filename = kInput("Filename: ")
  createDesktop(desktopFile, filename)


# If the file is run directly run getDataFromCLI()
if __name__ == "__main__":
  getDataFromCLI()
