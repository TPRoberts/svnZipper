# svnZipper
SVN Zipper for LeeDrOiD.co.uk

# Build Process
'''
sudo apt-get upgrade
sudo apt-get install git python python-pip python-svn
sudo pip install pyinstaller colorama
git clone https://github.com/TPRoberts/svnZipper.git
cd svnZipper
'''

__For LeeDroid linuxSvnZipper__
'''
./build.sh
'''
__For ICE linuxSvnZipper__
'''
./buildIce.sh
'''

The build executable will be in the following path:
'''
dist/svnZipper
'''
You can move it and rename it to whatever you like. I would suggest to move to a place with enough space as the checkouts happen in the location of the executable.

Change the permissions first, just to be sure.
'''
chmod +x svnZipper
./svnZipper
'''
