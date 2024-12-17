import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Scale
import schedule
import time
import os
import pygame
import random
from datetime import datetime
import json
from threading import Thread

class MusicSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("מתזמן המוזיקה")
        
        # Initialize days dictionary before creating GUI
        self.days = {
            'Sunday': tk.BooleanVar(),
            'Monday': tk.BooleanVar(),
            'Tuesday': tk.BooleanVar(),
            'Wednesday': tk.BooleanVar(),
            'Thursday': tk.BooleanVar(),
            'Friday': tk.BooleanVar(),
            'Saturday': tk.BooleanVar()
        }
        
        # הוספת משתנים חדשים לעיצוב
        self.custom_colors = {
            'slider_bg': '#2E3B4E',
            'slider_fg': '#4B7BE5',
            'time_bg': '#2E3B4E',
            'time_fg': '#E0E0E0',
            'spinbox_bg': '#1A1A2E',
            'spinbox_fg': '#E0E0E0',
            'frame_bg': '#1A1A2E'
        }
        
        # הוספת צבעים חדשים
        self.custom_colors.update({
            'checkbutton_selected': '#6C63FF',
            'checkbutton_bg': '#2E3B4E',
            'title_fg': '#FFFFFF',
            'volume_value_bg': '#4B7BE5'
        })
        
        # הגדרת גודל ומיקום החלון במרכז המסך
        window_width = 800
        window_height = 600  # Changed from 700 to 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Modern styling with gradient background
        gradient_frame = tk.Frame(self.root, bg='#1A1A2E')
        gradient_frame.place(relwidth=1, relheight=1)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern styles with hover effects
        style.configure('Modern.TButton',
            font=('Helvetica', 11, 'bold'),
            background='#4B7BE5',
            foreground='white',
            padding=10,
            borderwidth=0)
            
        style.map('Modern.TButton',
            background=[('active', '#6C63FF')],
            foreground=[('active', '#FFFFFF')])
            
        style.configure('Modern.TFrame',
            background='#1A1A2E')
            
        style.configure('Modern.TLabel',
            font=('Helvetica', 11),
            background='#1A1A2E',
            foreground='#E0E0E0')
            
        style.configure('Modern.TLabelframe',
            background='#16213E',
            foreground='#E0E0E0',
            font=('Helvetica', 12, 'bold'))
            
        style.configure('Modern.TLabelframe.Label',
            background='#16213E',
            foreground='#E0E0E0')
            
        # Configure Listbox colors
        self.listbox_colors = {
            'bg': '#16213E',
            'fg': '#E0E0E0',
            'selectbackground': '#4B7BE5',
            'selectforeground': 'white'
        }
        
        # Configure Volume Slider colors
        self.slider_colors = {
            'bg': '#16213E',
            'fg': '#4B7BE5',
            'troughcolor': '#2C3E50',
            'activebackground': '#6C63FF'
        }

        # אתחול pygame למוזיקה
        pygame.mixer.init()
        print("Pygame mixer initialized")
        
        # משתנים לשמירת הבחירות
        self.music_folder = ""
        self.selected_days = []
        self.schedules = []
        
        # עדכון הסגנונות
        style = ttk.Style()
        
        # הגדרת סגנון חדש לכותרות
        style.configure('Title.TLabel',
            font=('Helvetica', 14, 'bold'),
            background='#1A1A2E',
            foreground=self.custom_colors['title_fg'],
            anchor='center',
            padding=10)
            
        # סגנון חדש לצ'קבוטונים
        style.configure('Custom.TCheckbutton',
            background=self.custom_colors['checkbutton_bg'],
            foreground='white',
            font=('Helvetica', 10),
            padding=5)
            
        style.map('Custom.TCheckbutton',
            background=[('selected', self.custom_colors['checkbutton_selected'])],
            foreground=[('selected', 'white')])
            
        self.create_gui()
        self.load_settings()
    
    def create_gui(self):
        # Create main scrollable canvas
        main_canvas = tk.Canvas(self.root, bg='#1A1A2E')
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas, style='Modern.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # שימוש ב-grid במקום pack
        main_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # הגדרת משקולות לגריד
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Main frame configuration
        main_frame = ttk.Frame(scrollable_frame, style='Modern.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Update style configurations with more modern effects
        style = ttk.Style()
        style.configure('Modern.TFrame', background='#1A1A2E')
        style.configure('ModernCard.TFrame', 
            background='#232946',
            relief='raised',
            borderwidth=2)
        
        # Add gradient effects and shadows (using custom frame)
        class GradientFrame(tk.Frame):
            def __init__(self, parent, color1='#232946', color2='#2E3B4E', **kwargs):
                super().__init__(parent, **kwargs)
                self.bind('<Configure>', self._draw_gradient)
                self.color1 = color1
                self.color2 = color2

            def _draw_gradient(self, event=None):
                self.delete('gradient')
                width = self.winfo_width()
                height = self.winfo_height()
                limit = width
                (r1,g1,b1) = self.winfo_rgb(self.color1)
                (r2,g2,b2) = self.winfo_rgb(self.color2)
                r_ratio = float(r2-r1) / limit
                g_ratio = float(g2-g1) / limit
                b_ratio = float(b2-b1) / limit

                for i in range(limit):
                    nr = int(r1 + (r_ratio * i))
                    ng = int(g1 + (g_ratio * i))
                    nb = int(b1 + (b_ratio * i))
                    color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
                    self.create_line(i,0,i,height, tags=('gradient',), fill=color)
                self.lower('gradient')

        # Combine time, days, and volume in one container
        controls_frame = ttk.Frame(main_frame, style='ModernCard.TFrame')
        controls_frame.grid(row=3, column=0, pady=15, sticky='ew')
        controls_frame.grid_columnconfigure((0,1,2), weight=1)

        # Create the volume slider first
        self.volume_var = tk.DoubleVar(value=0.7)
        self.volume_slider = Scale(controls_frame,
            from_=0,
            to=1,
            orient='horizontal',
            resolution=0.01,
            variable=self.volume_var,
            command=self.update_volume,
            length=200,
            width=15,
            bg='#232946',
            fg='white',
            troughcolor='#4B7BE5',
            activebackground='#6C63FF',
            highlightthickness=0,
            font=('Helvetica', 10))

        # Then update its configuration
        self.volume_slider.configure(
            length=200,
            bg='#232946',
            troughcolor='#4B7BE5',
            activebackground='#6C63FF',
            highlightthickness=0)

        # Time selection frame
        time_frame = ttk.LabelFrame(controls_frame,
            text="בחירת שעה",
            style='Modern.TLabelframe',
            padding="10")
        time_frame.grid(row=0, column=0, padx=5, sticky='ew')

        # Days selection frame
        days_frame = ttk.LabelFrame(controls_frame,
            text="בחירת ימים",
            style='Modern.TLabelframe',
            padding="10")
        days_frame.grid(row=0, column=1, padx=5, sticky='ew')

        # Volume control frame
        volume_frame = ttk.LabelFrame(controls_frame,
            text="עוצמת שמע",
            style='Modern.TLabelframe',
            padding="10")
        volume_frame.grid(row=0, column=2, padx=5, sticky='ew')
        
        # Add volume slider to volume frame
        self.volume_slider.grid(row=0, column=0, padx=5, sticky='ew')
        
        # Volume label
        self.volume_label = ttk.Label(volume_frame,
            text="70%",
            style='Modern.TLabel',
            font=('Helvetica', 12, 'bold'))
        self.volume_label.grid(row=1, column=0, padx=5)

        # Add hover effects to frames
        for frame in [time_frame, days_frame, volume_frame]:
            frame.bind('<Enter>', lambda e: e.widget.configure(style='ModernHover.TLabelframe'))
            frame.bind('<Leave>', lambda e: e.widget.configure(style='Modern.TLabelframe'))

        # Update modern styles
        style.configure('ModernHover.TLabelframe',
            background='#2E3B4E',
            foreground='#FFFFFF')
        
        style.configure('Modern.TButton',
            font=('Helvetica', 11, 'bold'),
            background='#4B7BE5',
            foreground='white',
            padding=10,
            borderwidth=0)
        
        style.map('Modern.TButton',
            background=[('active', '#6C63FF'), ('hover', '#5A6FF0')],
            foreground=[('active', '#FFFFFF')])

        # Add subtle animations for buttons
        def on_enter(e):
            e.widget.configure(style='ModernHover.TButton')
            
        def on_leave(e):
            e.widget.configure(style='Modern.TButton')

        # Apply hover effects to all buttons
        for child in main_frame.winfo_children():
            if isinstance(child, ttk.Button):
                child.bind('<Enter>', on_enter)
                child.bind('<Leave>', on_leave)

        # Main frame configuration for center alignment
        main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Center all elements in main_frame
        main_frame.grid_columnconfigure(0, weight=1)
        
        # עדכון כותרת בחירת תיקייה
        folder_label = ttk.Label(main_frame, 
            text="בחירת תיקיית מוזיקה",
            style='Title.TLabel')
        folder_label.grid(row=0, column=0, pady=(0,10))
        
        # Folder selection with modern button
        folder_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        folder_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky='ew')
        
        ttk.Button(folder_frame, 
            text="בחר תיקיית מוזיקה",
            style='Modern.TButton',
            command=self.choose_folder).grid(row=0, column=1, padx=5)
            
        self.folder_label = ttk.Label(folder_frame,
            text="לא נבחרה תיקייה",
            style='Modern.TLabel',
            wraplength=300)
        self.folder_label.grid(row=0, column=0, padx=5)

        # Improved volume control
        volume_frame = ttk.LabelFrame(main_frame,
            text="עוצמת שמע",
            style='Modern.TLabelframe',
            padding="15")
        volume_frame.grid(row=2, column=0, pady=15, sticky='ew')
        
        volume_container = ttk.Frame(volume_frame, style='Modern.TFrame')
        volume_container.grid(row=0, column=0, sticky='ew')
        volume_frame.grid_columnconfigure(0, weight=1)
        
        self.volume_var = tk.DoubleVar(value=0.7)
        self.volume_slider = Scale(volume_container,
            from_=0,
            to=1,
            orient='horizontal',
            resolution=0.01,
            variable=self.volume_var,
            command=self.update_volume,
            bg=self.custom_colors['slider_bg'],
            fg='white',
            troughcolor=self.custom_colors['volume_value_bg'],
            activebackground=self.custom_colors['slider_fg'],
            highlightthickness=0,
            sliderrelief='raised',
            sliderlength=30,
            length=300,
            width=15,
            font=('Helvetica', 10))
        self.volume_slider.grid(row=0, column=0, padx=20, sticky='ew')
        
        # תווית לערך הווליום
        self.volume_label = ttk.Label(volume_container,
            text="70%",
            style='Modern.TLabel',
            font=('Helvetica', 12, 'bold'))
        self.volume_label.grid(row=0, column=1, padx=(5,20))
        
        # Create a container frame for time and days
        time_days_container = ttk.Frame(main_frame, style='Modern.TFrame')
        time_days_container.grid(row=3, column=0, pady=15, sticky='ew')
        time_days_container.grid_columnconfigure(0, weight=1)
        time_days_container.grid_columnconfigure(1, weight=1)

        # Improved time selection
        time_frame = ttk.LabelFrame(time_days_container,
            text="בחירת שעה",
            style='Modern.TLabelframe',
            padding="15")
        time_frame.grid(row=0, column=0, pady=15, padx=5, sticky='ew')
        
        time_container = ttk.Frame(time_frame, style='Modern.TFrame')
        time_container.grid(row=0, column=0, padx=20)
        time_frame.grid_columnconfigure(0, weight=1)
        
        # Custom spinbox style
        spinbox_style = {
            'width': 8,
            'font': ('Helvetica', 16),
            'justify': 'center',
            'bg': self.custom_colors['spinbox_bg'],
            'fg': self.custom_colors['spinbox_fg'],
            'buttonbackground': self.custom_colors['slider_fg'],
            'relief': 'flat',
            'highlightthickness': 1,
            'highlightcolor': self.custom_colors['slider_fg'],
            'highlightbackground': self.custom_colors['slider_fg']
        }
        
        self.hour_var = tk.StringVar(value="00")
        hour_spinbox = tk.Spinbox(time_container,
            from_=0,
            to=23,
            textvariable=self.hour_var,
            wrap=True,
            **spinbox_style)
        hour_spinbox.grid(row=0, column=0, padx=5)
        
        separator_label = ttk.Label(time_container,
            text=":",
            style='Modern.TLabel',
            font=('Helvetica', 20, 'bold'))
        separator_label.grid(row=0, column=1, padx=5)
        
        self.minute_var = tk.StringVar(value="00")
        minute_spinbox = tk.Spinbox(time_container,
            from_=0,
            to=59,
            textvariable=self.minute_var,
            wrap=True,
            **spinbox_style)
        minute_spinbox.grid(row=0, column=2, padx=5)
        
        # Format spinbox values
        def format_time(var):
            try:
                value = int(var.get())
                var.set(f"{value:02d}")
            except ValueError:
                var.set("00")
                
        self.hour_var.trace('w', lambda *args: format_time(self.hour_var))
        self.minute_var.trace('w', lambda *args: format_time(self.minute_var))

        # בחירת ימים - עיצוב מחדש
        days_frame = ttk.LabelFrame(time_days_container,
            text="בחירת ימים",
            style='Modern.TLabelframe',
            padding="10")
        days_frame.grid(row=0, column=1, pady=15, padx=5, sticky='ew')
        
        days_container = ttk.Frame(days_frame, style='Modern.TFrame')
        days_container.grid(row=0, column=0)
        days_frame.grid_columnconfigure(0, weight=1)
        
        day_names_hebrew = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ש']  # קיצור שמות הימים
        day_names_english = list(self.days.keys())
        
        # יצירת שני טורים של צ'קבוקסים
        for i, (day_eng, day_heb) in enumerate(zip(day_names_english, day_names_hebrew)):
            col = i % 4
            row = i // 4
            cb = ttk.Checkbutton(days_container,
                text=f"יום {day_heb}",
                variable=self.days[day_eng],
                style='Custom.TCheckbutton',
                command=lambda d=day_eng: self.update_day_selection(d))
            cb.grid(row=row, column=col, padx=10, pady=2)
        
        # כפתורי פעולה
        action_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        action_frame.grid(row=5, column=0, pady=15, sticky='ew')
        
        # מרכוז כפתורי הפעולה
        action_frame.grid_columnconfigure(tuple(range(5)), weight=1)
        
        ttk.Button(action_frame, text="הוסף תזמון", command=self.add_schedule, style='Modern.TButton').grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="שמור הגדרות", command=self.save_settings, style='Modern.TButton').grid(row=0, column=0, padx=5)
        
        # כפתור בדיקה
        ttk.Button(action_frame, text="הפעל שיר לבדיקה", command=self.test_play, style='Modern.TButton').grid(row=0, column=2, padx=5)
        ttk.Button(action_frame, text="כבה מוזיקה", command=self.stop_music, style='Modern.TButton').grid(row=0, column=3, padx=5)
        
        # Add shuffle button
        ttk.Button(action_frame,
            text="ערבב והשמע",
            style='Modern.TButton',
            command=self.shuffle_and_play).grid(row=0, column=4, padx=5)

        # Update listbox style and height
        self.schedule_listbox = tk.Listbox(main_frame,
            height=6,  # Reduced from 8 to 6
            bg=self.listbox_colors['bg'],
            fg=self.listbox_colors['fg'],
            selectbackground=self.listbox_colors['selectbackground'],
            selectforeground=self.listbox_colors['selectforeground'],
            selectmode='single',
            font=('Helvetica', 11),
            relief='flat',
            borderwidth=0)
        self.schedule_listbox.grid(row=6, column=0, sticky='ew', pady=10)  # Reduced pady from 15 to 10
        
        # כפתור הסרה
        ttk.Button(main_frame, text="הסר תזמון נבחר", command=self.remove_schedule, style='Modern.TButton').grid(row=7, column=0, pady=10)
        
        # תווית סטטוס
        self.status_label = ttk.Label(main_frame, text="מוכן", style='Modern.TLabel', wraplength=300)
        self.status_label.grid(row=8, column=0, pady=5)
        
        # תווית דיבאג
        self.debug_label = ttk.Label(main_frame, text="", style='Modern.TLabel', wraplength=300)
        self.debug_label.grid(row=9, column=0, pady=5)

        # Add hover effect to buttons
        def on_enter(e):
            e.widget.configure(background='#6C63FF')
            
        def on_leave(e):
            e.widget.configure(background='#4B7BE5')
            
        for child in action_frame.winfo_children():
            if isinstance(child, ttk.Button):
                child.bind('<Enter>', on_enter)
                child.bind('<Leave>', on_leave)

    def test_play(self):
        """פונקציה לבדיקת ניגון מוזיקה"""
        if not self.music_folder:
            messagebox.showerror("שגיאה", "נא לבחור תיקיית מוזיקה")
            return
            
        try:
            music_files = [f for f in os.listdir(self.music_folder) 
                          if f.endswith(('.mp3', '.wav'))]
            if music_files:
                music_file = os.path.join(self.music_folder, random.choice(music_files))
                print(f"Playing test file: {music_file}")
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play()
                self.status_label.config(text=f"מנגן: {os.path.basename(music_file)}")
            else:
                messagebox.showerror("שגיאה", "לא נמצאו קבצי מוזיקה בתיקייה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהפעלת המוזיקה: {str(e)}")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.music_folder = folder
            self.folder_label.config(text=self.music_folder)
            print(f"Selected folder: {folder}")
            # בדיקת קבצי מוזיקה בתיקייה
            music_files = [f for f in os.listdir(folder) if f.endswith(('.mp3', '.wav'))]
            print(f"Found {len(music_files)} music files")

    def add_schedule(self):
        if not self.music_folder:
            messagebox.showerror("שגיאה", "נא לבחור תיקיית מוזיקה")
            return
            
        selected_days = [day for day, var in self.days.items() if var.get()]
        if not selected_days:
            messagebox.showerror("שגיאה", "נא לבחור לפחות יום אחד")
            return
            
        time_str = f"{int(self.hour_var.get()):02d}:{int(self.minute_var.get()):02d}"
        schedule_info = {
            'time': time_str,
            'days': selected_days,
            'folder': self.music_folder,
            'volume': self.volume_var.get()  # Add volume to the schedule info
        }
        
        print(f"Adding schedule: {schedule_info}")
        self.schedules.append(schedule_info)
        self.update_schedule_display()
        self.setup_schedule(schedule_info)
        self.save_settings()

    def update_schedule_display(self):
        self.schedule_listbox.delete(0, tk.END)
        for s in self.schedules:
            days_str = ', '.join(s['days'])
            volume_percent = int(s.get('volume', 0.7) * 100)  # Default to 70% if not set
            self.schedule_listbox.insert(tk.END, f"{s['time']} - {days_str} (עוצמה: {volume_percent}%)")

    def remove_schedule(self):
        selection = self.schedule_listbox.curselection()
        if selection:
            index = selection[0]
            del self.schedules[index]
            self.update_schedule_display()
            self.save_settings()

    def save_settings(self):
        settings = {
            'schedules': self.schedules
        }
        try:
            with open('music_scheduler_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False)
            print("Settings saved successfully")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בשמירת ההגדרות: {str(e)}")

    def load_settings(self):
        try:
            with open('music_scheduler_settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.schedules = settings.get('schedules', [])
                self.update_schedule_display()
                for schedule_info in self.schedules:
                    self.setup_schedule(schedule_info)
            print("Settings loaded successfully")
        except FileNotFoundError:
            print("No settings file found")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בטעינת ההגדרות: {str(e)}")

    def setup_schedule(self, schedule_info):
        def play_music():
            current_day = datetime.now().strftime('%A')
            print(f"Current day: {current_day}")
            print(f"Scheduled days: {schedule_info['days']}")
            if current_day in schedule_info['days']:
                try:
                    # Set the volume for this schedule
                    volume = schedule_info.get('volume', 0.7)  # Default to 0.7 if not set
                    pygame.mixer.music.set_volume(volume)
                    
                    music_files = [f for f in os.listdir(schedule_info['folder']) 
                                 if f.endswith(('.mp3', '.wav'))]
                    print(f"Found {len(music_files)} music files")
                    if music_files:
                        self.music_files = music_files
                        self.current_music_index = 0
                        self.play_next_song(schedule_info['folder'])
                    else:
                        print("No music files found")
                        self.status_label.config(text="לא נמצאו קבצי מוזיקה")
                except Exception as e:
                    print(f"Error playing music: {str(e)}")
                    self.status_label.config(text=f"שגיאה: {str(e)}")
            else:
                print("Not scheduled for today")
        
        print(f"Setting up schedule for {schedule_info['time']}")
        schedule.every().day.at(schedule_info['time']).do(play_music)

    def run_scheduler(self):
        while True:
            try:
                current_time = datetime.now().strftime('%H:%M')
                schedule.run_pending()
                self.debug_label.config(text=f"זמן נוכחי: {current_time}")
                time.sleep(1)
            except Exception as e:
                print(f"Error in scheduler: {str(e)}")
                self.debug_label.config(text=f"שגיאה: {str(e)}")

    def stop_music(self):
        """Function to stop the music"""
        pygame.mixer.music.stop()
        self.status_label.config(text="המוזיקה הופסקה")

    def update_volume(self, *args):
        """עדכון תווית הווליום והעוצמה"""
        volume = self.volume_var.get()
        pygame.mixer.music.set_volume(volume)
        self.volume_label.config(text=f"{int(volume * 100)}%")

    def shuffle_and_play(self):
        """Function to shuffle and play music"""
        if not self.music_folder:
            messagebox.showerror("שגיאה", "נא לבחור תיקיית מוזיקה")
            return
            
        try:
            music_files = [f for f in os.listdir(self.music_folder) 
                          if f.endswith(('.mp3', '.wav'))]
            if music_files:
                random.shuffle(music_files)
                self.music_files = music_files
                self.current_music_index = 0
                self.play_next_song(self.music_folder)
            else:
                messagebox.showerror("שגיאה", "לא נמצאו קבצי מוזיקה בתיקייה")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה בהפעלת המוזיקה: {str(e)}")

    def play_next_song(self, folder):
        """Function to play the next song in the list"""
        if self.current_music_index < len(self.music_files):
            music_file = os.path.join(folder, self.music_files[self.current_music_index])
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()
            self.status_label.config(text=f"מנגן: {os.path.basename(music_file)}")
            self.current_music_index += 1
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            pygame.event.clear()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        self.play_next_song(folder)
                        return
                time.sleep(0.1)
        else:
            self.status_label.config(text="סיימנו לנגן את כל השירים")

    def update_day_selection(self, day):
        """עדכון חיווי ויזואלי לבחירת יום"""
        is_selected = self.days[day].get()
        # עדכון הסטטוס בר עם הימים שנבחרו
        selected_days = [day_heb for day_eng, var in self.days.items() 
                        if var.get()]
        if (selected_days):
            self.status_label.config(
                text=f"ימים נבחרים: {', '.join(selected_days)}")
        else:
            self.status_label.config(text="לא נבחרו ימים")

def main():
    root = tk.Tk()
    app = MusicSchedulerApp(root)
    
    # הפעלת הדפדפן בתהליכון נפרד
    scheduler_thread = Thread(target=app.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()
