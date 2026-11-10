# -*- coding: utf-8 -*-
## this plugin recoded by Lululla 2026
## 
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Input import Input
from Components.Label import Label
from Components.Pixmap import Pixmap
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from enigma import ePicLoad, getDesktop
from twisted.internet import reactor

import os
import urllib.request
from . import _

configFile = '/usr/lib/enigma2/python/Plugins/Extensions/TelevideoRAI/page.txt'

REGIONS = {
    "Nazionale": "nazionale", "Abruzzo": "abruzzo", "Alto Adige": "alto-adige",
    "Basilicata": "basilicata", "Calabria": "calabria", "Campania": "campania",
    "Emilia-Romagna": "emilia-romagna", "Friuli V.G.": "friuli-venezia-giulia",
    "Lazio": "lazio", "Liguria": "liguria", "Lombardia": "lombardia",
    "Marche": "marche", "Molise": "molise", "Piemonte": "piemonte",
    "Puglia": "puglia", "Sardegna": "sardegna", "Sicilia": "sicilia",
    "Toscana": "toscana", "Umbria": "umbria", "Valle d'Aosta": "valle-d-aosta",
    "Veneto": "veneto"
}

FORCE_RESOLUTION = None 


class PictureScreen(Screen):
    def __init__(self, session, picPath=None):
        if FORCE_RESOLUTION:
            screen_width = FORCE_RESOLUTION
            screen_height = int(screen_width * 9 / 16)
        else:
            screen_width = getDesktop(0).size().width()
            screen_height = getDesktop(0).size().height()

        btn_h = int(screen_height * 0.08)
        font_sz = int(btn_h * 0.4)
        bar_y = screen_height - btn_h

        self.skin = f"""
            <screen name="PictureScreen" position="center,center" size="{screen_width},{screen_height}"
            title="TelevideoRAI" backgroundColor="#00000000">
            
            <widget name="myPic" position="0,0" size="{screen_width},{screen_height}"
            zPosition="0" alphatest="on" />
            
            <widget name="bottombar" position="0,{bar_y}" size="{screen_width},{btn_h}" 
            backgroundColor="#000000" zPosition="1" />

            <widget name="label_red" position="20,{bar_y}" size="160,{btn_h}" 
            font="Regular;{font_sz}" halign="center" valign="center" foregroundColor="#ff4444" text="Indietro" zPosition="2" />
            <widget name="label_green" position="180,{bar_y}" size="160,{btn_h}" 
            font="Regular;{font_sz}" halign="center" valign="center" foregroundColor="#44ff44" text="Avanti" zPosition="2" />
            <widget name="label_yellow" position="340,{bar_y}" size="120,{btn_h}" 
            font="Regular;{font_sz}" halign="center" valign="center" foregroundColor="#ffff44" text="+10" zPosition="2" />
            <widget name="label_blue" position="460,{bar_y}" size="120,{btn_h}" 
            font="Regular;{font_sz}" halign="center" valign="center" foregroundColor="#3399ff" text="+100" zPosition="2" />

            <widget name="label_region" position="600,{bar_y}" size="450,{btn_h}" 
            font="Regular;{font_sz}" halign="center" valign="center" foregroundColor="#00ff00" text="MENU: Nazionale" zPosition="2" />
            
            <widget name="label_exit" position="{screen_width-210},{bar_y}" size="200,{btn_h}" 
            font="Regular;{font_sz}" halign="center" valign="center" foregroundColor="#ffffff" text="EXIT: Chiudi" zPosition="2" />
        </screen>"""

        Screen.__init__(self, session)
        
        self.session = session
        self.picPath = picPath
        self.page = 201
        self.tmpPage = ''
        self.spage = 1
        self.current_region = "nazionale"

        # Salviamo lo stato iniziale per il rollback
        self.prev_page = self.page
        self.prev_spage = self.spage
        self.prev_region = self.current_region

        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self.PicLoad.PictureData.get().append(self.DecodePicture)

        self['myPic'] = Pixmap()
        self['bottombar'] = Label()
        self['label_red'] = Label()
        self['label_green'] = Label()
        self['label_yellow'] = Label()
        self['label_blue'] = Label()
        self['label_region'] = Label()
        self['label_exit'] = Label()

        self['myActionsMap'] = ActionMap([
            'OkCancelActions', 'ColorActions', 'DirectionActions', 'NumberActions', 'InfoActions', 'MenuActions'
        ], {
            'ok': self.myInput,
            'green': self.GreenButton,
            'left': self.LeftButton,
            'right': self.RightButton,
            'red': self.RedButton,
            'yellow': self.YellowButton,
            'blue': self.BlueButton,
            'cancel': self.ExitButton,
            'menu': self.SelectRegion,
            '0': self.Key0, '1': self.Key1, '2': self.Key2, '3': self.Key3,
            '4': self.Key4, '5': self.Key5, '6': self.Key6, '7': self.Key7,
            '8': self.Key8, '9': self.Key9,
            'info': self.InfoButton,
        }, -1)

        self.readFile()
        self.onLayoutFinish.append(self.LoadPage)

    def readFile(self):
        try:
            if os.path.exists(configFile):
                with open(configFile, 'r') as mf:
                    line = mf.readline().strip()
                if line:
                    self.page = int(line)
                    self.prev_page = self.page # Aggiorna anche il prev
        except Exception as e:
            print('[PictureScreen] readFile error:', e)

    def saveFile(self):
        try:
            with open(configFile, 'w') as mf:
                mf.write(str(self.page))
        except Exception as e:
            print('[PictureScreen] saveFile error:', e)

    def update_region_label(self):
        # Trova il nome della regione corrispondente allo slug attuale
        for name, slug in REGIONS.items():
            if slug == self.current_region:
                self['label_region'].setText(f"MENU: {name}")
                break

    def ExitButton(self):
        self.saveFile()
        self.close()

    def SelectRegion(self):
        region_list = [(name, slug) for name, slug in REGIONS.items()]
        self.session.openWithCallback(
            self.regionSelected, ChoiceBox,
            title=_("Seleziona Regione"), list=region_list)

    def regionSelected(self, choice):
        if choice:
            region_name, region_slug = choice
            self.current_region = region_slug
            self.page = 100
            self.spage = 1
            self.update_region_label() # Aggiorna la label subito
            self.LoadPage()

    def myInput(self):
        self.session.openWithCallback(
            self.askForWord, InputBox,
            title=_('Please enter a page number:'),
            text=str(self.page), maxSize=3, type=Input.NUMBER)

    def askForWord(self, word):
        if not word:
            return
        try:
            self.page = int(word)
        except ValueError:
            return
        self.LoadPage()

    def InfoButton(self):
        self.session.open(MessageBox, _('TelevideoRAI\nTasti colorati per navigare.\nMENU per le Regioni.\nDigita il numero di pagina.'), MessageBox.TYPE_INFO)

    def RedButton(self):
        self.page -= 1; self.spage = 1; self.LoadPage()

    def GreenButton(self):
        self.page += 1; self.spage = 1; self.LoadPage()

    def LeftButton(self):
        if self.spage > 1:
            self.spage -= 1
        self.LoadPage()

    def RightButton(self):
        self.spage += 1; self.LoadPage()

    def YellowButton(self):
        self.page += 10; self.spage = 1; self.LoadPage()

    def BlueButton(self):
        self.page += 100; self.spage = 1; self.LoadPage()

    def NumberButton(self, number):
        self.tmpPage += number
        if len(self.tmpPage) == 3:
            try:
                self.page = int(self.tmpPage)
            except ValueError:
                pass
            self.tmpPage = ''
            self.spage = 1
            self.LoadPage()

    def Key0(self): self.NumberButton('0')
    def Key1(self): self.NumberButton('1')
    def Key2(self): self.NumberButton('2')
    def Key3(self): self.NumberButton('3')
    def Key4(self): self.NumberButton('4')
    def Key5(self): self.NumberButton('5')
    def Key6(self): self.NumberButton('6')
    def Key7(self): self.NumberButton('7')
    def Key8(self): self.NumberButton('8')
    def Key9(self): self.NumberButton('9')

    def LoadPage(self):
        self.prev_page = self.page
        self.prev_spage = self.spage
        self.prev_region = self.current_region

        if self.spage < 2:
            self.url = f'https://www.rainews.it/tlvd/images/{self.current_region}/16_9_page-{self.page}.png'
        else:
            self.url = f'https://www.rainews.it/tlvd/images/{self.current_region}/16_9_page-{self.page}.{self.spage}.png'
        
        print('-GG8 - URL:', self.url)
        self.download(self.url, '/tmp/myPic.png')

    def download(self, url, path):
        def _thread_download():
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response: # Timeout ridotto a 10s
                    with open(path, 'wb') as f:
                        f.write(response.read())
                reactor.callFromThread(self.downloadDone, None)
            except Exception as e:
                reactor.callFromThread(self.downloadError, e)

        reactor.callInThread(_thread_download)

    def downloadDone(self, raw=None):
        print('-GG8 - downloadDone')
        self.picPath = '/tmp/myPic.png'
        self.ShowPicture()

    def downloadError(self, failure):
        print('-GG8 - download error:', failure)
        self.page = self.prev_page
        self.spage = self.prev_spage
        self.current_region = self.prev_region
        self.update_region_label()

        if self['myPic'].instance is not None:
            self.session.open(
                MessageBox,
                _('Pagina non trovata o errore di rete.\nRimani alla pagina {}.').format(self.page),
                MessageBox.TYPE_ERROR, timeout=5)

    def ShowPicture(self):
        if self.picPath is not None and self['myPic'].instance is not None:
            self.PicLoad.setPara([
                self['myPic'].instance.size().width(),
                self['myPic'].instance.size().height(),
                self.Scale[0], self.Scale[1],
                0, 1, '#002C2C39'])
            self.PicLoad.startDecode(self.picPath)

    def DecodePicture(self, PicInfo=''):
        ptr = self.PicLoad.getData()
        if ptr is not None and self['myPic'].instance is not None:
            self['myPic'].instance.setPixmap(ptr)

    def cancel(self):
        print('[PictureScreen] - cancel')
        self.close(None)


def main(session, **kwargs):
    session.open(PictureScreen)


def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name='TelevideoRAI', description='TelevideoRAI',
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon='./plugin.png', fnc=main),
        PluginDescriptor(
            name='TelevideoRAI', description='TelevideoRAI',
            where=PluginDescriptor.WHERE_EXTENSIONSMENU,
            icon='./plugin.png', fnc=main),
    ]
