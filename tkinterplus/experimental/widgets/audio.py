from tkinter import NORMAL, HORIZONTAL, EW, NW, VERTICAL, IntVar, DoubleVar, StringVar, Frame, Tk, Button, Label, Scale, Menubutton, Menu
from pygame import mixer
import soundfile

from .. import Tooltip
from ... import MaterialIcon

mixer.init()

#NOTE This widget is still being worked on. Expect issues for missing features!
#TODO Create a way to hangle updating the visual timer.
#TODO Make this use winsound if user is on windows. else use pygame.mixer
class Audio(Frame):
    def __init__(self, master:Tk, controls:bool=True, state=NORMAL, bg:str=None, fg:str=None, activebackground:str=None, activeforeground:str=None, troughcolor:str=None, bordercolor:str=None, borderwidth:int=None):
        """Construct an audio widget with the parent MASTER."""
        self.file = None
        self.volume_state = 'hidden'
        self.audio_state = 'stopped'
        self._LABEL = StringVar()
        self._LABEL.set('0:00/0:00')
        self.update_event = None
        self.update_timer = 1 * 1000
        self._TIME = IntVar()
        self.seconds = DoubleVar()
        self.total_seconds = DoubleVar()
        self._loop = None

        # widget configure
        self.state = NORMAL
        self.controls = False
        self.bg = '#f0f0f0'
        self.fg = 'black'
        self.activebackground = '#f0f0f0'
        self.activeforeground = 'black'
        self.troughcolor = 'white'
        self.borderwidth = 1
        self.bordercolor = 'black'
        super().__init__(master, bg=self.bg, highlightthickness=self.borderwidth, highlightbackground=self.bordercolor)

        # Load needed icons
        self.PLAY = MaterialIcon('play_arrow', size=(23, 23), color=self.fg)
        self.PAUSE = MaterialIcon('pause', size=(23, 23), color=self.fg)
        self.OPTIONS = MaterialIcon('more_vert', size=(23, 23), color=self.fg)
        self.VOLUME_DOWN = MaterialIcon('volume_down', size=(23, 23), color=self.fg)
        self.VOLUME_UP = MaterialIcon('volume_up', size=(23, 23), color=self.fg)
        self.VOLUME_MUTE = MaterialIcon('volume_off', size=(23, 23), color=self.fg)

        self.configure(
            controls=controls,
            state=state,
            bg=bg,
            fg=fg,
            activebackground=activebackground,
            activeforeground=activeforeground,
            troughcolor=troughcolor,
            borderwidth=borderwidth,
            bordercolor=bordercolor
        )

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

    def _scrub(self, e):
        seconds = (int(e) / 100) * self.total_seconds.get()
        self.seek(seconds)

    def _create_controls(self):
        self._remove_controls()
        self._button = Button(self, image=self.PLAY, bd=0, highlightthickness=0, command=self.toggle, bg=self.bg, activebackground=self.activebackground, activeforeground=self.activeforeground)
        self._label = Label(self, textvariable=self._LABEL, bg=self.bg, fg=self.fg,  activebackground=self.activebackground, activeforeground=self.activeforeground)
        self._scale = Scale(self, orient=HORIZONTAL, variable=self._TIME, command=self._scrub, showvalue=False, bg=self.bg, highlightthickness=2, highlightbackground=self.bg, troughcolor=self.troughcolor, activebackground=self.activebackground)
        self._volume = Button(self, image=self.VOLUME_UP, bd=0, highlightthickness=0, bg=self.bg, activebackground=self.activebackground, activeforeground=self.activeforeground)

        tip = Tooltip(self._volume, follow=False)
        Scale(tip, orient=VERTICAL).grid(row=0,column=0)

        self._volume_scale = Scale(self, orient=HORIZONTAL, showvalue=False)

        self._more = Menubutton(self, image=self.OPTIONS, bd=0, highlightthickness=0, bg=self.bg, activebackground=self.activebackground, activeforeground=self.activeforeground)
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

        # Bind icons
        self.VOLUME_UP.bind_widget(self._volume)
        self.OPTIONS.bind_widget(self._more)
        self.PLAY.bind_widget(self._button)

        super().configure(padx=5,pady=5)

    def _total_time(self):
        t_ms = self.total_seconds.get() * 1000
        t_seconds = (t_ms / 1000) % 60
        t_minutes = ((t_ms / (1000*60)) % 60)
        t_hours   = ((t_ms / (1000*60*60)) % 24)
        if t_hours>=0: return '%02d:%02d'%(t_minutes, t_seconds)
        return '%02d:%02d:%02d'%(t_hours, t_minutes, t_seconds)

    def update_time(self, loop:bool=False, move:bool=True):
        # TODO This should use the Scale (self._TIME) to calc the time in the song instead of mixer.music.get_pos()
        ms = ((self.total_seconds.get() * self._scale.get()) / 100) * 1000


        # print(mixer.music.get_pos(), s*1000)

        # ms = mixer.music.get_pos()
        if ms > -1:
            self.seconds.set(ms / 1000)
            seconds = (ms / 1000) % 60
            minutes = ((ms / (1000*60)) % 60)
            hours   = ((ms / (1000*60*60)) % 24)
            total = self._total_time()
            if hours>=0:
                current = '%02d:%02d'%(minutes, seconds)
                time = '%s/%s'%(current, total)
            else:
                current = '%02d:%02d:%02d'%(hours, minutes, seconds)
                time = '%s/%s'%(current, total)
            self._LABEL.set(time)

            # Update scale when updated automatically
            # if move:
            #     mix = mixer.music.get_pos() / 1000
            #     ttime = (mix / self.total_seconds.get()) * 100
            #     print(ttime)
            #     self._TIME.set(ttime)
            
            if loop and self.audio_state=='playing': self._loop = self.after(self.update_timer, lambda: self.update_time(True))
        

    def open(self, file):
        """Load the sound file"""
        mixer.music.load(file)
        f = soundfile.SoundFile(file)
        self.seconds.set(0.0)
        self.total_seconds.set(f.frames / f.samplerate)
        f.close()

        # update label
        time = '00:00/%s'%(self._total_time())
        self._LABEL.set(time)

    def volume_up(self): print('up')
    def volume_down(self): print('down')
    def volume_mute(self): print('mute')

    def play(self, loops:int=0, start:float=0.0, fade_ms:int=0):
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
        if self._loop!=None: self.after_cancel(self._loop)
        self.after(self.update_timer, lambda: self.update_time(True))
        self.audio_state='playing'
        self._button.configure(image=self.PAUSE, command=self.pause)

    def seek(self, seconds:float):
        """Seek through the audio track"""
        mixer.music.stop()
        mixer.music.play(0, seconds)
        if self.audio_state != 'playing': self.pause()
        self.update_time(move=False)
    
    def toggle(self):
        if self.audio_state == 'playing': self.pause()
        elif self.audio_state == 'stopped': self.play()
        elif self.audio_state == 'paused': self.unpause()

    # Normal methods

    def configure(self, **kw):
        if 'controls' in kw and kw['controls']!=None:
            self.controls = kw['controls']
            if self.controls==True: self._create_controls()
            elif self.controls==False: self._remove_controls()
        if 'state' in kw and kw['state']!=None:
            self.state = kw['state']
            self._button.configure(state=self.state)
            self._scale.configure(state=self.state)
            self._volume.configure(state=self.state)
            self._more.configure(state=self.state)
            
        if 'bordercolor' in kw and kw['bordercolor']!=None:
            self.bordercolor = kw['bordercolor']
            super().configure(highlightbackground=self.bordercolor)

        if 'borderwidth' in kw and kw['borderwidth']!=None:
            self.borderwidth = kw['borderwidth']
            super().configure(highlightthickness=self.borderwidth)
    
        if 'bg' in kw and kw['bg']!=None:
            self.bg = kw['bg']
            super().configure(bg=self.bg)
            self._button.configure(bg=self.bg)
            self._label.configure(bg=self.bg)
            self._volume.configure(bg=self.bg)
            self._more.configure(bg=self.bg)
            self._scale.configure(highlightbackground=self.bg)

        if 'fg' in kw and kw['fg']!=None:
            self.fg = kw['fg']
            self._label.configure(fg=self.fg)
            self._scale.configure(bg=self.fg)

            self.PLAY.configure(color=self.fg)
            self.PAUSE.configure(color=self.fg)
            self.OPTIONS.configure(color=self.fg)
            self.VOLUME_DOWN.configure(color=self.fg)
            self.VOLUME_UP.configure(color=self.fg)
            self.VOLUME_MUTE.configure(color=self.fg)

        if 'activebackground' in kw and kw['activebackground']!=None:
            self.activebackground = kw['activebackground']
            self._button.configure(activebackground=self.activebackground)
            self._label.configure(activebackground=self.activebackground)
            self._volume.configure(activebackground=self.activebackground)
            self._more.configure(activebackground=self.activebackground)
            self._scale.configure(activebackground=self.activebackground)
            
        if 'activeforeground' in kw and kw['activeforeground']!=None:
            self.activeforeground = kw['activeforeground']
            self._button.configure(activeforeground=self.activeforeground)
            self._label.configure(activeforeground=self.activeforeground)
            self._volume.configure(activeforeground=self.activeforeground)
            self._more.configure(activeforeground=self.activeforeground)
            
        if 'troughcolor' in kw and kw['troughcolor']!=None:
            self.troughcolor = kw['troughcolor']
            self._scale.configure(troughcolor=self.troughcolor)

    config = configure

    def bind(self, sequence, func):
        #TODO Add custom seq: <<Play>> <<Stop>> <<Pause>> <<Unpause>> <<Seek>> <<End>>
        super().bind(sequence, func)
