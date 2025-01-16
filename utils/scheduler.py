import schedule
import time
import threading
from datetime import datetime

class MusicScheduler:
    def __init__(self, music_player):
        self.music_player = music_player
        self.schedules = []
        self.running = False
        self._scheduler_thread = None

    def add_schedule(self, time_str, days=None, stop_duration=0):
        """
        Add a new schedule for music playback.
        
        :param time_str: Time in format 'HH:MM'
        :param days: List of days to play music (e.g., ['Monday', 'Wednesday'])
        :param stop_duration: Duration to play music in minutes (0 means play indefinitely)
        """
        schedule_info = {
            'time': time_str,
            'days': days or [],
            'stop_duration': stop_duration
        }
        self.schedules.append(schedule_info)

    def _job(self):
        """Internal job to play music at scheduled times."""
        current_day = datetime.now().strftime('%A')
        current_time = datetime.now().strftime('%H:%M')
        
        print(f"SCHEDULER: Checking schedules - Current day: {current_day}, Current time: {current_time}")
        print(f"SCHEDULER: Total schedules: {len(self.schedules)}")
        
        for schedule_info in self.schedules:
            print(f"SCHEDULER: Checking schedule: {schedule_info}")
            
            # Exact time match and day match
            time_match = schedule_info['time'] == current_time
            day_match = not schedule_info['days'] or current_day in schedule_info['days']
            
            print(f"SCHEDULER: Time match: {time_match}, Day match: {day_match}")
            
            if time_match and day_match:
                print(f"SCHEDULER: Playing music for schedule: {schedule_info}")
                try:
                    # Play music with optional stop duration
                    self.music_player.shuffle_and_play(stop_duration=schedule_info.get('stop_duration', 0))
                except Exception as e:
                    print(f"SCHEDULER: Error playing music: {e}")

    def start(self):
        """Start the scheduler in a separate thread."""
        if self.running:
            print("SCHEDULER: Scheduler already running")
            return

        print("SCHEDULER: Starting scheduler")
        self.running = True
        
        def _run_scheduler():
            # Clear any existing scheduled jobs first
            schedule.clear()
            
            # Schedule jobs for each schedule
            for schedule_info in self.schedules:
                print(f"SCHEDULER: Scheduling job for {schedule_info}")
                schedule.every().day.at(schedule_info['time']).do(self._job)

            while self.running:
                schedule.run_pending()
                time.sleep(1)

        self._scheduler_thread = threading.Thread(target=_run_scheduler, daemon=True)
        self._scheduler_thread.start()
        print("SCHEDULER: Scheduler thread started")

    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self._scheduler_thread:
            self._scheduler_thread.join()
        
        # Clear all scheduled jobs
        schedule.clear()

    def get_schedules(self):
        """Return the list of current schedules."""
        return self.schedules

    def remove_schedule(self, index):
        """Remove a schedule by its index."""
        if 0 <= index < len(self.schedules):
            del self.schedules[index]
