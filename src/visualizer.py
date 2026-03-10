# Gabriel Bassoi
"""
Visualizer class for displaying audio waveforms using Matplotlib.
"""
import sv_ttk
from matplotlib.axes import Axes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D


class Visualizer:
    """
    Visualizer class for displaying audio waveforms using Matplotlib.
    """

    # Type hints for elements of the chart that will be created later
    ax1: Axes
    ax2: Axes
    ax3: Axes
    canvas: FigureCanvasTkAgg
    fig: Figure

    line1: Line2D
    line2: Line2D
    line3: Line2D

    def __init__(self, ui):
        self.ui = ui

    def update_visualization(self, first_update=False):

        audio_data = self.ui.sound.get_current_audio_data()
        combined_data = self.ui.sound.get_current_combined_audio_data()

        if first_update:
            # Create line objects once
            x = range(1000)
            self.line1, = self.ax1.plot(x, audio_data[:1000, 0], color='#0d6efd', linewidth=0.8)
            self.line2, = self.ax2.plot(x, audio_data[:1000, 1], color='#0d6efd', linewidth=0.8)
            self.line3, = self.ax3.plot(x, combined_data[:1000], color='#20c997', linewidth=0.8)

        else:
            # Update existing line data
            self.line1.set_ydata(audio_data[:1000, 0])
            self.line2.set_ydata(audio_data[:1000, 1])
            self.line3.set_ydata(combined_data[:1000])

        self.canvas.draw()

        beat_freq = abs(self.ui.sound.frequency_diff)
        if self.ui.sound.is_playing:
            self.ui.beat_label.config(text=f'Beat: {beat_freq} Hz')
        else:
            self.ui.beat_label.config(text='Beat: -- Hz')

    def style_axis(self):
        theme_color = 'white' if sv_ttk.get_theme() == 'dark' else 'black'

        for ax, name in zip((self.ax1, self.ax2, self.ax3), ('Left', 'Right', 'Combined')):
            ax.set_facecolor('#2b2b2b' if sv_ttk.get_theme() == 'dark' else '#f0f0f0')
            ax.yaxis.label.set_color(theme_color)
            ax.set_ylim(-1, 1)
            ax.tick_params(axis='both', labelsize=9)

            # Remove numeric ticks entirely
            ax.set_xticks([])
            ax.set_yticks([])

            ax.set_ylabel(name, fontsize=12)

            ax.grid(True, color=theme_color, alpha=0.25, linewidth=0.8)