import os
import random
import pygame
import threading
import time

class MusicPlayer:
    def __init__(self, volume=0.7):
        pygame.mixer.init()
        self.volume = volume
        self.current_playlist = []
        self.current_song_index = -1
        self._playback_thread = None
        self._stop_playback = False
        self._stop_duration = 0  # Duration to stop playback in minutes
        self._stop_timer = None

    def set_volume(self, volume):
        """Set the volume of the music player."""
        self.volume = volume
        pygame.mixer.music.set_volume(volume)

    def load_playlist(self, music_folder):
        """Load all music files from a specified folder."""
        if not os.path.exists(music_folder):
            raise ValueError(f"Music folder {music_folder} does not exist.")
        
        # Support multiple audio formats
        supported_formats = ['.mp3', '.wav', '.ogg', '.flac']
        
        self.current_playlist = [
            os.path.join(music_folder, song) 
            for song in os.listdir(music_folder) 
            if os.path.splitext(song)[1].lower() in supported_formats
        ]
        
        random.shuffle(self.current_playlist)
        self.current_song_index = 0

    def _stop_after_duration(self):
        """Stop playback after specified duration."""
        time.sleep(self._stop_duration * 60)  # Convert minutes to seconds
        self.stop()

    def _continuous_playback(self):
        """Manage continuous playback of songs in the playlist."""
        self._stop_playback = False
        
        # Start stop timer if duration is set
        if self._stop_duration > 0:
            self._stop_timer = threading.Thread(target=self._stop_after_duration, daemon=True)
            self._stop_timer.start()
        
        while not self._stop_playback and self.current_playlist:
            try:
                # Play current song
                current_song = self.current_playlist[self.current_song_index]
                print(f"MUSIC PLAYER: Playing song: {current_song}")
                
                pygame.mixer.music.load(current_song)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play()
                
                # Wait for the song to finish
                while pygame.mixer.music.get_busy() and not self._stop_playback:
                    time.sleep(1)
                
                # Move to next song if not stopped
                if not self._stop_playback:
                    self.current_song_index = (self.current_song_index + 1) % len(self.current_playlist)
            
            except Exception as e:
                print(f"MUSIC PLAYER: Error during playback: {e}")
                break

    def shuffle_and_play(self, stop_duration=0):
        """
        Shuffle the playlist and start continuous playback.
        
        :param stop_duration: Duration to play music in minutes (0 means play indefinitely)
        """
        if not self.current_playlist:
            print("MUSIC PLAYER: No music loaded. Use load_playlist() first.")
            return
        
        # Stop any existing playback
        self.stop()
        
        # Set stop duration
        self._stop_duration = stop_duration
        
        # Shuffle the playlist
        random.shuffle(self.current_playlist)
        
        # Reset to the first song
        self.current_song_index = 0
        
        # Start continuous playback in a separate thread
        self._playback_thread = threading.Thread(target=self._continuous_playback, daemon=True)
        self._playback_thread.start()

    def stop(self):
        """Stop the current music playback."""
        self._stop_playback = True
        
        # Wait for playback thread to finish
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join()
        
        # Stop pygame music
        pygame.mixer.music.stop()
