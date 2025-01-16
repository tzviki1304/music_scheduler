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
        """Create the main GUI elements with a modern layout."""
        # Create main container with padding
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas with scrollbar
        canvas = tk.Canvas(main_frame, bg=AppStyles.SOFT_THEME['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style='Modern.Vertical.TScrollbar')
        
        # Create scrollable frame
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Add scrollable frame to canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)

        # Add mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Configure canvas resize
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width-4)  # -4 for padding
        canvas.bind("<Configure>", _on_canvas_configure)

        # File selection section
        file_frame = ttk.LabelFrame(scrollable_frame, text="בחירת תיקייה", style='Modern.TLabelframe')
        file_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        self.file_path_var = tk.StringVar()
        path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, style='Modern.TEntry')
        path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        
        browse_button = ttk.Button(file_frame, text="בחר תיקייה", 
                                 command=self.browse_directory, style='Modern.TButton')
        browse_button.pack(side="right", padx=(5, 10), pady=10)
        
        # Volume control with modern slider
        volume_frame = ttk.LabelFrame(scrollable_frame, text="עוצמת שמע", style='Modern.TLabelframe')
        volume_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        self.volume_var = tk.DoubleVar(value=70)
        volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                variable=self.volume_var, command=self.update_volume,
                                style='Modern.Horizontal.TScale')
        volume_slider.pack(fill="x", padx=10, pady=10)
        
        # Schedule controls
        schedule_frame = ttk.LabelFrame(scrollable_frame, text="הוספת לוח זמנים", style='Modern.TLabelframe')
        schedule_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        time_frame = ttk.Frame(schedule_frame, style='Modern.TFrame')
        time_frame.pack(fill="x", padx=10, pady=5)
        
        # Start time selection
        start_time_frame = ttk.Frame(time_frame, style='Modern.TFrame')
        start_time_frame.pack(side="left", padx=5)
        
        ttk.Label(start_time_frame, text="שעת התחלה:", style='Modern.TLabel').pack(side="left", padx=5)
        
        self.hour_var = tk.StringVar()
        hour_combo = ttk.Combobox(start_time_frame, textvariable=self.hour_var, width=3, 
                                values=[f"{i:02d}" for i in range(24)], style='Modern.TCombobox')
        hour_combo.pack(side="left", padx=2)
        
        ttk.Label(start_time_frame, text=":", style='Modern.TLabel').pack(side="left")
        
        self.minute_var = tk.StringVar()
        minute_combo = ttk.Combobox(start_time_frame, textvariable=self.minute_var, width=3,
                                  values=[f"{i:02d}" for i in range(60)], style='Modern.TCombobox')
        minute_combo.pack(side="left", padx=2)

        # End time selection
        end_time_frame = ttk.Frame(time_frame, style='Modern.TFrame')
        end_time_frame.pack(side="left", padx=20)
        
        ttk.Label(end_time_frame, text="זמן סיום (דקות):", style='Modern.TLabel').pack(side="left", padx=5)
        
        self.duration_var = tk.StringVar(value="60")
        duration_combo = ttk.Combobox(end_time_frame, textvariable=self.duration_var, width=4,
                                    values=[str(i) for i in range(0, 181, 15)], style='Modern.TCombobox')
        duration_combo.pack(side="left", padx=2)
        
        # Days selection with modern checkboxes
        days_frame = ttk.Frame(schedule_frame, style='Modern.TFrame')
        days_frame.pack(fill="x", padx=10, pady=10)
        
        self.day_vars = {day: tk.BooleanVar() for day in ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי']}
        for day, var in self.day_vars.items():
            ttk.Checkbutton(days_frame, text=day, variable=var, style='Modern.TCheckbutton').pack(side="right", padx=5)
        
        # Add schedule button
        add_button = ttk.Button(schedule_frame, text="הוסף לוח זמנים", 
                              command=self.add_schedule, style='Modern.TButton')
        add_button.pack(pady=10)
        
        # Schedule list with modern styling
        list_frame = ttk.LabelFrame(scrollable_frame, text="לוחות זמנים", style='Modern.TLabelframe')
        list_frame.pack(fill="both", expand=True, pady=(0, 20), padx=20)
        
        self.schedule_list = tk.Text(list_frame, height=10, wrap=tk.WORD,
                                   font=('Segoe UI', 10),
                                   bg='white',
                                   relief="flat",
                                   padx=10,
                                   pady=10)
        self.schedule_list.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        list_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                     command=self.schedule_list.yview,
                                     style='Modern.Vertical.TScrollbar')
        list_scrollbar.pack(side="right", fill="y")
        self.schedule_list.configure(yscrollcommand=list_scrollbar.set)
        
        # Control buttons
        button_frame = ttk.Frame(scrollable_frame, style='Modern.TFrame')
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        remove_button = ttk.Button(button_frame, text="הסר לוח זמנים",
                                 command=self.remove_schedule, style='Modern.TButton')
        remove_button.pack(side="left", padx=5)
        
        save_button = ttk.Button(button_frame, text="עבור מוזיקה",
                               command=self.save_settings, style='Modern.TButton')
        save_button.pack(side="right", padx=5)

    def browse_directory(self):
        """Open file dialog to choose music folder."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.music_player.load_playlist(folder_path)
            self.file_path_var.set(folder_path)
            self.save_settings()

    def update_volume(self, *args):
        """Update music player volume."""
        volume = self.volume_var.get()
        self.music_player.set_volume(volume)
        self.save_settings()

    def add_schedule(self):
        # Validate hours and minutes
        try:
            hours = int(self.hour_var.get())
            minutes = int(self.minute_var.get())
            
            # Validate range
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                raise ValueError("Invalid time range")
            
            # Format time string
            time_str = f"{hours:02d}:{minutes:02d}"
        except ValueError:
            messagebox.showerror("שגיאה", "אנא הזן שעה ודקות תקינים")
            return

        # Get selected days
        selected_days = [day for day, var in self.day_vars.items() if var.get()]

        # Check if a music folder is selected
        if self.file_path_var.get() == "":
            messagebox.showerror("שגיאה", "אנא בחר תיקיית מוזיקה לפני הוספת לוח זמנים")
            return

        # Add the schedule
        try:
            schedule_info = {
                'time': time_str, 
                'days': selected_days,
                'stop_duration': int(self.duration_var.get())
            }
            self.music_scheduler.add_schedule(time_str, selected_days, int(self.duration_var.get()))
            display_days = [day for day, var in self.day_vars.items() if var.get()]
            self.schedule_list.insert(tk.END, f"{time_str} - {', '.join(display_days)}\n")
            self.save_settings()
            
            # Restart the scheduler to pick up the new schedule
            self.music_scheduler.stop()
            self.music_scheduler.start()
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהוספת לוח זמנים: {str(e)}")

    def remove_schedule(self):
        """Remove selected schedule."""
        try:
            self.schedule_list.delete('1.0', tk.END)
            self.music_scheduler.remove_schedule(0)
            self.save_settings()
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהסרת לוח זמנים: {str(e)}")

    def save_settings(self):
        """Save application settings to file."""
        try:
            settings = {
                'volume': self.volume_var.get(),
                'music_folder': self.file_path_var.get(),
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
                self.file_path_var.set(music_folder)
                try:
                    self.music_player.load_playlist(music_folder)
                except Exception as e:
                    messagebox.showwarning("אזהרה", f"לא ניתן לטעון את תיקיית המוזיקה: {str(e)}")

            # Restore schedules
            self.schedule_list.delete('1.0', tk.END)
            schedules = settings.get('schedules', [])
            for schedule in schedules:
                time_str = schedule.get('time', '')
                days = schedule.get('days', [])
                stop_duration = schedule.get('stop_duration', 0)
                if time_str:
                    self.music_scheduler.add_schedule(time_str, days, stop_duration)
                    self.schedule_list.insert(tk.END, f"{time_str} - {', '.join(days)}\n")

            # Restart scheduler to apply loaded schedules
            self.music_scheduler.stop()
            self.music_scheduler.start()

        except FileNotFoundError:
            # First-time setup or no settings file
            pass
        except json.JSONDecodeError:
            messagebox.showerror("שגיאה", "קובץ ההגדרות פגום")

def main():
    root = tk.Tk()
    app = MusicSchedulerApp(root)
    
    def on_closing():
        # Stop the scheduler before closing
        app.music_scheduler.stop()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
