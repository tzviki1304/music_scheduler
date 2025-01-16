import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui.app_styles import AppStyles
from utils.music_player import MusicPlayer
from utils.scheduler import MusicScheduler
from utils.config import WINDOW_WIDTH, WINDOW_HEIGHT, SETTINGS_FILE, DEFAULT_SETTINGS

class MusicSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("מתזמן המוזיקה")
        
        # Initialize music player and scheduler
        self.music_player = MusicPlayer()
        self.music_scheduler = MusicScheduler(self.music_player)
        
        # Start the scheduler
        self.music_scheduler.start()
        
        # Configure window
        self._configure_window()
        
        # Configure styles
        AppStyles.configure_styles()
        
        # Create GUI first to initialize volume_var
        self.create_gui()
        
        # Then load settings
        self.load_settings()

    def _configure_window(self):
        """Configure window size and position with minimum dimensions."""
        # Set minimum window size
        self.root.minsize(400, 600)  # Minimum width and height

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate window size as percentage of screen
        window_width = int(screen_width * 0.6)  # 60% of screen width
        window_height = int(screen_height * 0.7)  # 70% of screen height

        # Center the window
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)

        # Set window geometry
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(True, True)  # Allow resizing

    def create_gui(self):
        """Create the main GUI layout with responsive scrollable content."""
        # Main container with both vertical and horizontal scrolling
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Canvas with both Vertical and Horizontal Scrollbars
        canvas = tk.Canvas(main_container, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(main_container, orient=tk.VERTICAL, command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(main_container, orient=tk.HORIZONTAL, command=canvas.xview)
        
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Grid layout for scrollbars and canvas
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Existing sections
        self._create_folder_section(scrollable_frame)
        self._create_volume_section(scrollable_frame)
        self._create_schedule_section(scrollable_frame)

    def _create_folder_section(self, parent):
        """Create music folder selection section."""
        folder_frame = ttk.LabelFrame(parent, text="בחירת תיקיית מוזיקה", style='Modern.TLabelframe')
        folder_frame.pack(fill=tk.X, pady=10)

        self.folder_label = ttk.Label(folder_frame, text="לא נבחרה תיקייה", style='Modern.TLabel')
        self.folder_label.pack(side=tk.LEFT, padx=10)

        choose_folder_btn = ttk.Button(folder_frame, text="בחר תיקייה", style='Modern.TButton', command=self.choose_folder)
        choose_folder_btn.pack(side=tk.RIGHT, padx=10)

    def _create_volume_section(self, parent):
        """Create volume control section."""
        volume_frame = ttk.LabelFrame(parent, text="עוצמת שמע", style='Modern.TLabelframe')
        volume_frame.pack(fill=tk.X, pady=10)

        self.volume_var = tk.DoubleVar(value=self.music_player.volume)
        volume_slider = tk.Scale(volume_frame, 
            from_=0, to=1, 
            orient=tk.HORIZONTAL, 
            resolution=0.01,
            variable=self.volume_var,
            command=self.update_volume,
            length=300)
        volume_slider.pack(padx=20, pady=10)

        self.volume_label = ttk.Label(volume_frame, text=f"{int(self.volume_var.get() * 100)}%", style='Modern.TLabel')
        self.volume_label.pack(pady=5)

    def _create_schedule_section(self, parent):
        # Schedule section frame
        schedule_frame = ttk.LabelFrame(parent, text="הוספת לוח זמנים", style="TLabelframe")
        schedule_frame.pack(padx=10, pady=10, fill="x")

        # Time input frame
        time_frame = ttk.Frame(schedule_frame)
        time_frame.pack(padx=10, pady=5, fill="x")

        # Hours input
        ttk.Label(time_frame, text="שעה:").pack(side="right", padx=(0, 5))
        hours_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=5, format="%02.0f")
        hours_spinbox.pack(side="right", padx=(0, 10))

        # Minutes input
        ttk.Label(time_frame, text="דקות:").pack(side="right", padx=(0, 5))
        minutes_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=5, format="%02.0f")
        minutes_spinbox.pack(side="right", padx=(0, 10))

        # Stop duration input
        ttk.Label(time_frame, text="עצירה אחרי (דקות):").pack(side="right", padx=(0, 5))
        stop_duration_spinbox = ttk.Spinbox(time_frame, from_=0, to=120, width=5, format="%03.0f")
        stop_duration_spinbox.pack(side="right", padx=(0, 10))

        # Days selection
        days_frame = ttk.Frame(schedule_frame)
        days_frame.pack(padx=10, pady=5, fill="x")

        days_label = ttk.Label(days_frame, text="ימים:")
        days_label.pack(side="right", padx=(0, 5))

        # Days checkbuttons with Hebrew names
        days = {
            "ראשון": "Sunday", 
            "שני": "Monday", 
            "שלישי": "Tuesday", 
            "רביעי": "Wednesday", 
            "חמישי": "Thursday", 
            "שישי": "Friday"
        }
        days_vars = {}
        for hebrew_day, english_day in days.items():
            days_vars[english_day] = tk.BooleanVar()
            day_check = ttk.Checkbutton(days_frame, text=hebrew_day, variable=days_vars[english_day])
            day_check.pack(side="right", padx=5)

        # Add schedule button
        add_schedule_btn = ttk.Button(
            schedule_frame, 
            text="הוסף לוח זמנים", 
            command=lambda: self.add_schedule(
                hours_spinbox.get(), 
                minutes_spinbox.get(), 
                stop_duration_spinbox.get(),
                days_vars
            )
        )
        add_schedule_btn.pack(padx=10, pady=10)

        # Schedules listbox
        schedules_frame = ttk.Frame(schedule_frame)
        schedules_frame.pack(padx=10, pady=5, fill="both", expand=True)

        schedules_label = ttk.Label(schedules_frame, text="לוחות זמנים:")
        schedules_label.pack()

        self.schedules_listbox = tk.Listbox(schedules_frame, height=5)
        self.schedules_listbox.pack(fill="both", expand=True)

        # Remove schedule button
        remove_schedule_btn = ttk.Button(
            schedule_frame, 
            text="הסר לוח זמנים", 
            command=self.remove_schedule
        )
        remove_schedule_btn.pack(padx=10, pady=10)

        # Stop music button
        stop_music_btn = ttk.Button(
            schedule_frame, 
            text="עצור מוזיקה", 
            command=self.stop_music
        )
        stop_music_btn.pack(padx=10, pady=10)

        return schedule_frame

    def choose_folder(self):
        """Open file dialog to choose music folder."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.music_player.load_playlist(folder_path)
            self.folder_label.config(text=folder_path)
            self.save_settings()

    def update_volume(self, *args):
        """Update music player volume."""
        volume = self.volume_var.get()
        self.music_player.set_volume(volume)
        self.volume_label.config(text=f"{int(volume * 100)}%")
        self.save_settings()

    def add_schedule(self, hours, minutes, stop_duration, days_vars):
        # Validate hours and minutes
        try:
            hours = int(hours)
            minutes = int(minutes)
            stop_duration = int(stop_duration)
            
            # Validate range
            if not (0 <= hours <= 23 and 0 <= minutes <= 59 and stop_duration >= 0):
                raise ValueError("Invalid time or duration range")
            
            # Format time string
            time_str = f"{hours:02d}:{minutes:02d}"
        except ValueError:
            messagebox.showerror("שגיאה", "אנא הזן שעה, זמן וזמן עצירה תקינים")
            return

        # Get selected days
        selected_days = [day for day, var in days_vars.items() if var.get()]

        # Check if a music folder is selected
        if self.folder_label.cget('text') == "לא נבחרה תיקייה":
            messagebox.showerror("שגיאה", "אנא בחר תיקיית מוזיקה לפני הוספת לוח זמנים")
            return

        # Add the schedule
        try:
            schedule_info = {
                'time': time_str, 
                'days': selected_days,
                'stop_duration': stop_duration
            }
            self.music_scheduler.add_schedule(time_str, selected_days, stop_duration)
            display_days = [day for day, var in days_vars.items() if var.get()]
            self.schedules_listbox.insert(tk.END, f"{time_str} - {', '.join(display_days)} (עצירה: {stop_duration} דקות)")
            self.save_settings()
            
            # Restart the scheduler to pick up the new schedule
            self.music_scheduler.stop()
            self.music_scheduler.start()
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת לוח זמנים: {str(e)}")

    def remove_schedule(self):
        """Remove selected schedule."""
        try:
            index = self.schedules_listbox.curselection()[0]
            self.schedules_listbox.delete(index)
            self.music_scheduler.remove_schedule(index)
            self.save_settings()
        except IndexError:
            messagebox.showerror("שגיאה", "אנא בחר לוח זמנים להסרה")

    def stop_music(self):
        """Stop music playback."""
        try:
            self.music_player.stop()
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בעצירת המוזיקה: {str(e)}")

    def load_settings(self):
        """Load application settings from file."""
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                
            # Restore volume
            volume = settings.get('volume', 0.7)
            self.volume_var.set(volume)
            self.music_player.set_volume(volume)

            # Restore music folder
            music_folder = settings.get('music_folder', '')
            if music_folder and os.path.exists(music_folder):
                self.folder_label.config(text=music_folder)
                try:
                    self.music_player.load_playlist(music_folder)
                except Exception as e:
                    messagebox.showwarning("אזהרה", f"לא ניתן לטעון את תיקיית המוזיקה: {str(e)}")

            # Restore schedules
            self.schedules_listbox.delete(0, tk.END)
            schedules = settings.get('schedules', [])
            for schedule in schedules:
                time_str = schedule.get('time', '')
                days = schedule.get('days', [])
                stop_duration = schedule.get('stop_duration', 0)
                if time_str:
                    self.music_scheduler.add_schedule(time_str, days, stop_duration)
                    self.schedules_listbox.insert(tk.END, f"{time_str} - {', '.join(days)} (עצירה: {stop_duration} דקות)")

            # Restart scheduler to apply loaded schedules
            self.music_scheduler.stop()
            self.music_scheduler.start()

        except FileNotFoundError:
            # First-time setup or no settings file
            pass
        except json.JSONDecodeError:
            messagebox.showerror("שגיאה", "קובץ ההגדרות פגום")

    def save_settings(self):
        """Save application settings to file."""
        try:
            settings = {
                'volume': self.volume_var.get(),
                'music_folder': self.folder_label.cget('text'),
                'schedules': [
                    {
                        'time': schedule['time'], 
                        'days': schedule['days'],
                        'stop_duration': schedule['stop_duration']
                    } for schedule in self.music_scheduler.get_schedules()
                ]
            }

            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בשמירת הגדרות: {str(e)}")

def main():
    root = tk.Tk()
    app = MusicSchedulerApp(root)
    
    def on_closing():
        # Stop the scheduler before closing
        app.music_scheduler.stop()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
