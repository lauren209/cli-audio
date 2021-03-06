"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import os
from pathlib import Path
from exceptions.CLI_Audio_File_Exception import CLI_Audio_File_Exception

class Player:
    """Controls the actions of the player, such as pausing, quitting, and playing"""
    def __init__(self):
        """starts with no song being played"""
        self.currentSong = "Nothing playing."
        self.paused = True
        self.position = 0
        self.playlist = []

    def getCurrentSong(self):
        """returns the current song"""
        return self.currentSong

    def pause(self):
        """if the song is paused then the stream is stopped. One pressed again, the song continues"""
        if self.paused == False:
            self.paused = True
            self.stream.stop_stream()
        else:
            self.paused = False
            self.stream.start_stream()

    def play(self, track):
        """allows the player """
        self.paused = False
        try:
            if not Path(track).is_file():
                raise CLI_Audio_File_Exception
        except CLI_Audio_File_Exception:
            currentSong = "Nothing playing."
            print("File not found")
            return 0

        self.currentSong = track
        self.wf = wave.open(track, 'rb')

        # instantiate PyAudio (1)
        self.p = pyaudio.PyAudio()

        # open self.stream using callback (3)
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True,
                stream_callback=self.callback)

        # start the self.stream (4)
        self.stream.start_stream()

    def stop(self):
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            self.p.terminate() 
        except:
            pass

        

    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def list(self):
        self.songlist = []
        mylist = os.listdir("./media")

        for file in mylist:
            filename, extension = os.path.splitext(file)
            
            if extension == ".wav":
                self.songlist.append(filename)
            
        return self.songlist


