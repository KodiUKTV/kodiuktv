#----Massive Credit to Rob from HDTV for letting me use this-----------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui
import sys
import os
import plugintools
import time
import socket
from StringIO import StringIO
import gzip

AddonID = 'plugin.video.stealthstreams'
RunPath = xbmc.translatePath(os.path.join('special://home','addons',AddonID,'resources/'));
REMOTE_VERSION_FILE = 'Imh0dHBzOi8vYXJjaGl2ZS5vcmcvZG93bmxvYWQvU3RlYWx0aF8yMDE1MTIvdmVyc2lvbi50eHQi'.decode('base64')
LOCAL_VERSION_FILE = os.path.join(RunPath , "version.txt")  
def read(url):
    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    return data
def message_yes_no(text1, text2="", text3=""):
    if text3=="":
        yes_pressed = xbmcgui.Dialog().yesno( text1 , text2 )
    elif text2=="":
        yes_pressed = xbmcgui.Dialog().yesno( "" , text1 )
    else:
        yes_pressed = xbmcgui.Dialog().yesno( text1 , text2 , text3 )
    return yes_pressed
def get_data_path():
    dev = xbmc.translatePath( __settings__.getAddonInfo('Profile') )
    if not os.path.exists(dev):
        os.makedirs(dev)
    return dev

def check_for_updates():
    try:
        data = read( REMOTE_VERSION_FILE )
        versiondescargada = data.splitlines()[0]
        urldescarga = data.splitlines()[1]
        infile = open( LOCAL_VERSION_FILE )
        data = infile.read()
        infile.close();
        versionlocal = data.splitlines()[0]

        if int(versiondescargada)>int(versionlocal): 
            yes_pressed = message_yes_no("Stealh Streams","New Version Found!","Do you want to Update now?")
            if yes_pressed:
                try:
                    local_file_name = os.path.join( plugintools.get_data_path() , "update.zip" )
                    urllib.urlretrieve(urldescarga, local_file_name )
                    import ziptools
                    unzipper = ziptools.ziptools()
                    destpathname = xbmc.translatePath( "special://home/addons")
                    unzipper.extract( local_file_name , destpathname )
                    os.remove(local_file_name)
                    xbmc.executebuiltin("UpdateLocalAddons")
                    xbmc.executebuiltin("UpdateAddonRepos")
                    xbmc.executebuiltin((u'XBMC.Notification("Update Done!", "Stealth Streams has been updated", 2000)'))
                    xbmc.executebuiltin( "Container.Refresh" )
                except:
                    xbmc.executebuiltin((u'XBMC.Notification("Not updated", "Error the update has failed", 2000)'))
    except:
        import traceback	

