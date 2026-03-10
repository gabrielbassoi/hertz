# Gabriel Bassoi
"""
This module defines the Sound class, which generates and plays binaural beats using the sounddevice library.
"""
import time

import numpy as np
import sounddevice as sd


class Sound:
    """
    The Sound class generates and plays binaural beats based on specified parameters.
    """

    SAMPLE_RATE = 44100

    def __init__(self):
        sd.default.samplerate = self.SAMPLE_RATE

        self._frequency = 0
        self._duration = 5.0
        self._volume = 0.5
        self._frequency_diff = 0.0
        self._fade_enabled = False
        self._fade_duration = 2.0  # seconds
        self._tone = None
        self._is_playing = False

    def play(self, volume_update: bool = False):
        self._generate_audio_data()
        if not volume_update:
            self.play_fade(mode='in')
        sd.play(self._tone, loop=True)
        self._is_playing = True

    def stop(self):
        self.play_fade(mode='out')
        sd.stop()
        self._is_playing = False

    def play_fade(self, mode: str):
        if mode in ['in', 'out']:
            fade_samples = int(self._fade_duration * self.SAMPLE_RATE)

            if mode == 'in':
                fade_in = np.linspace(0, 1, fade_samples)
                fade = self._tone[:fade_samples] * fade_in[:, np.newaxis]
            else:
                fade_out = np.linspace(1, 0, fade_samples)
                fade = self._tone[-fade_samples:] * fade_out[:, np.newaxis]

            sd.play(fade, loop=False)
            time.sleep(self._fade_duration)

    def _generate_audio_data(self):
        t = np.linspace(0, self._duration, int(self.SAMPLE_RATE * self._duration), False)

        first_tone = 2 * np.pi * t

        left_tone = self._volume * np.sin(first_tone * self._frequency)
        right_tone = self._volume * np.sin(first_tone * (self._frequency + self._frequency_diff))

        self._tone = np.column_stack((left_tone, right_tone))

    @property
    def is_playing(self):
        return self._is_playing

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        self._frequency = frequency

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume

    @property
    def frequency_diff(self):
        return self._frequency_diff

    @frequency_diff.setter
    def frequency_diff(self, frequency_diff):
        self._frequency_diff = frequency_diff

    @property
    def fade_enabled(self):
        return self._fade_enabled

    @fade_enabled.setter
    def fade_enabled(self, enabled):
        self._fade_enabled = enabled

    def get_current_audio_data(self):
        """Get current stereo audio data for visualization"""
        if self._tone is not None:
            sample_length = min(4410, len(self._tone))
            return self._tone[:sample_length]
        return np.zeros((1000, 2))  # Return 1000 samples of silence

    def get_current_combined_audio_data(self):
        """Get difference (L-R) between channels for visualization."""
        audio_data = self.get_current_audio_data()
        if self._tone is not None:
            return audio_data[:, 0] - audio_data[:, 1]
        return np.zeros(1000)


