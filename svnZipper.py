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
import time
import ConfigParser
import md5
import Tkinter
import tkFileDialog
import hashlib
from subprocess import call
from multiprocessing.pool import ThreadPool

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


def getRemoteRevision(svnID, url):
	headrev = pysvn.Revision( pysvn.opt_revision_kind.head )            
	revlog = svnID.log( url, revision_start=headrev, revision_end=headrev, discover_changed_paths=False)
	revision = revlog[0].revision.number
	return int(revision)
	
def getLocalRevision(svnID, workingDir):
	revision = svnID.info(workingDir).get("revision").number
	return int(revision)
	
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
	menuItems = ["Build "+bcolors.OKGREEN+"HTC 10"+bcolors.ENDC+" Nightly zip", "Build "+bcolors.OKGREEN+"HTC One M9"+bcolors.ENDC+" Nightly zip", "Build "+bcolors.OKGREEN+"HTC One M8"+bcolors.ENDC+" Nightly zip", "Configure working and build directories", "Exit"]
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
		return "config"
	elif option == 5:
		return "exit"


# Build the zip
# Input:- Dest dir
# Input: Zip name
# Description: Builds the zip
def buildZip(src, dst):
	zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
	abs_src = os.path.abspath(src)
	exclude = [".svn", "libs", "Builds"]
	#excludeFiles = ["UpdateAndBuild.bat", "svnZipper.exe", "svnZipper.cfg"]
	total = 0
	for dirname, subdirs, files in os.walk(src):
		subdirs[:] = [d for d in subdirs if d not in exclude]
		for filename in files:
			if filename == "supersu.zip":
				absname = os.path.abspath(os.path.join(dirname, filename))
				arcname = absname[len(abs_src) + 1:]
				total += os.path.getsize(absname)
			if not filename.endswith( ('.bat','.exe', 'zip', '.cfg', '.zip.md5', '.md5') ):
				absname = os.path.abspath(os.path.join(dirname, filename))
				arcname = absname[len(abs_src) + 1:]
				total += os.path.getsize(absname)
	
	current = 0
	for dirname, subdirs, files in os.walk(src):
		subdirs[:] = [d for d in subdirs if d not in exclude]
		for filename in files:
			if filename == "supersu.zip":
				absname = os.path.abspath(os.path.join(dirname, filename))
				arcname = absname[len(abs_src) + 1:]
				percent = 100 * current / total
				sys.stdout.write("%sPROGRESS: %d%%   \r%s"% (bcolors.OKGREEN, percent, bcolors.ENDC))
				sys.stdout.flush()
				zf.write(absname, arcname)
				current += os.path.getsize(absname)	
			if not filename.endswith( ('.bat','.exe', '.zip', '.cfg', '.zip.md5', '.md5') ):
				absname = os.path.abspath(os.path.join(dirname, filename))
				arcname = absname[len(abs_src) + 1:]
				percent = 100 * current / total
				sys.stdout.write("%sPROGRESS: %d%%   \r%s"% (bcolors.OKGREEN, percent, bcolors.ENDC))
				sys.stdout.flush()
				zf.write(absname, arcname)
				current += os.path.getsize(absname)
	zf.close()
	logging.info("Done zipping %s.zip", dst)



# Checkout the SVN
# Input:- Object to svnID
# Input:- String for working directory
# Description: Checkout the working directory
def checkoutSVN(svnID, remoteSvn, workingDir):
	svnID.checkout(remoteSvn, workingDir)
	
# Update the SVN
# Input:- Object to svnID
# Input:- String for working directory
# Description: Update the working directory
def updateSVN(svnID, workingDir):
	svnID.update(workingDir)

def getList(svnID, url):
	list = svnID.list( url, recurse=True)
	return int(len(list))
	
def getRemoteFileList(svnID, url):
	number = 0
	pool = ThreadPool(processes=1)
	async_result = pool.apply_async(getList, (svnID, url))
	while async_result.ready() == False:
		sys.stdout.write("%sPROCESS: Reading %s   \r%s"% (bcolors.OKGREEN, url, bcolors.ENDC))
		time.sleep(1)
		sys.stdout.write("%sPROCESS: Reading %s.   \r%s"% (bcolors.OKGREEN, url, bcolors.ENDC))
		time.sleep(1)
		sys.stdout.write("%sPROCESS: Reading %s..   \r%s"% (bcolors.OKGREEN, url, bcolors.ENDC))
		time.sleep(1)
		sys.stdout.write("%sPROCESS: Reading %s...   \r%s"% (bcolors.OKGREEN, url, bcolors.ENDC))
		time.sleep(1)
		sys.stdout.flush()
	sys.stdout.flush()
	logging.info("Finsihed reading %s", url)
	return async_result.get()
	
def getFileCount(path):
	total = 0
	exclude = [".svn"]
	for dirname, subdirs, files in os.walk(path):
		subdirs[:] = [d for d in subdirs if d not in exclude]
		for filename in files:
			absname = os.path.abspath(os.path.join(dirname, filename))
			total += 1
	return total

## Yes No Promt
def queryYesNo(question, default="yes"):

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def md5(zipPath, zipName):
	fname = zipPath + ".zip"
	hash_md5 = hashlib.md5()
	with open(fname, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
			
	f = open(zipPath+".zip"+".md5", 'w')
	f.write(hash_md5.hexdigest()+ " *"+ zipName + ".zip")
	f.close()

def makeMd5Sum(path, zipName):
	pool = ThreadPool(processes=1)
	async_result = pool.apply_async(md5, (path, zipName))
	while async_result.ready() == False:
		sys.stdout.write("%sPROCESS: Making MD5 checksum %s.zip.md5 file   \r%s"% (bcolors.OKGREEN, path, bcolors.ENDC))
		time.sleep(1)
		sys.stdout.write("%sPROCESS: Making MD5 checksum %s.zip.md5 file.   \r%s"% (bcolors.OKGREEN, path, bcolors.ENDC))
		time.sleep(1)
		sys.stdout.write("%sPROCESS: Making MD5 checksum %s.zip.md5 file..   \r%s"% (bcolors.OKGREEN, path, bcolors.ENDC))
		time.sleep(1)
		sys.stdout.write("%sPROCESS: Making MD5 checksum %s.zip.md5 file...   \r%s"% (bcolors.OKGREEN, path, bcolors.ENDC))
		time.sleep(1)
		sys.stdout.flush()
	sys.stdout.flush()
	logging.info("MD5 file %s.zip.md5 saved					 					", path)

# Check Arguments
# Input:- Source directory
# Input:- Destination directory
# Output:- Boolean, True is everything is ok
# This function will check the source and destination directory
def checkArgs(path):

    returnValue = True
    

    if not os.path.isdir(path):
        logging.warning("Directory %s doesn't exist", path)
        logging.info("Making directory as it doesn't exists")
        os.makedirs(path)

    return returnValue
							 
# Main
if __name__ == "__main__":

	# Initialise all logging configuration, only levels equal to info or above will be logged, the stream will be stdout and message will appear as the following:
	# DEBUG: This is DEBUG (only if configured)
	# INFO: This is information
	# Warning: This is a warning
	# Error: This is a error
	logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s: %(message)s')
	
	# Current directory
	workingDir = os.path.dirname(os.path.realpath(__file__))
	
	# Configuration
	config = ConfigParser.RawConfigParser()
	configFile="svnZipper.cfg"
	
	if not os.path.isfile(configFile):
		config.add_section('SVNZipper')
		config.set('SVNZipper', 'destM8Checkout', os.path.realpath(workingDir))
		config.set('SVNZipper', 'destM9Checkout', os.path.realpath(workingDir))
		config.set('SVNZipper', 'dest10Checkout', os.path.realpath(workingDir))
		
		config.set('SVNZipper', 'builds', os.path.realpath(workingDir +"/"+"Builds"))
		
		# Writing our configuration file to 'example.cfg'
		with open(configFile, 'wb') as configfile:
			config.write(configfile)
    
    # Init coloama for ASCII colours in the terminal
	colorama.init()
	
    # Remote SVN locations
	htcM8Svn = "http://www.soldier9312-xda.de/svn/leedroid-m8/trunk"
	htcM9Svn = "http://www.soldier9312-xda.de/svn/leedroid-m9/trunk"
	htc10Svn = "http://www.soldier9312-xda.de/svn/leedroid-10/trunk"
     
	# Checkout folders
	config.read(configFile)
	destM8Checkout = config.get('SVNZipper', 'destM8Checkout')
	destM9Checkout = config.get('SVNZipper', 'destM9Checkout')
	dest10Checkout = config.get('SVNZipper', 'dest10Checkout')
	
	# Build folders
	builds = config.get('SVNZipper', 'builds')
	if not os.path.isdir(builds):
		os.makedirs(builds)


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
			workingDest = os.path.join(workingDir, dest10Checkout)
			Svn = htc10Svn
			zipPrefix = "LeeDrOiD_10"
			origonalFileCount = getFileCount(workingDest)
		elif returnOption == "m9":
			workingDest = os.path.join(workingDir, destM8Checkout)
			Svn = htcM9Svn
			zipPrefix = "LeeDrOiD_M9"
			origonalFileCount = getFileCount(workingDest)
		elif returnOption == "m8":
			workingDest = os.path.join(workingDir, destM8Checkout)
			Svn = htcM8Svn
			zipPrefix = "LeeDrOiD_M8"
			origonalFileCount = getFileCount(workingDest)
		elif returnOption == "config":
			# We have no arguments pass to use we will prompt the user
			
			if queryYesNo("QUESTION: Set HTC 10 working directory? "):
				root = Tkinter.Tk()
				root.withdraw() # hide root
				HTC10Working = tkFileDialog.askdirectory(parent=root,initialdir=workingDir,title="Please select working directory for LeeDrOiD's HTC 10 ROM")
				root.destroy()
			else:
				HTC10Working = ""
			if HTC10Working == "":
				HTC10Working = os.path.realpath(dest10Checkout)
				logging.info("HTC 10 working directory was skipped %s will be used", HTC10Working)
			else:
				logging.info("HTC 10 working directory set to %s", HTC10Working)
				checkArgs(HTC10Working)
			if queryYesNo("QUESTION: Set HTC M9 working directory? "):
				root = Tkinter.Tk()
				root.withdraw() # hide root
				m9Working = tkFileDialog.askdirectory(parent=root,initialdir=workingDir,title="Please select working directory for LeeDrOiD's HTC M9 ROM")
				root.destroy()
			else:
				m9Working = ""
			if m9Working == "":
				m9Working = os.path.realpath(destM9Checkout)
				logging.info("HTC M9 working directory was skipped %s will be used", m9Working)
			else:
				logging.info("HTC M9 working directory set to %s", m9Working)
				checkArgs(m9Working)
			if queryYesNo("QUESTION: Set HTC M8 working directory? "):
				root = Tkinter.Tk()
				root.withdraw() # hide root
				m8Working = tkFileDialog.askdirectory(parent=root,initialdir=workingDir,title="Please select working directory for LeeDrOiD's HTC M8 ROM")
				root.destroy()
			else:
				m8Working = ""
			if m8Working == "":
				m8Working = os.path.realpath(destM8Checkout)
				logging.info("HTC M8 working directory was skipped %s will be used", m8Working)
			else:
				logging.info("HTC M8 working directory set to %s", m8Working)
				checkArgs(m8Working)
			if queryYesNo("QUESTION: Set directory where your builds (zips) will be stored? "):
				root = Tkinter.Tk()
				root.withdraw() # hide root
				buildsPath = tkFileDialog.askdirectory(parent=root,initialdir=workingDir,title="Please select your build directory")
				root.destroy()
			else:
				buildsPath = ""
			if buildsPath == "":
				buildsPath = os.path.realpath(builds)
				logging.info("Build directory was skipped %s will be used", buildsPath)
			else:
				logging.info("Build directory set to %s", buildsPath)
				checkArgs(buildsPath)
				
			config.set('SVNZipper', 'destM8Checkout', os.path.realpath(m8Working))
			config.set('SVNZipper', 'destM9Checkout', os.path.realpath(m9Working))
			config.set('SVNZipper', 'dest10Checkout', os.path.realpath(HTC10Working))
			config.set('SVNZipper', 'builds', os.path.realpath(buildsPath))
		
			# Writing our configuration file to 'example.cfg'
			with open(configFile, 'wb') as configfile:
				config.write(configfile)
				
			# Checkout folders
			config.read(configFile)
			destM8Checkout = config.get('SVNZipper', 'destM8Checkout')
			destM9Checkout = config.get('SVNZipper', 'destM9Checkout')
			dest10Checkout = config.get('SVNZipper', 'dest10Checkout')
			
			# Build folders
			builds = config.get('SVNZipper', 'builds')
			
			raw_input("\nPress Enter to Return to the Main Menu...")
		elif returnOption == "exit":
			cls()
			sys.exit()
		
		if returnOption == "10" or returnOption == "m9" or returnOption == "m8":
			if not os.path.isdir(workingDest):
				logging.warning("%s does not exist, so this directory will be made", workingDest)
				os.makedirs(workingDest)
			try:
				getRemoteRevision(svnClient, workingDest) == getLocalRevision(svnClient, workingDest)
				isWorking = True
			except:
				isWorking = False
				
			if not isWorking:
				logging.info("Checking out %s", Svn)

				pool = ThreadPool(processes=1)
				async_result = pool.apply_async(checkoutSVN, (svnClient, Svn, workingDest))
				while async_result.ready() == False:
					curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
					sys.stdout.write("%sPROCESS: Checked out %d files   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
					time.sleep(1)
					curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
					sys.stdout.write("%sPROCESS: Checked out %d files.   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
					time.sleep(1)
					curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
					sys.stdout.write("%sPROCESS: Checked out %d files..   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
					time.sleep(1)
					curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
					sys.stdout.write("%sPROCESS: Checked out %d files...   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
					time.sleep(1)
					sys.stdout.flush()
				sys.stdout.flush()
				logging.info("Finsihed checking out %s into %s", Svn, workingDest) 
			else:
				if (getRemoteRevision(svnClient, workingDest) == getLocalRevision(svnClient, workingDest)):
					logging.info("Your local repository is alread up to date")
					question = "QUESTION: The remote repository is at revision %d, your local repository is at revision %d. Would you like to force a update?" % (getRemoteRevision(svnClient, workingDest), getLocalRevision(svnClient, workingDest))
					forceUpdate = queryYesNo(question)
					if forceUpdate:
						logging.info("Updating %s repository", workingDest)
						pool = ThreadPool(processes=1)
						async_result = pool.apply_async(updateSVN, (svnClient, workingDest))
						while async_result.ready() == False:
							curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
							sys.stdout.write("%sPROCESS: Updated %d files   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
							time.sleep(1)
							curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
							sys.stdout.write("%sPROCESS: Updated %d files.   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
							time.sleep(1)
							curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
							sys.stdout.write("%sPROCESS: Updated %d files..   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
							time.sleep(1)
							curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
							sys.stdout.write("%sPROCESS: Updated %d files...   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
							time.sleep(1)
							sys.stdout.flush()
						sys.stdout.flush()
						logging.info("Finsihed updated %s", workingDest)
						forceUpdate = False
				elif (getRemoteRevision(svnClient, workingDest) != getLocalRevision(svnClient, workingDest)):
					logging.info("Updating %s repository", workingDest)
					pool = ThreadPool(processes=1)
					async_result = pool.apply_async(updateSVN, (svnClient, workingDest))
					while async_result.ready() == False:
						curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
						sys.stdout.write("%sPROCESS: Updated %d files   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
						time.sleep(1)
						curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
						sys.stdout.write("%sPROCESS: Updated %d files.   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
						time.sleep(1)
						curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
						sys.stdout.write("%sPROCESS: Updated %d files..   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
						time.sleep(1)
						curentFileCount = abs(origonalFileCount - getFileCount(workingDest))
						sys.stdout.write("%sPROCESS: Updated %d files...   \r%s"% (bcolors.OKGREEN, curentFileCount, bcolors.ENDC))
						time.sleep(1)
						sys.stdout.flush()
					sys.stdout.flush()
					logging.info("Finsihed updated %s", workingDest)
			
			if not os.path.isdir(builds):
				os.makedirs(builds)
			zipName = zipPrefix + "_R%d" % (getLocalRevision(svnClient, workingDest))
			zipPath = os.path.join(builds, zipName)
			if os.path.exists(zipPath+".zip"):
				logging.info("%s.zip alread exists.", zipPath)
				question = "QUESTION: Would you like to rebuild?"
				forceZip = queryYesNo(question)
				if forceZip:
					logging.warning("Removing old %s.zip", zipPath)
					os.remove(zipPath+".zip")
					if os.path.isfile(zipPath+".zip.md5"):
						logging.warning("Removing old %s.zip.md5", zipPath)
						os.remove(zipPath+".zip.md5")
					logging.info("Making %s.zip", zipPath)
					buildZip(workingDest, zipPath)
					if os.path.isfile(zipPath+".zip"):
						logging.info("Making MD5 checksum")
						makeMd5Sum(zipPath, zipName)
			else:
				logging.info("Making %s.zip", zipPath)
				buildZip(workingDest, zipPath)
				if os.path.isfile(zipPath+".zip"):
					logging.info("Making MD5 checksum")
					makeMd5Sum(zipPath, zipName)
					
			raw_input("\nPress Enter to Return to the Main Menu...")
		cls()
