# Gabriel Bassoi
"""
Timer module for the sound player application.
"""


class Timer:
    """
    Timer class to handle the countdown timer functionality for the sound player application.
    """
    def __init__(self, ui):
        self.ui = ui

    def start_timer(self, time: str):
        """Start timer if value is specified"""
        time_seconds = self.minutes_to_seconds(time)
        if time_seconds > 0:
            self._start_timer_countdown(time_seconds)

    def _start_timer_countdown(self, seconds):
        """Display countdown timer"""
        if self.ui.sound.is_playing and seconds > 0:
            mins = seconds // 60
            secs = seconds % 60
            self.ui.timer_label.config(text=f'Time: {mins:02d}:{secs:02d}')
            self.ui.root.after(1000, lambda: self._start_timer_countdown(seconds - 1))
        elif seconds <= 0:
            self.ui.stop()

    def minutes_to_seconds(self, time):
        time_seconds = 0
        if time and int(time) > 0:
            time_seconds = int(time) * 60
        return time_seconds

