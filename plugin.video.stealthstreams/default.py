import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,datetime,os,xbmc,json
import GoDev, common	
from datetime import datetime, timedelta
import base64

ADDON = xbmcaddon.Addon(id='plugin.video.stealthstreams')
AddonID = 'plugin.video.stealthstreams'

Username=xbmcplugin.getSetting(int(sys.argv[1]), 'Username')
Password=xbmcplugin.getSetting(int(sys.argv[1]), 'Password')
M3UActive=xbmcplugin.getSetting(int(sys.argv[1]), 'M3UActive')
M3ULink=xbmcplugin.getSetting(int(sys.argv[1]), 'M3ULink')
CFU=xbmcplugin.getSetting(int(sys.argv[1]), 'CFU')

from time import strftime
from datetime import datetime
Addon = xbmcaddon.Addon(AddonID)

ListName='SportsReplays'
type ='bTN1OA=='.decode('base64')
site = 'aHR0cDovL3BsYXluaWNldHYudGs='.decode('base64')
port = 'MjA1Mg=='.decode('base64')
Images=xbmc.translatePath(os.path.join('special://home','addons',AddonID,'resources/'));
SportsM3uLinks = 'b3MucGF0aC5qb2luKEltYWdlcywgJ0lrMHpkWE11ZEhoMElnPT0nLmRlY29kZSgnYmFzZTY0Jykp'.decode('base64')

def OpenM3uURL(url, headers={}, user_data={}, justCookie=False):
	if user_data:
		user_data = urllib.urlencode(user_data)
		req = urllib2.Request(url, user_data)
	else:
		req = urllib2.Request(url)
	
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
	for k, v in headers.items():
		req.add_header(k, v)
	
	response = urllib2.urlopen(req)
	
	if justCookie == True:
		if response.info().has_key("Set-Cookie"):
			data = response.info()['Set-Cookie']
		else:
			data = None
	else:
		data = response.read().replace("\r", "")
	
	response.close()
	return data
def MainMenu():
    AddDir('My Account','%s:%s/panel_api.php?username=%s&password=%s'%(site,port,Username,Password),3,Images + 'MyAcc.png')
    AddDir('Live TV','%s:%s/get.php?username=%s&password=%s&type=m3u_plus&output=hls'%(site,port,Username,Password),5,Images + 'Live TV.png')
    addDir2('Settings','settings',8,'')
    if CFU == "true":
        GoDev.check_for_updates()#self.openSettings(addonId)
def Open_URL(url):
        req = urllib2.Request(url)
        #req.add_header('User-Agent' , "Magic Browser")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
def LiveTV(url):
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        vidlocation=('%s:%s/live/%s/%s/'%(site,port,Username,Password))
        link = Open_URL(url)
        match=re.compile('{"name":"(.+?)","stream_id":"(.+?)".+?"live":"1".+?icon":"(.+?)"').findall(link)
        for name,url,iconimage in match:
                AddPlayable('%s'%(name),'%s/%s.ts'%(vidlocation,url,),'%s'%(iconimage).replace("\/","/"),'')
def OnDemand(url):
        xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
        vidlocation=('%s:%s/movie/%s/%s/'%(site,port,Username,Password))
        link = Open_URL(url)
        match=re.compile('{"name":"(.+?)","stream_id":"(.+?)".+?container_extension":"(.+?)","stream_icon":"(.+?)",".+?"').findall(link)#match=re.compile('{"name":"(.+?)","stream_id":"(.+?)".+?"live":"0".+?icon":"(.+?)"').findall(link)
        for name,streamid,container,iconimage in match:
                AddPlayable('%s'%(name),'%s/%s.%s'%(vidlocation,streamid,container),'%s'%(iconimage).replace("\/","/"),'')               					
def MyAccDetails(url):
        link = Open_URL(url)
        match=re.compile('"username":"(.+?)"').findall(link)
        match1=re.compile('"status":"(.+?)"').findall(link)
        match2=re.compile('"exp_date":"(.+?)"').findall(link) 	
        match3=re.compile('"active_cons":"(.+?)"').findall(link)
        match4=re.compile('"created_at":"(.+?)"').findall(link)
        match5=re.compile('"max_connections":"(.+?)"').findall(link)
        match6=re.compile('"is_trial":"1"').findall(link)
        for url in match:
                AddAccInfo('My Stealth Streams Account Information','','',Images +'MyAcc.png')
                AddAccInfo('Username:  %s'%(url),'','',Images + 'MyAcc.png')
        for url in match1:
                AddAccInfo('Status:  %s'%(url),'','',Images + 'MyAcc.png')
        for url in match4:
                dt = datetime.fromtimestamp(float(match4[0]))
                dt.strftime('%Y-%m-%d %H:%M:%S')
                AddAccInfo('Created:  %s'%(dt),'','',Images +'MyAcc.png')
        for url in match2:
                dt = datetime.fromtimestamp(float(match2[0]))
                dt.strftime('%Y-%m-%d %H:%M:%S')
                AddAccInfo('Expires:  %s'%(dt),'','',Images +'MyAcc.png')
        for url in match3:
                AddAccInfo('Active Connection:  %s'%(url),'','',Images +'MyAcc.png')
        for url in match5:
                AddAccInfo('Max Connection:  %s'%(url),'','',Images +'MyAcc.png') 
        for url in match6:
                AddAccInfo('Trial: Yes','','',Images +'MyAcc.png')
        AddAccInfo('','','','')  
        AddAccInfo('','','','') 
        AddAccInfo('Sign up here - www.kodiuk.tv','','','') 		
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
                                param[splitparams[0].lower()] = splitparams[1]#param[splitparams[0]]=splitparams[1]
                                
        return param
def AddPlayable(name,url,iconimage,urlType):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        menu=[]
        liz.setProperty('IsPlayable','true')
        liz.addContextMenuItems(items=menu, replaceItems=False)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok	  
def AddDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def AddAccInfo(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def AddM3U(name, url, mode, iconimage, description="", isFolder=True, background=None):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
    liz.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)	
def RefreshList(url):	
	listName = ("SportsReplays".encode('utf-8')).strip()
	listUrl = (M3ULink.encode('utf-8')).strip()
	list = common.ReadList(SportsM3uLinks)	
	for item in list:
		if item["url"].lower() == listUrl.lower():
			return
	list.append({"name": listName.decode("utf-8"), "url": listUrl})
	if common.SaveList(SportsM3uLinks, list):
		xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))	
def PlayM3U(name, url, iconimage=None):
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	listitem.setProperty('IsPlayable','true')
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
def SportsReplays(url):	
    list = common.m3u2list(url)
    for channel in list:
        name = common.GetEncodeString(channel["display_name"])
        _NAME_=name
        if _NAME_ in name:
            AddM3U(name ,channel["url"], 7, "", isFolder=False)
def openSettings():
    ADDON.openSettings()	
def addDir2(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok	
params=get_params()
url=None
name=None
iconimage=None
mode=None
description=None


try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    mode=int(params["mode"])
except: pass
try:    description = urllib.unquote_plus(params["description"])
except:	pass
try:	iconimage = urllib.unquote_plus(params["iconimage"])
except:	pass

if mode==None or url==None or len(url)<1:
    MainMenu()
    #RefreshList(M3ULink)	
elif mode==2:
    LiveTV(url)
elif mode==5:
    SportsReplays(url)
elif mode==6:
    OnDemand(url)
elif mode==3:
    MyAccDetails(url) 
elif mode==7:
	PlayM3U(name, url, iconimage)
elif mode==8:
	openSettings()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
