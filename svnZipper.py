#! /usr/bin/python -B

###############################################################
########				 svnZipper.py				  ########
########			 Made by Thomas Roberts			######## 
########				  17/02/2016				   ########
########				 Version  0.1				   ########	
###############################################################


import os
import sys
import logging
import shutil
import pysvn
import zipfile
import colorama
from subprocess import call

# ASCII Colors for the terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# welcome
# Input:- None
# Output:- None
# Prints welcome headeer for LeeDrOiD
def welcome():
	print bcolors.OKGREEN +  "$$\\                           $$$$$$$\\             $$$$$$\\  $$\\ $$$$$$$\\        $$\\   $$\\ $$\\           $$\\         $$\\     $$\\           " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$ |                          $$  __$$\\           $$  __$$\\ \\__|$$  __$$\\       $$$\\  $$ |\\__|          $$ |        $$ |    $$ |          " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$ |       $$$$$$\\   $$$$$$\\  $$ |  $$ | $$$$$$\\  $$ /  $$ |$$\\ $$ |  $$ |      $$$$\\ $$ |$$\\  $$$$$$\\  $$$$$$$\\  $$$$$$\\   $$ |$$\\   $$\\ " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$ |      $$  __$$\\ $$  __$$\\ $$ |  $$ |$$  __$$\\ $$ |  $$ |$$ |$$ |  $$ |      $$ $$\\$$ |$$ |$$  __$$\\ $$  __$$\\ \\_$$  _|  $$ |$$ |  $$ |" + bcolors.ENDC
	print bcolors.OKGREEN +  "$$ |      $$$$$$$$ |$$$$$$$$ |$$ |  $$ |$$ |  \\__|$$ |  $$ |$$ |$$ |  $$ |      $$ \\$$$$ |$$ |$$ /  $$ |$$ |  $$ |  $$ |    $$ |$$ |  $$ |" + bcolors.ENDC
	print bcolors.OKGREEN +  "$$ |      $$   ____|$$   ____|$$ |  $$ |$$ |      $$ |  $$ |$$ |$$ |  $$ |      $$ |\\$$$ |$$ |$$ |  $$ |$$ |  $$ |  $$ |$$\\ $$ |$$ |  $$ |" + bcolors.ENDC
	print bcolors.OKGREEN +  "$$$$$$$$\\ \\$$$$$$$\\ \\$$$$$$$\\ $$$$$$$  |$$ |       $$$$$$  |$$ |$$$$$$$  |      $$ | \\$$ |$$ |\\$$$$$$$ |$$ |  $$ |  \\$$$$  |$$ |\\$$$$$$$ |" + bcolors.ENDC
	print bcolors.OKGREEN +  "\\________| \\_______| \\_______|\\_______/ \\__|       \\______/ \\__|\\_______/       \\__|  \\__|\\__| \\____$$ |\\__|  \\__|   \\____/ \\__| \\____$$ |" + bcolors.ENDC
	print bcolors.OKGREEN +  "                                                                                              $$\\   $$ |                        $$\\   $$ |" + bcolors.ENDC
	print bcolors.OKGREEN +  "                                                                                              \\$$$$$$  |                        \\$$$$$$  |" + bcolors.ENDC
	print bcolors.OKGREEN +  "                                                                                               \\______/                          \\______/ " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$$$$$$\\            $$\\ $$\\       $$\\        $$$$$$\\                      $$\\             $$\\                                             " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$  __$$\\           \\__|$$ |      $$ |      $$  __$$\\                     \\__|            $$ |                                            " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$ |  $$ |$$\\   $$\\ $$\\ $$ | $$$$$$$ |      $$ /  \\__| $$$$$$$\\  $$$$$$\\  $$\\  $$$$$$\\  $$$$$$\\                                           " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$$$$$$\\ |$$ |  $$ |$$ |$$ |$$  __$$ |      \\$$$$$$\\  $$  _____|$$  __$$\\ $$ |$$  __$$\\ \\_$$  _|                                          " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$  __$$\\ $$ |  $$ |$$ |$$ |$$ /  $$ |       \\____$$\\ $$ /      $$ |  \\__|$$ |$$ /  $$ |  $$ |                                            " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$ |  $$ |$$ |  $$ |$$ |$$ |$$ |  $$ |      $$\\   $$ |$$ |      $$ |      $$ |$$ |  $$ |  $$ |$$\\                                         " + bcolors.ENDC
	print bcolors.OKGREEN +  "$$$$$$$  |\\$$$$$$  |$$ |$$ |\\$$$$$$$ |      \\$$$$$$  |\\$$$$$$$\\ $$ |      $$ |$$$$$$$  |  \\$$$$  |                                        " + bcolors.ENDC
	print bcolors.OKGREEN +  "\\_______/  \\______/ \\__|\\__| \\_______|       \\______/  \\_______|\\__|      \\__|$$  ____/    \\____/                                         " + bcolors.ENDC
	print bcolors.OKGREEN +  "                                                                              $$ |                                                        " + bcolors.ENDC
	print bcolors.OKGREEN +  "                                                                              $$ |                                                        " + bcolors.ENDC
	print bcolors.OKGREEN +  "                                                                              \\__|                                                        " + bcolors.ENDC


# Clear shell script
# Input:- None
# Output:- None
# Description: This function will clear the shell 
def cls():
	os.system(['clear','cls'][os.name == 'nt'])


# Set Up the Main menu
# Input:- None
# Output:- Returns a ID (string)
# Description: Display main menu items
def mainMenu():
	cls()
	welcome()
	menuItems = ["Build HTC 10 Nightly zip", "Build HTC One M9 Nightly zip", "Build HTC One M8 Nightly zip", "Exit"]
	i = 1

	print "Choice one of the following options:"
	for item in menuItems:
		print "%d. %s" % (i, menuItems[i-1])
		i+=1

	option = raw_input("\nInput your selection -> ")

	try:
		option = int (option)
		if(option > len(menuItems) or option < 1):
			logging.error("%d selection is not in range", option)
		else:
			logging.debug("You selected option %d '%s'", option,menuItems[option-1])
	except ValueError:
		logging.error("%s is not a valid option", option)

	if option == 1:
		return "10"
	elif option == 2:
		return "m9"
	elif option == 3:
		return "m8"
	elif option == 4:
		return "exit"


# Build the zip
# Input:- Dest dir
# Input: Zip name
# Description: Builds the zip
def buildZip(src, dst):
	zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
	abs_src = os.path.abspath(src)
	exclude = [".svn"]
	for dirname, subdirs, files in os.walk(src):
		subdirs[:] = [d for d in subdirs if d not in exclude]
		for filename in files:
			absname = os.path.abspath(os.path.join(dirname, filename))
			arcname = absname[len(abs_src) + 1:]
			#print 'zipping %s as %s' % (os.path.join(dirname, filename),arcname)
			zf.write(absname, arcname)
	zf.close()



# Checkout the SVN
# Input:- Object to svnID
# Input:- String for working directory
# Description: Checkout the working directory
def checkoutSVN(svnID, remoteSvn, workingDir):
	svnID.checkout(remoteSvn, workingDir)

# Main
if __name__ == "__main__":

	# Initialise all logging configuration, only levels equal to info or above will be logged, the stream will be stdout and message will appear as the following:
	# DEBUG: This is DEBUG (only if configured)
	# INFO: This is information
	# Warning: This is a warning
	# Error: This is a error
	logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Init coloama for ASCII colours in the terminal
	colorama.init()
    # Remote SVN locations
	htcM8Svn = "http://www.soldier9312-xda.de/svn/leedroid-m8/trunk"
	htcM9Svn = "http://www.soldier9312-xda.de/svn/leedroid-m9/trunk"
	htc10Svn = "http://www.soldier9312-xda.de/svn/leedroid-10/trunk"
     
	# Checkout folders
	destM8Checkout = "HTC_M8_Trunk"
	destM9Checkout = "HTC_M9_Trunk"
	dest10Checkout = "HTC_10_Trunk"

	if (os.name == "nt"):
		windows = True
		call(["mode", "140,60"], shell=True)
	else:
		windows = False


	while (1):
		# Display the Main Menu
		returnOption = mainMenu()

		cls()
		welcome()
		svnClient = pysvn.Client()
		if returnOption == "10":
			logging.info("Checking out HTC 10 Trunk")
			checkoutSVN(svnClient, htc10Svn, dest10Checkout)
			logging.info("Building zip")
			buildZip(dest10Checkout, "HTC_10_Build")
		elif returnOption == "m9":
			logging.info("Checking out HTC One M9 Trunk")
			checkoutSVN(svnClient, htcM9Svn, destM9Checkout)
			logging.info("Building zip")
			buildZip(destM9Checkout, "HTC_M9_Build")
		elif returnOption == "m8":
			logging.info("Checking out HTC One M8 Trunk")
			checkoutSVN(svnClient, htcM8Svn, destM8Checkout)
			logging.info("Building zip")
			buildZip(destM8Checkout, "HTC_M8_Build")
		elif returnOption == "exit":
			cls()
			sys.exit()
		cls()
