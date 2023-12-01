#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------#
#   coded by Lululla  #
#      24/11/2023     #
# --------------------#
from . import _
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.LoadPixmap import LoadPixmap
from enigma import eListboxPythonMultiContent, gFont
from enigma import eTimer, RT_HALIGN_LEFT, RT_VALIGN_CENTER
import os
from .lib.GetEcmInfo import GetEcmInfo
plugin_path = '/usr/lib/enigma2/python/Plugins/Extensions/nssaddon/'
cccaminfo = False
ECM_INFO = '/tmp/ecm.info'


def main(session, **kwargs):
    session.open(NSSCamsManager)


def DreamCCExtra(name, index, isActive=False):
    res = [index]
    res.append((eListboxPythonMultiContent.TYPE_TEXT,
                90,
                6,
                200,
                30,
                0,
                RT_HALIGN_LEFT | RT_VALIGN_CENTER,
                name))
    if isActive:
        png = LoadPixmap(plugin_path + 'res/pics/on.png')
    else:
        png = LoadPixmap(plugin_path + 'res/pics/off.png')
    res.append((eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST,
                5,
                3,
                70,
                40,
                png))
    return res


class DCCMenu(MenuList):

    def __init__(self, list, selection=0, enableWrapAround=True):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 30))
        self.l.setItemHeight(50)
        self.selection = selection

    def postWidgetCreate(self, instance):
        MenuList.postWidgetCreate(self, instance)
        self.moveToIndex(self.selection)


class NSSCamsManager(Screen):
    skin = '''
        <screen name="NSSCamsManager" position="320,180" size="1280,720" title="" flags="wfNoBorder" backgroundColor="#101010">
            <widget name="list" position="40,155" size="675,370" scrollbarMode="showOnDemand" transparent="1" zPosition="2" />
            <widget name="info" position="42,550" size="1210,68" font="Regular; 18" halign="left" foregroundColor="yellow" backgroundColor="#20000000" transparent="1" zPosition="7" />
            <widget name="ecm" position="740,155" size="507,370" font="Regular; 22" halign="left" foregroundColor="yellow" backgroundColor="#20000000" transparent="1" zPosition="5" />
            <ePixmap name="red" position="45,670" zPosition="2" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/nssaddon/res/buttons/key_red.png" transparent="1" alphatest="on" />
            <ePixmap name="green" position="260,670" zPosition="2" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/nssaddon/res/buttons/key_green.png" transparent="1" alphatest="on" />
            <ePixmap name="blue" position="790,670" zPosition="2" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/nssaddon/res/buttons/key_blue.png" transparent="1" alphatest="on" />
            <ePixmap name="yellow" position="531,670" zPosition="2" size="34,47" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/nssaddon/res/buttons/key_yellow.png" transparent="1" alphatest="on" />
            <widget name="key_red" position="85,670" size="209,40" valign="center" halign="left" zPosition="4" foregroundColor="white" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
            <widget name="key_green" position="300,670" size="209,40" valign="center" halign="left" zPosition="4" foregroundColor="white" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
            <widget name="key_yellow" position="571,670" size="209,40" valign="center" halign="left" zPosition="4" foregroundColor="white" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
            <widget name="key_blue" position="831,670" size="209,40" valign="center" halign="left" zPosition="4" foregroundColor="white" font="Regular;30" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/nssaddon/res/icons/logo.png" position="303,54" size="711,76" alphatest="on" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/nssaddon/res/pics/backg.png" scale="stretch" position="0,0" size="1280,720" alphatest="on" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/nssaddon/res/pics/logo.png" position="42,67" size="150,50" alphatest="on" zPosition="5" />
        </screen>'''

    def __init__(self, session, args=0):
        self.session = session
        Screen.__init__(self, session)
        self.skin = NSSCamsManager.skin
        self.index = 0
        self.sclist = []
        self.namelist = []
        self.softcamlist = []
        self.lastCam = ''
        try:
            self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        except:
            self.oldService = self.session.nav.getCurrentlyPlayingServiceOrGroup()
        self['actions'] = ActionMap(['OkCancelActions',
                                     'MenuActions',
                                     'ColorActions'], {'ok': self.action,
                                                       'cancel': self.close,
                                                       'menu': self.confignss,
                                                       'green': self.action,
                                                       'yellow': self.stardown,
                                                       'blue': self.messagekd,
                                                       'red': self.stop,
                                                       })
        self.CCcam = False
        self['key_red'] = Button(_('Stop'))
        self['key_green'] = Button(_('Start/Restart'))
        self['key_yellow'] = Button(_('Download'))
        self['key_blue'] = Button(_('Softcam'))
        os.system('ln -sf /usr/keys /var/keys')
        self.lastCam = self.readCurrent()
        self['info'] = Label()
        self['ecm'] = Label('')
        # self['pixmap'] = Pixmap()
        self['list'] = DCCMenu(self.softcamlist)
        self.readScripts()
        title = 'Nss Cams Manager'
        self.setTitle(title)
        self.EcmInfoPollTimer = eTimer()
        try:
            self.EcmInfoPollTimer_conn = self.EcmInfoPollTimer.timeout.connect(self.setEcmInfo)
        except:
            self.EcmInfoPollTimer.callback.append(self.setEcmInfo)
        self.EcmInfoPollTimer.start(200)
        self.onShown.append(self.ecm)
        self.onShown.append(self.openCCcamInfo)
        self.onHide.append(self.stopEcmInfoPollTimer)

    def confignss(self):
        from Plugins.Extensions.nssaddon.lib.datas import cccConfig
        self.session.open(cccConfig)

    def messagekd(self):
        self.session.openWithCallback(self.keysdownload, MessageBox, _('Update SoftcamKeys from google search?'), MessageBox.TYPE_YESNO)

    def keysdownload(self, result):
        if result:
            # script = ("sed -i -e 's/\r$//' %sauto" % plugin_path)
            script = (". %sauto.sh" % plugin_path)
            from os import access, X_OK
            if not access(script, X_OK):
                os.chmod(script, 493)
                # os.system("sed -i -e 's/\r$//' %sauto.sh" % plugin_path)
                # os.system("sed -i -e 's/^M$//' %sauto.sh" % plugin_path)
            os.system("os2unix %s" % script)
            self.session.open(Console, _('Update Softcam.key: %s') % script, ['%s' % script])

    def setEcmInfo(self):
        try:
            self.ecminfo = GetEcmInfo()
            newEcmFound, ecmInfo = self.ecminfo.getEcm()
            if newEcmFound:
                self['ecm'].setText(''.join(ecmInfo))
            else:
                self.ecm()
        except Exception as e:
            print(e)

    def ecm(self):
        try:
            ecmf = ''
            if os.path.exists(ECM_INFO):
                try:
                    with open(ECM_INFO) as f:
                        self["ecm"].text = f.read()
                except IOError:
                    pass
            else:
                self['ecm'].setText(ecmf)
        except Exception as e:
            print('error ecm: ', e)

    def stopEcmInfoPollTimer(self):
        self.EcmInfoPollTimer.stop()

    def refresh(self):
        self.index = 0
        self.sclist = []
        self.namelist = []
        try:
            self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        except:
            self.oldService = self.session.nav.getCurrentlyPlayingServiceOrGroup()
        self.softcamlist = []
        self['list'].setList(self.softcamlist)
        self.readScripts()
        self.lastCam = self.readCurrent()
        self.ecm()
        title = 'Nss Cams Manager'
        self.setTitle(title)
        self.openCCcamInfo()

    def showcccaminfo(self):
        try:
            if 'cccam' in self.lastCam.lower():
                self.session.openWithCallback(CCcamInfoMain)
        except:
            pass

    def openCCcamInfo(self):
        try:
            if 'cccam' in self.lastCam.lower():
                self.CCcam = True
            else:
                self.CCcam = False
        except:
            self.CCcam = False

    def openTest(self):
        pass

    def getLastIndex(self):
        a = 0
        if len(self.namelist) > 0:
            for x in self.namelist:
                if x == self.lastCam:
                    return a
                a += 1

        else:
            return -1
        return -1

    def action(self):
        self.session.nav.playService(None)
        last = self.getLastIndex()
        var = self['list'].getSelectionIndex()
        try:
            os.remove('/tmp/ecm.info')
        except:
            pass

        self['info'].setText('')
        if last > -1:
            if last == var:
                self.cmd1 = '/usr/script/cam/' + self.sclist[var] + ' cam_res &'
                os.system(self.cmd1)
                os.system('sleep 3')
            else:
                self.cmd1 = '/usr/script/cam/' + self.sclist[last] + ' cam_down &'
                os.system(self.cmd1)
                os.system('sleep 2')
                self.cmd1 = '/usr/script/cam/' + self.sclist[var] + ' cam_up &'
                os.system(self.cmd1)
        else:
            try:
                self.cmd1 = '/usr/script/cam/' + self.sclist[var] + ' cam_up &'
                os.system(self.cmd1)
                os.system('sleep 3')
            except:
                self.refresh
                return

        if last != var:
            try:
                self.lastCam = self['list'].l.getCurrentSelection()[1][7]
                self.writeFile()
            except:
                self.refresh
                return

        print(self.cmd1)
        self.readScripts()
        self.session.nav.playService(self.oldService)
        self.refresh
        return

    def writeFile(self):
        if self.lastCam is not None:
            clist = open('/etc/clist.list', 'w')
            clist.write(self.lastCam)
            clist.close()
        stcam = open('/etc/startcam.sh', 'w')
        stcam.write('#!/bin/sh\n' + self.cmd1)
        stcam.close()
        self.cmd2 = 'chmod 755 /etc/startcam.sh &'
        os.system(self.cmd2)
        return

    def stop(self):
        self.session.nav.playService(None)
        last = self.getLastIndex()
        if last > -1:
            self.cmd1 = '/usr/script/cam/' + self.sclist[last] + ' cam_down &'
            os.system(self.cmd1)
        else:
            return
        self.lastCam = 'no'
        self.writeFile()
        os.system('sleep 4')
        self.readScripts()
        self['info'].setText(' ')
        self.session.nav.playService(self.oldService)
        return

    def readScripts(self):
        self.index = 0
        scriptliste = []
        pliste = []
        path = '/usr/script/cam/'
        for root, dirs, files in os.walk(path):
            for name in files:
                scriptliste.append(name)

        self.sclist = scriptliste
        i = len(self.softcamlist)
        del self.softcamlist[0:i]
        for lines in scriptliste:
            dat = path + lines
            sfile = open(dat, 'r')
            for line in sfile:
                if line[0:3] == 'OSD':
                    nam = line[5:len(line) - 2]
                    if self.lastCam is not None:
                        if nam == self.lastCam:
                            self.softcamlist.append(DreamCCExtra(name=nam, index=self.index, isActive=True))
                        else:
                            self.softcamlist.append(DreamCCExtra(name=nam, index=self.index, isActive=False))
                        self.index += 1
                    else:
                        self.softcamlist.append(DreamCCExtra(name=nam, index=self.index, isActive=False))
                        self.index += 1
                    pliste.append(nam)

            sfile.close()
            self['list'].setList(self.softcamlist)
            self.namelist = pliste

        return

    def readCurrent(self):
        lastcam = ''
        try:
            clist = open('/etc/clist.list', 'r')
        except:
            return

        if clist is not None:
            for line in clist:
                lastcam = line

            clist.close()
        return lastcam

    def autocam(self):
        current = None
        try:
            clist = open('/etc/clist.list', 'r')
            print('found list')
        except:
            return

        if clist is not None:
            for line in clist:
                current = line

            clist.close()
        print('current =', current)
        if os.path.isfile('/etc/autocam.txt') is False:
            alist = open('/etc/autocam.txt', 'w')
            alist.close()
        self.cleanauto()
        alist = open('/etc/autocam.txt', 'a')
        alist.write(self.oldService.toString() + '\n')
        last = self.getLastIndex()
        alist.write(current + '\n')
        alist.close()
        self.session.openWithCallback(self.callback, MessageBox, _('Autocam assigned to the current channel'), type=1, timeout=10)
        return

    def cleanauto(self):
        delemu = 'no'
        if os.path.isfile('/etc/autocam.txt') is False:
            return
        myfile = open('/etc/autocam.txt', 'r')
        myfile2 = open('/etc/autocam2.txt', 'w')
        icount = 0
        for line in myfile.readlines():
            if line[:-1] == self.oldService.toString():
                delemu = 'yes'
                icount = icount + 1
                continue
            if delemu == 'yes':
                delemu = 'no'
                icount = icount + 1
                continue
            myfile2.write(line)
            icount = icount + 1

        myfile.close()
        myfile2.close()
        os.system('rm /etc/autocam.txt')
        os.system('cp /etc/autocam2.txt /etc/autocam.txt')

    def stardown(self):
        category = 'PluginEmulators.xml'
        from Plugins.Extensions.nssaddon.plugin import Categories
        self.session.open(Categories, category)
