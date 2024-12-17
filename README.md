# Music Scheduler Application

A Python-based music scheduling application with a modern GUI that allows users to schedule music playback at specific times on selected days.

## Features

- 🎵 Schedule music playback for specific times and days
- 📂 Select music folders for playback
- 🔊 Volume control with visual feedback
- 📅 Day selection with Hebrew interface
- 💾 Save and load schedule settings
- 🔄 Shuffle and play functionality
- ⏹️ Stop music playback
- 🎯 Test play feature

## Requirements

- Python 3.x
- Required Python packages:
  - tkinter
  - pygame
  - schedule
  
```bash
pip install pygame schedule
```

## Installation

1. Clone this repository
2. Install the required packages
3. Run `music_scheduler.py`

## Usage

1. Select a music folder containing MP3 or WAV files
2. Choose the desired time for playback
3. Select the days you want the music to play
4. Adjust the volume as needed
5. Click "Add Schedule" to create a new schedule
6. Your schedules will be saved automatically
7. Use the "Shuffle and Play" button to play songs one after the other in random order

## Configuration

The application saves its settings in `music_scheduler_settings.json` in the same directory as the application.

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

This README provides a clear overview of your application, its features, setup instructions, and basic usage guidelines. You can modify it further based on any specific details or requirements you'd like to add.
