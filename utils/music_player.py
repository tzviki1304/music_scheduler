import os
import random
import pygame

class MusicPlayer:
    def __init__(self, volume=0.7):
        pygame.mixer.init()
        self.volume = volume
        self.current_playlist = []
        self.current_song_index = -1

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

    def play(self):
        """Play the current song or start from the beginning of the playlist."""
        if not self.current_playlist:
            raise ValueError("No music loaded. Use load_playlist() first.")
        
        current_song = self.current_playlist[self.current_song_index]
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

    def play_next(self):
        """Play the next song in the playlist."""
        if not self.current_playlist:
            return
        
        self.current_song_index = (self.current_song_index + 1) % len(self.current_playlist)
        self.play()

    def stop(self):
        """Stop the current music playback."""
        pygame.mixer.music.stop()

    def shuffle_and_play(self):
        """Shuffle the playlist and play the first song."""
        if not self.current_playlist:
            print("MUSIC PLAYER: No music loaded. Use load_playlist() first.")
            return
        
        # Shuffle the playlist
        random.shuffle(self.current_playlist)
        
        # Reset to the first song
        self.current_song_index = 0
        
        # Play the first song
        current_song = self.current_playlist[self.current_song_index]
        print(f"MUSIC PLAYER: Playing song: {current_song}")
        
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
