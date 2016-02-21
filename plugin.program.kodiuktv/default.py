import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re, glob
import time
import downloader
import zipfile
import extract
import GoDev
import zipfile
import ntpath

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://archive.org'
ADDON=xbmcaddon.Addon(id='plugin.program.kodiuktv')
AddonID = 'plugin.program.kodiuktv'
MainPath=xbmc.translatePath(os.path.join('special://home','addons',AddonID));
Images=xbmc.translatePath(os.path.join('special://home','addons',AddonID,'resources','images/')); 
FanArt = xbmc.translatePath(os.path.join(MainPath,'FanArt.png'));
HOME =  xbmc.translatePath('special://home/')
ADDONS =  xbmc.translatePath(os.path.join('special://home','addons',''))
Dialog =  xbmcgui.Dialog()
DialogProcess =  xbmcgui.DialogProgress()
USERDATA =  xbmc.translatePath(os.path.join('special://home/userdata',''))
GUISETTINGS =  os.path.join(USERDATA,'guisettings.xml')
THUMBNAILS =  xbmc.translatePath(os.path.join(USERDATA,'Thumbnails'))
zip =  ADDON.getSetting('zip')
USB =  xbmc.translatePath(os.path.join(zip))
skin =  xbmc.getSkinDir()
VERSION = "1.3"
PATH = "kodiuktv"

def MainMenu():
	Maintenance  =  ADDON.getSetting('Maintenance')
	KodiUKBuildMenu  =  ADDON.getSetting('KodiUKBuildMenu')
	Extras  =  ADDON.getSetting('Extras')
	CommunityBuildMenu  =  ADDON.getSetting('CommunityBuildMenu')	
	if KodiUKBuildMenu == 'true':
		addFolder('folder','Kodi UK TV Builds','none', 'KodiUKBuildMenu', 'kodiukbuilds.png','','','')
	if CommunityBuildMenu == 'true':
		addFolder('folder','Community Builds','none', 'CommBuildMenu', 'community.png','','','')
	if Extras == 'true':
		addFolder('folder','Extras','none', 'ExtraMenu', 'extras.png','','','')
	if Maintenance == 'true':
		addFolder('folder','Maintenance and Tweaks','FanArt', 'Tools', 'maintenance.png','','','')	
	setView('movies', 'MAIN')
def KodiUKBuildMenu():
    link = OPEN_URL('http://builds.kodiuk.tv/development/xml/toolbox.xml').replace('\n','').replace('\r','')  #Spaf
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,FanArt,description in match:
        addXMLMenu(name,url,1,iconimage,FanArt,description)
    setView('movies', 'MAIN')
def CommBuildMenu():
    link = OPEN_URL('http://builds.kodiuk.tv/development/xml/toolboxcommunity.xml').replace('\n','').replace('\r','')  #Spaf
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,FanArt,description in match:
        addXMLMenu(name,url,1,iconimage,FanArt,description)
    setView('movies', 'MAIN')	
def Wipe_Kodi():
    mybackuppath = xbmc.translatePath(os.path.join(USB,'Community Builds','My Builds'))
    choice = xbmcgui.Dialog().yesno("Are you sure!!!", 'This will revert back to a blank Kodi?', '', 'Dont blame me if it goes wrong!', yeslabel='Yes',nolabel='No')
    if choice == 1:
        if skin!= "skin.confluence":
            Dialog.ok('Kodi UK','Please Change to the default Confluence skin','before performing a wipe.','')
            xbmc.executebuiltin("ActivateWindow(appearancesettings)")
            return
        else:
            choice = xbmcgui.Dialog().yesno("Kodi UK", 'This will completely wipe your install.', 'Are you sure?', '', yeslabel='Yes', nolabel='No')
            if choice == 0:
                if not os.path.exists(mybackuppath):
                    os.makedirs(mybackuppath)
                vq = 'backup.zip'
                if ( not vq ): return False, 0
                title = urllib.quote_plus(vq)
                backup_zip = xbmc.translatePath(os.path.join(mybackuppath,title+'.zip'))
                exclude_dirs_full =  ['plugin.program.kodiuktv']
                exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
                message_header = "Creating full backup of existing build"
                message1 = "Archiving..."
                message2 = ""
                message3 = "Please Wait"
                GoDev.Archive_Tree(HOME, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
            choice = xbmcgui.Dialog().yesno("Remove KodiUK Wizard?", 'Do you also want to remove the Kodi UK Wizard', 'add-on and have a complete fresh start or would you', 'prefer to keep this on your system?', yeslabel='Remove',nolabel='Keep')
            if choice == 0:
                GoDev.Remove_Textures()
                trpath = xbmc.translatePath(os.path.join(ADDONS,AddonID,''))
                trtemp = xbmc.translatePath(os.path.join(HOME,'..','kodiukwizard.zip'))
                GoDev.Archive_File(trpath, trtemp)
                deppath = xbmc.translatePath(os.path.join(ADDONS,'script.module.addon.common',''))
                deptemp = xbmc.translatePath(os.path.join(HOME,'..','kodiukwizarddep.zip'))
                GoDev.Archive_File(deppath, deptemp)
                GoDev.Destroy_Path(HOME)
                if not os.path.exists(trpath):
                    os.makedirs(trpath)
                if not os.path.exists(deppath):
                    os.makedirs(deppath)
                time.sleep(1)
                GoDev.Read_Zip(trtemp)
                DialogProcess.create("Kodi UK","Checking ",'', 'Please Wait')
                DialogProcess.update(0,"", "Extracting Zip Please Wait")
                extract.all(trtemp,trpath,dialogprocess)
                GoDev.Read_Zip(deptemp)
                extract.all(deptemp,deppath,dialogprocess)
                DialogProcess.update(0,"", "Extracting Zip Please Wait")
                DialogProcess.close()
                time.sleep(1)
            elif choice == 1:
                GoDev.Remove_Textures()
                GoDev.Destroy_Path(HOME)
                DialogProcess.close()
            else: return
def GeneralMaint():
    addFolder('','Clear Cache', 'none', 'Clear_Cache', 'clearcache.png','','','')
    addFolder('','Clear Addon Data','none','Remove_Addon_Data','addondata.png','','','')
    addFolder('','Clear Crash Logs', 'none', 'Remove_Crash_Logs', 'crashlogs.png','','','')
    addFolder('','Clear Textures','none','Remove_Textures','cleartextures.png','','','')
    addFolder('','Clear Thumbnails','none','Remove_Thumbs','thumbnails.png','','','')
    addFolder('','Clear Packages','none','Remove_Packages','packages.png','','','')
    setView('movies', 'MAIN')	
def Tools():
    addFolder('folder','General Maintenance & Fixes', 'none', 'GeneralMaint', 'Generalmaintenance.png','','','')
    addFolder('folder','Backup/Restore','none','BackupMenu','backuprestore.png','','','')
    addFolder('','Fresh Start', 'none', 'Wipe_Kodi', 'freshstart.png','','','')
    addFolder('','Convert Link To Special',HOME,'make_special','links.png','','','')
    setView('movies', 'MAIN')	
def Clear_Cache():
    choice = xbmcgui.Dialog().yesno('Are you Sure?', 'This will delete all your Cache', 'It can help with Buffering issue','and can clear alot of space', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Wipe_Cache()
def Remove_Addon_Data():
    choice = xbmcgui.Dialog().yesno('Delete Addon_Data Folder?', 'This will free up space by deleting your addon_data', 'folder. This contains all addon related settings', 'including username and password info.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Delete_Userdata()
        Dialog.ok("Addon_Data Removed", '', 'Your addon_data folder has now been removed.','')
def Remove_Crash_Logs():
    choice = xbmcgui.Dialog().yesno('Remove All Crash Logs?', 'There is absolutely no harm in doing this, these are', 'log files generated when Kodi crashes and are','only used for debugging purposes.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Delete_Logs()
        Dialog.ok("Crash Logs Removed", '', 'Your crash log files have now been removed.','')
def Remove_Packages():
    choice = xbmcgui.Dialog().yesno('Delete Packages Folder?', 'This will free up space by deleting the zip install', 'files of your addons. The only downside is you\'ll no', 'longer be able to rollback to older versions.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Delete_Packages()
        Dialog.ok("Packages Removed", '', 'Your zip install files have now been removed.','')
def Remove_Textures():
    choice = xbmcgui.Dialog().yesno('Clear Cached Images?', 'This will clear your textures13.db file.', 'These will automatically be', 'repopulated after a restart.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Remove_Textures()
def Remove_Thumbs():
    choice = xbmcgui.Dialog().yesno('Clear Cached Images?', 'This will clear your thumbnail files.', 'These will automatically be', 'repopulated after a restart.', nolabel='Cancel',yeslabel='Delete')
    if choice == 1:
        GoDev.Destroy_Path(THUMBNAILS)	
def BackupMenu():
    addFolder('folder','Backup','none','backup_option','Backup.png','','','')
    addFolder('folder','Restore','none','restore_option','Restore.png','','','')	
    setView('movies', 'MAIN')
def Backup_Option():
    addFolder('','Full Backup','url','backupzip','Backup.png','','','')
    setView('movies', 'MAIN')
def Restore_Option():
    addFolder('','Full restore','url','RestoreIt','restore.png','','','')
    setView('movies', 'MAIN')
def ComingSoon():
    Dialog.ok('Kodi UK Wizard','Coming Soon!')			
def ExtraMenu():
    link = OPEN_URL('http://builds.kodiuk.tv/development/xml/toolboxextras.xml').replace('\n','').replace('\r','')  #Spaf
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,FanArt,description in match:
        addXMLMenu(name,url,2,iconimage,FanArt,description)
    setView('movies', 'MAIN')	
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR dodgerblue]Community[/COLOR] [COLOR lime]Toolbox[/COLOR]","Downloading ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    Dialog = xbmcgui.Dialog()
    Dialog.ok("DOWNLOAD COMPLETE", 'Unfortunately the only way to get the new changes to stick is', 'to force close kodi. Click ok to force Kodi to close,', 'DO NOT use the quit/exit options in Kodi.')
def wizard2(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("[COLOR dodgerblue]Community[/COLOR] [COLOR lime]Toolbox[/COLOR]","Downloading ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    Dialog = xbmcgui.Dialog()
    Dialog.ok("Stealth Streams", 'Installed iVue Link', '', '')
def addXMLMenu(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def addFolder(type,name,url,mode,iconimage = '',FanArt = '',video = '',description = ''):
    if type != 'folder2' and type != 'addon':
        if len(iconimage) > 0:
            iconimage = Images + iconimage
        else:
            iconimage = 'DefaultFolder.png'
    if type == 'addon':
        if len(iconimage) > 0:
            iconimage = iconimage
        else:
            iconimage = 'none'
    if FanArt == '':
        FanArt = FanArt
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&FanArt="+urllib.quote_plus(FanArt)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
    liz.setProperty( "FanArt_Image", FanArt )
    liz.setProperty( "Build.Video", video )
    if (type=='folder') or (type=='folder2') or (type=='tutorial_folder') or (type=='news_folder'):
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    else:
        ok=Add_Directory_Item(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok
def Add_Directory_Item(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder) 
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param


params=get_params()
url=None
name=None
mode=None
iconimage=None
FanArt=None
description=None
addon_id=None
audioaddons=None
author=None
buildname=None
data_path=None
description=None
DOB=None
email=None
fanart=None
forum=None
iconimage=None
link=None
local=None
messages=None
mode=None
name=None
posts=None
programaddons=None
provider_name=None
repo_id=None
repo_link=None
skins=None
sources=None
updated=None
unread=None
version=None
video=None
videoaddons=None
welcometext=None
zip_link=None

try:    addon_id=urllib.unquote_plus(params["addon_id"])
except: pass
try:    audioaddons=urllib.unquote_plus(params["audioaddons"])
except: pass
try:    author=urllib.unquote_plus(params["author"])
except: pass
try:    buildname=urllib.unquote_plus(params["buildname"])
except: pass
try:    data_path=urllib.unquote_plus(params["data_path"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass
try:    DOB=urllib.unquote_plus(params["DOB"])
except: pass
try:    email=urllib.unquote_plus(params["email"])
except: pass
try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
try:    forum=urllib.unquote_plus(params["forum"])
except: pass
try:    guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    link=urllib.unquote_plus(params["link"])
except: pass
try:    local=urllib.unquote_plus(params["local"])
except: pass
try:    messages=urllib.unquote_plus(params["messages"])
except: pass
try:    mode=str(params["mode"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except: pass
try:    posts=urllib.unquote_plus(params["posts"])
except: pass
try:    programaddons=urllib.unquote_plus(params["programaddons"])
except: pass
try:    provider_name=urllib.unquote_plus(params["provider_name"])
except: pass
try:    repo_link=urllib.unquote_plus(params["repo_link"])
except: pass
try:    repo_id=urllib.unquote_plus(params["repo_id"])
except: pass
try:    skins=urllib.unquote_plus(params["skins"])
except: pass
try:    sources=urllib.unquote_plus(params["sources"])
except: pass
try:    updated=urllib.unquote_plus(params["updated"])
except: pass
try:    unread=urllib.unquote_plus(params["unread"])
except: pass
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    version=urllib.unquote_plus(params["version"])
except: pass
try:    video=urllib.unquote_plus(params["video"])
except: pass
try:    videoaddons=urllib.unquote_plus(params["videoaddons"])
except: pass
try:    zip_link=urllib.unquote_plus(params["zip_link"])
except: pass
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    mode=int(params["mode"])
except: pass
try:    FanArt=urllib.unquote_plus(params["FanArt"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass


print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )


if mode==None or url==None or len(url)<1:
        MainMenu()
elif mode == 'KodiUKBuildMenu' : KodiUKBuildMenu() #KodiBuildMenu
elif mode == 'CommBuildMenu' : CommBuildMenu() #CommBuildMenu
elif mode == 'Tools' : Tools() #ToolsMenu
elif mode == 'ExtraMenu': ExtraMenu() #ExtraMenu
elif mode == 'BackupMenu' : BackupMenu() #BackupMenu
elif mode == 'backup_option': Backup_Option() #BackupMenu
elif mode == 'restore_option': Restore_Option()#RestoreMenu
elif mode == 'GeneralMaint' : GeneralMaint() #GeneralMaint
elif mode == 'Clear_Cache' : Clear_Cache() #Clear_Cache
elif mode == 'Remove_Addon_Data' : Remove_Addon_Data() #Remove_Addon_Data
elif mode == 'Remove_Crash_Logs' : Remove_Crash_Logs() #Remove_Crash_Logs
elif mode == 'Remove_Textures' : Remove_Textures() #Remove_Textures
elif mode == 'Remove_Thumbs' : Remove_Thumbs() #Remove_Thumbs
elif mode == 'Remove_Packages' : Remove_Packages() #Remove_Packages
elif mode == 'Wipe_Kodi' : Wipe_Kodi() #Wipe_Kodi
elif mode == 'make_special' : GoDev.Fix_Special(url)#make Special
elif mode == 'backupzip': GoDev.Backupzip() #Backitup
elif mode == 'RestoreIt': GoDev.RestoreIt() #RestoreBuild
elif mode == 'ComingSoon': ComingSoon() #ComingSoon
elif mode==1: wizard(name,url,description) #OpenWizard
elif mode==2: wizard2(name,url,description) #OpenWizard
xbmcplugin.endOfDirectory(int(sys.argv[1]))
