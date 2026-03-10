from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import pywinstyles
import sv_ttk

from ui import UI

# Gabriel Bassoi
"""
This is a Python application that generates binaural beats based on user input frequencies. 
It features a graphical user interface (GUI) built with Tkinter, allowing users to control various aspects of the 
sound generation, including frequency, volume, and timer settings. The application also includes a visualizer that 
displays the audio waveform in real-time.
"""

class Main:
    """
    Main application class that initializes the UI and starts the main loop
    """

    def __init__(self):
        self.ui = UI()
        self.menu_frame: ttk.Frame = ttk.Frame(self.ui.root, padding='16 16 16 16')
        self.control_frame: ttk.Frame = ttk.Frame(self.ui.root, padding='16 0 16 16')
        self.main_frame: ttk.Frame = ttk.Frame(self.ui.root, padding='16 0 16 16')
        self.hertz_frame: ttk.Frame = ttk.Frame(self.ui.root, padding='16 16 16 16')
        self.viz_frame: ttk.Frame = ttk.Frame(self.ui.root, padding='16 16 16 16')

        self.init_ui()
        self.init_frames()

        self.ui.root.mainloop()

    def init_ui(self):
        self.ui.root.title('Hertz - Beat Generator')
        self.ui.root.resizable(False, False)
        self.ui.root.geometry('650x760')

        self.menu_frame.pack(fill='x', side='top')
        self.control_frame.pack(fill='x', side='top')
        self.main_frame.pack(expand=True, side='top')
        self.hertz_frame.pack(expand=True, side='top', anchor='center')
        self.viz_frame.pack(fill='both', expand=True, side='bottom')

        sv_ttk.set_theme('dark')
        self.ui.root.update_idletasks()

        pywinstyles.change_header_color(self.ui.root, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")

    def init_frames(self):
        self.create_menu_frame()
        self.create_control_frame()
        self.create_main_frame()
        self.create_hertz_frame()
        self.create_viz_frame()

    def create_menu_frame(self):
        self.menu_frame.columnconfigure(1, weight=1)
        self.menu_frame.columnconfigure(2, weight=1)
        self.menu_frame.columnconfigure(9, weight=1)

        # Play/Pause Button
        self.ui.play_pause_button = self.ui.create_button(self.menu_frame, text='▶', command=self.ui.play_stop, column=0, width=12)


        # Volume Scale
        self.ui.volume_scale = ttk.Scale(self.menu_frame,
                                     orient='horizontal',
                                     length=100, from_=0,
                                     to=100,
                                     command=self.ui.update_volume_label)
        self.ui.volume_scale.grid(column=2, row=2, columnspan=6, sticky='we', padx=2, pady=5)
        self.ui.volume_scale.set(self.ui.sound.volume * 100)

        # Volume Text
        self.ui.text_volume_label = self.ui.create_label(self.menu_frame, text='50%', column=8, row=2, padx=2)

        # Theme toggle button
        self.ui.create_button(self.menu_frame, text='🌓', command=self.ui.toggle_theme, column=10, width=3)

    def create_control_frame(self):
        self.control_frame.columnconfigure(3, weight=1)

        # Timer input
        self.ui.create_label(self.control_frame, text='Timer (min):', column=0, row=0, sticky='e', padx=2)
        self.ui.timer_entry = self.ui.create_entry(self.control_frame, textvariable=None, column=2, row=0, sticky='w', initial_value='0')

        # Timer label
        self.ui.timer_label = self.ui.create_label(self.control_frame, text='', column=3, row=0, padx=5, foreground='#0d6efd')

    def create_hertz_frame(self):
        # Frequency Entry
        self.ui.frequency_entry = self.ui.create_entry(self.hertz_frame, textvariable=self.ui.frequency, column=0, row=0, sticky='e',
                                             initial_value='0')
        self.ui.create_label(self.hertz_frame, text='Hz', column=1, row=0, padx=(5, 15))

        # Frequency Difference Entry
        self.ui.frequency_diff_entry = self.ui.create_entry(self.hertz_frame, textvariable=self.ui.frequency_diff, column=3, row=0,
                                                  sticky='e', initial_value='0')
        self.ui.create_label(self.hertz_frame, text='Diff', column=4, row=0, padx=(5, 15))

        # Beat frequency display
        self.ui.beat_label = self.ui.create_label(self.hertz_frame, text='Beat: -- Hz', column=6, row=0, sticky='e', padx=5)

    def create_viz_frame(self):
        # Visualization
        self.ui.visualizer.fig = Figure(figsize=(5, 4.2), dpi=80)
        self.ui.visualizer.ax1 = self.ui.visualizer.fig.add_subplot(311)
        self.ui.visualizer.ax2 = self.ui.visualizer.fig.add_subplot(312)
        self.ui.visualizer.ax3 = self.ui.visualizer.fig.add_subplot(313)
        self.ui.visualizer.fig.tight_layout(pad=2.0)
        self.ui.visualizer.fig.patch.set_facecolor('#1c1c1c')

        self.ui.visualizer.style_axis()

        self.ui.visualizer.canvas = FigureCanvasTkAgg(self.ui.visualizer.fig, master=self.viz_frame)

        self.ui.visualizer.update_visualization(first_update=True)

        self.ui.visualizer.canvas.get_tk_widget().pack(fill='both', expand=True)

    def create_main_frame(self):
        # Buttons
        padding = 6
        buttons_list = [
            ['Relieves Pain & Stress', '174', 0, 0],
            ['Heals Tissues & Organs', '285', 0, 1],
            ['Eliminates Fear', '396', 0, 2],
            ['Wipes out Negativity', '417', 1, 0],
            ['Repairs DNA', '528', 1, 1],
            ['Brings Loves & Compassion', '639', 1, 2],
            ['Detoxifies Cells & Organs', '741', 2, 0],
            ['Awakens Intuition', '852', 2, 1],
            ['Connects to Higher self', '963', 2, 2]
        ]

        for button in buttons_list:
            self.ui.create_type_button(self.main_frame, text=button[0], frequency=button[1], padding=padding, column=button[2], row=button[3])


if __name__ == '__main__':
    main = Main()