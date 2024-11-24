import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
        self.root.geometry("600x450")  # הגדלתי מעט את החלון
        
        # הגדרת כיוון טקסט מימין לשמאל
        self.root.tk_setPalette(background='#f0f0f0')
        
        # אתחול pygame למוזיקה
        pygame.mixer.init()
        print("Pygame mixer initialized")
        
        # משתנים לשמירת הבחירות
        self.music_folder = ""
        self.selected_days = []
        self.schedules = []
        
        self.create_gui()
        self.load_settings()
    
    def create_gui(self):
        # מסגרת ראשית
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # כפתור בחירת תיקייה
        ttk.Button(main_frame, text="בחר תיקיית מוזיקה", command=self.choose_folder).grid(row=0, column=1, pady=5)
        self.folder_label = ttk.Label(main_frame, text="לא נבחרה תיקייה", wraplength=300)
        self.folder_label.grid(row=0, column=0, pady=5)
        
        # בחירת שעה
        time_frame = ttk.LabelFrame(main_frame, text="בחירת שעה", padding="5")
        time_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.hour_var = tk.StringVar(value="00")
        self.minute_var = tk.StringVar(value="00")
        
        ttk.Spinbox(time_frame, from_=0, to=23, width=5, textvariable=self.hour_var).grid(row=0, column=1)
        ttk.Label(time_frame, text=":").grid(row=0, column=2)
        ttk.Spinbox(time_frame, from_=0, to=59, width=5, textvariable=self.minute_var).grid(row=0, column=3)
        
        # בחירת ימים
        days_frame = ttk.LabelFrame(main_frame, text="בחירת ימים", padding="5")
        days_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.days = {
            'Sunday': tk.BooleanVar(),    # שיניתי לאנגלית כי זה מה שדרוש להשוואה
            'Monday': tk.BooleanVar(),
            'Tuesday': tk.BooleanVar(),
            'Wednesday': tk.BooleanVar(),
            'Thursday': tk.BooleanVar(),
            'Friday': tk.BooleanVar(),
            'Saturday': tk.BooleanVar()
        }
        
        day_names_hebrew = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת']
        day_names_english = list(self.days.keys())
        
        for i, (day_eng, day_heb) in enumerate(zip(day_names_english, day_names_hebrew)):
            ttk.Checkbutton(days_frame, text=day_heb, variable=self.days[day_eng]).grid(row=0, column=i, padx=5)
        
        # כפתורי פעולה
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(action_frame, text="הוסף תזמון", command=self.add_schedule).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="שמור הגדרות", command=self.save_settings).grid(row=0, column=0, padx=5)
        
        # כפתור בדיקה
        ttk.Button(action_frame, text="הפעל שיר לבדיקה", command=self.test_play).grid(row=0, column=2, padx=5)
        
        # רשימת תזמונים
        self.schedule_listbox = tk.Listbox(main_frame, height=5)
        self.schedule_listbox.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # כפתור הסרה
        ttk.Button(main_frame, text="הסר תזמון נבחר", command=self.remove_schedule).grid(row=5, column=0, columnspan=2, pady=5)
        
        # תווית סטטוס
        self.status_label = ttk.Label(main_frame, text="מוכן", wraplength=300)
        self.status_label.grid(row=6, column=0, columnspan=2, pady=5)
        
        # תווית דיבאג
        self.debug_label = ttk.Label(main_frame, text="", wraplength=300)
        self.debug_label.grid(row=7, column=0, columnspan=2, pady=5)

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
            'folder': self.music_folder
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
            self.schedule_listbox.insert(tk.END, f"{s['time']} - {days_str}")

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
                    music_files = [f for f in os.listdir(schedule_info['folder']) 
                                 if f.endswith(('.mp3', '.wav'))]
                    print(f"Found {len(music_files)} music files")
                    if music_files:
                        music_file = os.path.join(schedule_info['folder'], 
                                                random.choice(music_files))
                        print(f"Playing: {music_file}")
                        pygame.mixer.music.load(music_file)
                        pygame.mixer.music.play()
                        self.status_label.config(text=f"מנגן: {os.path.basename(music_file)}")
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

def main():
    root = tk.Tk()
    app = MusicSchedulerApp(root)
    
    # הפעלת הדפדפן בתהליכון נפרד
    scheduler_thread = Thread(target=app.run_scheduler, daemon=True)
    scheduler_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()