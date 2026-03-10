# Gabriel Bassoi
"""
UI Module - Main user interface for the Binaural Beats Generator

This module handles all GUI components and user interactions for the binaural
beats application.
"""

from tkinter import ttk, Tk, StringVar, BooleanVar

import pywinstyles
import sv_ttk

from sound import Sound
from timer import Timer
from visualizer import Visualizer


class UI:
    """
    Main UI class that initializes the application and manages all widgets and interactions
    """

    # Type hints for widgets that will be created later
    frequency_entry: ttk.Entry
    frequency_diff_entry: ttk.Entry
    timer_entry: ttk.Entry
    play_pause_button: ttk.Button
    timer_label: ttk.Label
    text_volume_label: ttk.Label
    volume_scale: ttk.Scale
    beat_label: ttk.Label

    def __init__(self):
        self.root = Tk()

        self.sound = Sound()
        self.timer = Timer(self)
        self.visualizer = Visualizer(self)

        self.frequency = StringVar()
        self.frequency_diff = StringVar()
        self.volume: int = 50
        self.last_volume: int = 50

    def create_type_button(self, frame: ttk.Frame, text: str, frequency: str, padding: int, column: int, row: int) -> ttk.Button:
        button = ttk.Button(frame, text=text, command=lambda: self._set_frequency(frequency))
        button.grid(column=column, row=row, sticky='we', padx=padding, pady=5)
        return button

    def create_label(self, frame: ttk.Frame, text: str, column: int, row: int, sticky: str = 'w', padx = 0, foreground: str = None) -> ttk.Label:
        label = ttk.Label(frame, text=text, foreground=foreground)
        label.grid(column=column, row=row, sticky=sticky, padx=padx)
        return label

    def create_button(self, frame: ttk.Frame, text: str, command, column: int, width:int=8, color: str = None) -> ttk.Button:
        button = ttk.Button(frame, text=text, command=command, width=width)
        button.grid(column=column, row=2, sticky='we', padx=2, pady=5)
        if color:
            pywinstyles.set_opacity(button, color=color)
        return button

    def create_entry(self, frame: ttk.Frame, textvariable, column: int, row: int, sticky: str = 'w', initial_value: str = None) -> ttk.Entry:
        entry = ttk.Entry(frame, width=12, textvariable=textvariable)
        entry.grid(column=column, row=row, sticky=sticky, padx=2)
        if initial_value is not None:
            entry.insert(0, initial_value)
        return entry

    def _set_frequency(self, frequency: str):
        """
        Set frequency in the entry field when a preset button is clicked
        :param frequency: Frequency value to set
        """
        self.frequency_entry.delete(first=0, last=1000)
        self.frequency_entry.insert(0, frequency)

    def play_stop(self):
        if self.sound.is_playing:
            self.stop()
        elif self.frequency_entry.get() and self.frequency_diff_entry.get():
            self.play()

    def play(self):
        self.play_pause_button.config(text='■')

        self.sound.frequency = int(self.frequency_entry.get())
        self.sound.frequency_diff = float(self.frequency_diff_entry.get() or 0.0)

        self.sound.play()
        self.visualizer.update_visualization()
        self.timer.start_timer(self.timer_entry.get())

    def stop(self):
        self.play_pause_button.config(text='▶')

        self.sound.stop()
        self.timer_label.config(text='')

    def update_volume_label(self, volume):
        """
        Updated the volume label.
        Stops and plays the sound with the new volume.
        last_volume is used to prevent unnecessary restarts when the volume is unchanged.
        """
        self.volume = int(float(volume))
        if hasattr(self, 'text_volume_label') and self.sound.is_playing and self.last_volume != self.volume:
            self.last_volume = self.volume

            self.text_volume_label.config(text=str(self.volume) + '%')
            self.sound.volume = self.volume / 100
            self.sound.play(volume_update=True)

    def toggle_theme(self):
        current_theme = sv_ttk.get_theme()
        new_theme = 'light' if current_theme == 'dark' else 'dark'

        sv_ttk.set_theme(new_theme)
        pywinstyles.change_header_color(self.root, "#1c1c1c" if new_theme == "dark" else "#fafafa")

        # Update matplotlib colors

        if new_theme == 'dark':
            self.visualizer.fig.patch.set_facecolor('#1c1c1c')
        else:
            self.visualizer.fig.patch.set_facecolor('#fafafa')

        self.visualizer.style_axis()
        self.visualizer.canvas.draw()
