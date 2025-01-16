import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AppStyles:
    @staticmethod
    def configure_styles():
        """Configure modern, consistent styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')

        # Enhanced Soft Color Palette
        SOFT_THEME = {
            'primary': '#A7C7E7',     # Soft Pastel Blue
            'secondary': '#E6E6FA',   # Lavender
            'background': '#F0F4F8',  # Very Light Blue-Gray
            'text_primary': '#0D1321', # Very Dark Blue-Gray (Darker Text)
            'text_secondary': '#1A2B3C', # Slightly Lighter Dark Blue-Gray
            'accent': '#6B8E9F',      # Soft Muted Blue for accents
            'border': '#D1D8E0'       # Light Gray Border
        }

        # Custom Scrollbar Styling
        style.configure("Vertical.TScrollbar", 
            background=SOFT_THEME['secondary'],
            bordercolor=SOFT_THEME['border'],
            arrowcolor=SOFT_THEME['text_primary'],
            troughcolor=SOFT_THEME['background'])
        style.map("Vertical.TScrollbar",
            background=[('active', SOFT_THEME['accent'])])

        # Horizontal Scrollbar Styling
        style.configure("Horizontal.TScrollbar", 
            background=SOFT_THEME['secondary'],
            bordercolor=SOFT_THEME['border'],
            arrowcolor=SOFT_THEME['text_primary'],
            troughcolor=SOFT_THEME['background'])
        style.map("Horizontal.TScrollbar",
            background=[('active', SOFT_THEME['accent'])])

        # Enhanced Button Styles with Soft Shadows
        style.configure('Modern.TButton',
            font=('Segoe UI', 10, 'bold'),
            background=SOFT_THEME['primary'],
            foreground=SOFT_THEME['text_primary'],
            padding=(10, 6),
            borderwidth=1,
            relief='flat')
        
        style.map('Modern.TButton',
            background=[('active', SOFT_THEME['accent']), ('pressed', SOFT_THEME['secondary'])],
            foreground=[('active', SOFT_THEME['text_primary'])])

        # Label Styles with Enhanced Readability
        style.configure('Modern.TLabel',
            font=('Segoe UI', 10),
            background=SOFT_THEME['background'],
            foreground=SOFT_THEME['text_primary'])
        
        style.configure('Title.TLabel',
            font=('Segoe UI', 12, 'bold'),
            background=SOFT_THEME['background'],
            foreground=SOFT_THEME['text_secondary'],
            anchor='center',
            padding=8)

        # Day Label Specific Style
        style.configure('Day.TLabel',
            font=('Segoe UI', 10, 'bold'),
            background=SOFT_THEME['background'],
            foreground=SOFT_THEME['text_primary'])

        # Frame Styles
        style.configure('Modern.TFrame', 
            background=SOFT_THEME['background'])
        
        style.configure('ModernCard.TFrame', 
            background=SOFT_THEME['secondary'],
            relief='flat',
            borderwidth=1)

        # Checkbutton Styles with Modern Design
        style.configure('Custom.TCheckbutton',
            background=SOFT_THEME['background'],
            foreground=SOFT_THEME['text_primary'],
            font=('Segoe UI', 10),
            padding=5)
        
        style.map('Custom.TCheckbutton',
            background=[('selected', SOFT_THEME['primary'])],
            foreground=[('selected', SOFT_THEME['text_primary'])],
            indicatorbackground=[('selected', SOFT_THEME['accent'])],
            indicatorforeground=[('selected', 'white')])

        # LabelFrame Styles
        style.configure('Modern.TLabelframe',
            background=SOFT_THEME['secondary'],
            foreground=SOFT_THEME['text_primary'],
            font=('Helvetica', 12, 'bold'))
        
        style.configure('Modern.TLabelframe.Label',
            background=SOFT_THEME['secondary'],
            foreground=SOFT_THEME['text_primary'])

    @staticmethod
    def add_hover_effects(widget):
        """Add hover effects to buttons."""
        def on_enter(e):
            e.widget.configure(style='Modern.TButton')
            
        def on_leave(e):
            e.widget.configure(style='Modern.TButton')

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
