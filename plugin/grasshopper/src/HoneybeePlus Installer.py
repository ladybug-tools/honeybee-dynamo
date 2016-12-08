# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# This file is part of Honeybee.
#
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
This component downloads honeybee libraries from github to:
C:\Users\%USERNAME%\AppData\Roaming\McNeel\Rhinoceros\5.0\scripts

-

    Args:
        _install!: Set to True to install honeybee[+] (and ladybug) on your machine.
        update_: Optional boolean to update honeybee even if you have it already installed.
    Returns:
        Vviiiiiiiiiizzz!: !!!
"""

ghenv.Component.Name = "HoneybeePlus Installer"
ghenv.Component.NickName = "HBInstaller"
ghenv.Component.Message = 'VER 0.0.01\nDEC_07_2016'
ghenv.Component.Category = "HoneybeePlus"
ghenv.Component.SubCategory = "05 :: Developers"
ghenv.Component.AdditionalHelpFromDocStrings = "1"

import os
import System
import sys
import zipfile
import shutil
from Grasshopper.Folders import UserObjectFolders


def installButterfly(update):
    
    """
    This code will download butterfly library from github to:
        C:\Users\%USERNAME%\AppData\Roaming\McNeel\Rhinoceros\5.0\scripts\butterfly
    """
    folders = ('ladybug', 'honeybee', 'honeybee_grasshopper')
    repos = ('ladybug', 'honeybee', 'honeybee-plus')
    
    targetDirectory = [p for p in sys.path if p.find('scripts')!= -1][0]
    try:
        targetDirectory = [p for p in sys.path if p.find('scripts')!= -1][0]
    except IndexError:
        # there is no scripts in path try to find plugins folder
        try:
            targetDirectory = [p for p in sys.path if p.find(r'settings\lib')!= -1][0]
        except IndexError:
            raise IOError('Failed to find a shared path in sys.path to install butterfly.\n' \
                          'Make sure Grasshopper is installed correctly!')
    
    # delete folders 
    if update:
        for f in folders:
            libFolder = os.path.join(targetDirectory, f)
            if os.path.isdir(libFolder):
                try:
                    shutil.rmtree(libFolder)
                except:
                    print 'Failed to remove {}.'.format(libFolder)
    else:
        for c, f in enumerate(folders):
            if not os.path.isdir(os.path.join(targetDirectory, f)):
                break  # at least one of the folders is not installed
            else:
                print 'Found {}'.format(os.path.join(targetDirectory, f))
        
        if c == 2:
            # all the folders are installed
            print 'All the folders are already installed.' \
                'Set update to True if you want them to be updated.'
            return

    for repo in repos:
        url = "https://github.com/ladybug-analysis-tools/%s/archive/master.zip" % repo
        # download the zip file
        print "Downloading {} the github repository to {}".format(repo, targetDirectory)
        zipFile = os.path.join(targetDirectory, '%s.zip' % repo)
        
        try:
            client = System.Net.WebClient()
            client.DownloadFile(url, zipFile)
        except Exception, e:
            msg = `e` + "\nDownload failed! Try to download and unzip the file manually form:\n" + url
            raise Exception(msg)
        
        #unzip the file
        with zipfile.ZipFile(zipFile) as zf:
            for f in zf.namelist():
                if f.endswith('/'):
                    try: os.makedirs(f)
                    except: pass
                else:
                    zf.extract(f, targetDirectory)
        zf.close()
        try:
            os.remove(zipFile)
        except:
            pass       
    
    # copy files to folder.
    for f, r in zip(folders, repos):
        bfFolder = os.path.join(targetDirectory, r"{}-master".format(r), f)
        libFolder = os.path.join(targetDirectory, f)
        print 'Copying {} source code to {}'.format(f, libFolder)
        try:
            shutil.copytree(bfFolder, libFolder)
        except:
            pass
    
    # copy user-objects
    uofolder = UserObjectFolders[0]
    bfUserObjectsFolder = os.path.join(targetDirectory, r"honeybee-plus-master\plugin\grasshopper\userObjects")
    print 'Copying honeybee[+] userobjects to {}.'.format(uofolder)
    
    # remove all the HoneybeePlus userobjects
    for f in os.listdir(uofolder):
        if f.startswith("HoneybeePlus"):
            os.remove(os.path.join(uofolder, f))
            
    for f in os.listdir(bfUserObjectsFolder):
        shutil.copyfile(os.path.join(bfUserObjectsFolder, f),
                        os.path.join(uofolder, f))

    # try to clean up
    for r in repos:
        try:
            shutil.rmtree(os.path.join(targetDirectory, '{}-master'.format(r)))
        except:
            pass

if _install:
    installButterfly(update_)


def importlibs():
    import ladybug
    import honeybee
    import honeybee_grasshopper
    print "Imported honeybee[+] from {}\nVviiiizzzz...".format(honeybee_grasshopper.__file__)

try:
    importlibs()
except ImportError as e:
    if str(e) == 'No module named ladybug':
        installButterfly(update_)
        try:
            importlibs()
        except:
            raise Exception("Failed to import honeybee[+]:\n{}".format(e))
    else:
        raise Exception("Failed to import honeybee[+]:\n{}".format(e))

# push this component to back
ghenv.Component.OnPingDocument().SelectAll()
ghenv.Component.Attributes.Selected = False
ghenv.Component.OnPingDocument().BringSelectionToTop()
ghenv.Component.OnPingDocument().DeselectAll()