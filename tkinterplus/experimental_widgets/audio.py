from tkinter import NORMAL, HORIZONTAL, EW, VERTICAL, StringVar, Frame, Tk, Button, Label, Scale, Menubutton, Menu
from pygame import mixer
mixer.init()

from .. import PLAY, PAUSE, MORE_VERT, VOLUME_UP, VOLUME_DOWN, VOLUME_MUTE, Icon, Tooltip

#NOTE This widget is still being worked on. Expect issues for missing features!
#TODO Create a way to hangle updating the visual timer.
#TODO Make this use winsound if user is on windows. else use pygame.mixer
class Audio(Frame):
    def __init__(self, master:Tk, controls:bool=True, state=NORMAL):
        """
        Audio widget which may display and run sound files. Supported types: wav, mp3, ogg

        Parameters
        ---
        `master` - The _ROOT window

        `controls` - Whether or not to add controls. If set to False it will be an invisable widget.

        `state` - The state of the widget. NORMAL or DISABED
        """
        Frame.__init__(self, master, bg='gray')
        self.controls = False
        self.file = None
        self.state = NORMAL
        self.volume_state = 'hidden'
        self.audio_state = 'stopped'
        self._LABEL = StringVar()
        self._LABEL.set('0:00/0:00')
        self.update_event = None
        self.update_timer = 1 * 1000

        # Load needed icons
        self.PLAY = Icon(PLAY)
        self.PAUSE = Icon(PAUSE)
        self.OPTIONS = Icon(MORE_VERT)
        self.VOLUME_DOWN = Icon(VOLUME_DOWN)
        self.VOLUME_UP = Icon(VOLUME_UP)
        self.VOLUME_MUTE = Icon(VOLUME_MUTE)

        self.configure(controls=controls, state=state)

    def _remove_controls(self):
        for i in self.winfo_children():
            i.destroy()

    def _toggle_volume(self):
        if self.volume_state == 'hidden':
            self._volume_scale.grid(row=0,column=3)
            self.volume_state='shown'

        elif self.volume_state == 'shown':
            self._volume_scale.grid_forget()
            self.volume_state='hidden'

    def _create_controls(self):
        self._remove_controls()
        self._button = Button(self, image=self.PLAY, bd=0, highlightthickness=0, command=self.toggle)
        self._label = Label(self, textvariable=self._LABEL)
        self._scale = Scale(self, orient=HORIZONTAL, showvalue=False)

        self._volume = Button(self, image=self.VOLUME_UP, bd=0, highlightthickness=0)

        tip = Tooltip(self._volume)
        Scale(tip, orient=VERTICAL).grid(row=0,column=0)

        self._volume_scale = Scale(self, orient=HORIZONTAL, showvalue=False)

        self._more = Menubutton(self, image=self.OPTIONS, bd=0, highlightthickness=0)
        menu = Menu(self._more, tearoff=False)
        menu.add_command(label='Playback Speed')
        self._more.configure(menu=menu)
        
        self._button.grid(row=0,column=0)
        self._label.grid(row=0,column=1)
        self._scale.grid(row=0,column=2, sticky=EW)
        # vol Scale
        self._volume.grid(row=0,column=4)
        self._more.grid(row=0,column=5)
        self.grid_columnconfigure(2, weight=1)

        super().configure(padx=5,pady=5)

    def update_time(self, loop:bool=False):
        ms = mixer.music.get_pos()
        seconds = (ms / 1000) % 60
        minutes = ((ms / (1000*60)) % 60)
        hours   = ((ms / (1000*60*60)) % 24)

        if hours>=0:
            time = '%d:%d/1:00'%(minutes, seconds)
        else:
            time = '%d:%d:%d/1:00'%(hours, minutes, seconds)

        self._LABEL.set(time)
        print(time)

        if loop and self.audio_state=='playing': self._loop = self.after(self.update_timer, lambda: self.update_time(True))

    def load(self, file):
        """Load the sound file"""
        print('**SET MAX TIME**')
        mixer.music.load(file)

    def volume_up(self): print('up')
    def volume_down(self): print('down')
    def volume_mute(self): print('mute')

    def play(self, loops:int=0, start:float=0, fade_ms:int=0):
        """Play the audio from the start"""
        mixer.music.play(loops, start, fade_ms)
        if self.audio_state=='stopped': self.update_event = self.after(self.update_timer, lambda: self.update_time(True))
        self.audio_state='playing'
        self._button.configure(image=self.PAUSE, command=self.pause)

    def stop(self):
        """Stop the audio"""
        mixer.music.stop()
        self.after_cancel(self.update_event)
        self.audio_state='stopped'
        self._button.configure(image=self.PLAY, command=self.play)

    def pause(self):
        """Pause the audio"""
        mixer.music.pause()
        self.audio_state='paused'
        self._button.configure(image=self.PLAY, command=self.unpause)

    def unpause(self):
        """Play the audio from the last position"""
        mixer.music.unpause()
        self.after_cancel(self._loop)
        self.after(self.update_timer, lambda: self.update_time(True))
        self.audio_state='playing'
        self._button.configure(image=self.PAUSE, command=self.pause)

    def seek(self, pos):
        """Seek through the audio track"""
        pass
    
    def toggle(self):
        if self.audio_state == 'playing': self.pause()
        elif self.audio_state == 'stopped': self.play()
        elif self.audio_state == 'paused': self.unpause()

    # Normal methods

    def configure(self, **kw):
        if 'controls' in kw:
            self.controls = kw['controls']
            if self.controls==True: self._create_controls()
            elif self.controls==False: self._remove_controls()
        if 'state' in kw:
            self.state = kw['state']
            self._button.configure(state=self.state)
            self._scale.configure(state=self.state)
            self._volume.configure(state=self.state)
            self._more.configure(state=self.state)
    config = configure

    def bind(self, sequence, func):
        #TODO Add custom seq: <<Play>> <<Stop>> <<Pause>> <<Unpause>> <<Seek>>
        super().bind(sequence, func)
