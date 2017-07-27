import os, xbmc, xbmcaddon

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'KODIUKTV Community Portal / Wizard / Maintenance'
EXCLUDES       = [ADDON_ID, 'repository.kodiuktv']
# Text File with build info in it.
BUILDFILE      = 'http://builds.kodiuk.tv/development/communityhub/lists/officialbuilds.txt'
# How often you would list it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.
APKFILE        = 'http://builds.kodiuk.tv/development/communityhub/lists/apks.txt'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = 'YouTube Videos'
YOUTUBEFILE    = 'http://builds.kodiuk.tv/development/communityhub/lists/youtube.txt'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'http://builds.kodiuk.tv/development/communityhub/lists/addons.txt'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'http://builds.kodiuk.tv/development/communityhub/lists/tweaklists/autoxml.txt'

# Dont need to edit just here for icons stored locally
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')

#########################################################
### THEMING MENU ITEMS ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = ''
# Leave as http:// for default icon
ICONBUILDS     = 'http://builds.kodiuk.tv/development/communityhub/icons/officialbuilds.png'
ICONMAINT      = 'http://builds.kodiuk.tv/development/communityhub/icons/maintenance.png'
ICONAPK        = 'http://builds.kodiuk.tv/development/communityhub/icons/apkinstaller.png'
ICONADDONS     = 'http://builds.kodiuk.tv/development/communityhub/icons/addoninstaller.png'
ICONYOUTUBE    = 'http://builds.kodiuk.tv/development/communityhub/icons/youtube.png'
ICONSAVE       = 'http://builds.kodiuk.tv/development/communityhub/icons/savedata.png'
ICONTRAKT      = 'http://builds.kodiuk.tv/development/communityhub/icons/trakt.png'
ICONREAL       = 'http://builds.kodiuk.tv/development/communityhub/icons/realdebrid.png'
ICONLOGIN      = 'http://builds.kodiuk.tv/development/communityhub/icons/icon.png'
ICONCONTACT    = 'http://builds.kodiuk.tv/development/communityhub/icons/contactus.png'
ICONSETTINGS   = 'http://builds.kodiuk.tv/development/communityhub/icons/settings.png'
# Hide the ====== seperators 'Yes' or 'No'
HIDESPACERS    = 'No'
# Character used in seperator
SPACER         = '-'

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'dodgerblue'
COLOR2         = 'ghostwhite'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][B][I]([COLOR '+COLOR2+']KODIUKTV[/COLOR])[/B][/COLOR] [COLOR '+COLOR2+']%s[/COLOR][/I]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Current Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Current Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'KODIUK.TV is built for sharing & learning together so we can grow as a community. Get involved!\r\n\r\n Get in touch & Get support via one of our community outlets http://kodiuk.tv & http://community.kodiuk.tv. Want your build or addon in the portal? Were always happy to add new content! Just get in touch with us on FB or Twitter & Well get it done for you'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = 'http://builds.kodiuk.tv/development/xml/icon.png'
CONTACTFANART  = 'http://'
#########################################################

#########################################################
### AUTO UPDATE #########################################
########## FOR THOSE WITH NO REPO #######################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'No'
# Url to wizard version
WIZARDFILE     = ''
#########################################################

#########################################################
### AUTO INSTALL ########################################
########## REPO IF NOT INSTALLED ########################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'No'
# Addon ID for the repository
REPOID         = 'repository.kodiuktv'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.github.com/kodiuktv/kodiuktv/master/_repo/addons.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://raw.github.com/kodiuktv/kodiuktv/master/_repo/'
#########################################################

#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'http://builds.kodiuk.tv/development/communityhub/lists/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
HEADERMESSAGE  = 'KODIUK.TV Community Portal Notifications'
# url to image if using Image 424x180
HEADERIMAGE    = 'http://'
# Background for Notification Window
BACKGROUND     = ''
#########################################################