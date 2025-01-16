import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AppStyles:
    # Modern Color Palette with Gradient Effects
    SOFT_THEME = {
        'primary': '#4158D0',      # Vibrant Blue
        'secondary': '#C850C0',    # Bright Purple
        'gradient_start': '#4158D0',
        'gradient_end': '#C850C0',
        'background': '#F8F9FD',   # Light Background
        'text_primary': '#2A2A72',  # Deep Blue Text
        'text_secondary': '#4A4A8A', # Lighter Blue Text
        'accent': '#FF4B91',       # Pink Accent
        'border': '#E2E8F0',      # Soft Border
        'hover': '#3B49B8',       # Darker Blue for hover
        'disabled': '#CBD5E0',    # Light Gray for disabled
        'success': '#48BB78',     # Green
        'error': '#F56565'        # Red
    }

    @staticmethod
    def configure_styles():
        """Configure modern, consistent styles for the application."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure ttk styles with rounded corners and gradients
        style.configure("TFrame", background=AppStyles.SOFT_THEME['background'])
        
        # Modern Label Frame with rounded corners
        style.configure("Modern.TLabelframe", 
            background=AppStyles.SOFT_THEME['background'],
            bordercolor=AppStyles.SOFT_THEME['border'],
            relief="flat",
            borderwidth=2)
        style.configure("Modern.TLabelframe.Label", 
            foreground=AppStyles.SOFT_THEME['text_primary'],
            background=AppStyles.SOFT_THEME['background'],
            font=('Segoe UI', 10, 'bold'))

        # Enhanced Button Style
        style.configure('Modern.TButton',
            font=('Segoe UI', 10),
            background=AppStyles.SOFT_THEME['primary'],
            foreground='white',
            bordercolor=AppStyles.SOFT_THEME['border'],
            relief="flat",
            padding=(20, 10))
        style.map('Modern.TButton',
            background=[('active', AppStyles.SOFT_THEME['hover']),
                       ('disabled', AppStyles.SOFT_THEME['disabled'])],
            foreground=[('disabled', AppStyles.SOFT_THEME['text_secondary'])])

        # Modern Entry Style
        style.configure('Modern.TEntry',
            fieldbackground='white',
            bordercolor=AppStyles.SOFT_THEME['border'],
            lightcolor=AppStyles.SOFT_THEME['border'],
            darkcolor=AppStyles.SOFT_THEME['border'],
            borderwidth=1,
            relief="solid",
            padding=5)

        # Combobox with rounded corners
        style.configure('Modern.TCombobox',
            background='white',
            fieldbackground='white',
            selectbackground=AppStyles.SOFT_THEME['primary'],
            selectforeground='white',
            bordercolor=AppStyles.SOFT_THEME['border'],
            arrowcolor=AppStyles.SOFT_THEME['primary'],
            padding=5)
        
        # Scale (Slider) with modern look
        style.configure('Modern.Horizontal.TScale',
            background=AppStyles.SOFT_THEME['background'],
            troughcolor=AppStyles.SOFT_THEME['border'],
            bordercolor=AppStyles.SOFT_THEME['border'],
            lightcolor=AppStyles.SOFT_THEME['primary'],
            darkcolor=AppStyles.SOFT_THEME['primary'])

        # Checkbutton with custom color
        style.configure('Modern.TCheckbutton',
            background=AppStyles.SOFT_THEME['background'],
            foreground=AppStyles.SOFT_THEME['text_primary'],
            focuscolor=AppStyles.SOFT_THEME['primary'])
        style.map('Modern.TCheckbutton',
            background=[('active', AppStyles.SOFT_THEME['background'])],
            foreground=[('disabled', AppStyles.SOFT_THEME['disabled'])])

        # Scrollbar with rounded design
        style.configure("Modern.Vertical.TScrollbar",
            background=AppStyles.SOFT_THEME['primary'],
            bordercolor=AppStyles.SOFT_THEME['border'],
            arrowcolor='white',
            troughcolor=AppStyles.SOFT_THEME['background'],
            relief="flat",
            width=12)
        style.map("Modern.Vertical.TScrollbar",
            background=[('active', AppStyles.SOFT_THEME['hover']),
                       ('pressed', AppStyles.SOFT_THEME['hover'])])

        # Label Styles with Enhanced Readability
        style.configure('Modern.TLabel',
            font=('Segoe UI', 10),
            background=AppStyles.SOFT_THEME['background'],
            foreground=AppStyles.SOFT_THEME['text_primary'])
        
        style.configure('Title.TLabel',
            font=('Segoe UI', 12, 'bold'),
            background=AppStyles.SOFT_THEME['background'],
            foreground=AppStyles.SOFT_THEME['text_secondary'],
            anchor='center',
            padding=8)

        # Day Label Specific Style
        style.configure('Day.TLabel',
            font=('Segoe UI', 10, 'bold'),
            background=AppStyles.SOFT_THEME['background'],
            foreground=AppStyles.SOFT_THEME['text_primary'])

        # Frame Styles
        style.configure('Modern.TFrame', 
            background=AppStyles.SOFT_THEME['background'])
        
        style.configure('ModernCard.TFrame', 
            background=AppStyles.SOFT_THEME['secondary'],
            relief='flat',
            borderwidth=1)

    @staticmethod
    def add_hover_effects(widget):
        """Add hover effects to buttons."""
        def on_enter(e):
            e.widget.configure(style='Modern.TButton')
            
        def on_leave(e):
            e.widget.configure(style='Modern.TButton')

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
