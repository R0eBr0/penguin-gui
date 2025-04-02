import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import math

def create_multiple_windows():
    windows = []
    window_targets = []
    window_creation_times = []  # Track when each window was created
    explosion_frames = []  # Store explosion animation frames
    
    root = tk.Tk()
    root.withdraw()
    
    # Load both GIFs
    gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gif.gif")
    explosion_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hi.gif")
    
    if not os.path.exists(gif_path) or not os.path.exists(explosion_path):
        messagebox.showerror("Error", "GIF files not found!")
        return
    
    # Load penguin GIF frames
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy()))
            gif.seek(len(frames))
    except EOFError:
        pass
    
    # Load explosion GIF frames
    explosion_gif = Image.open(explosion_path)
    try:
        while True:
            explosion_frames.append(ImageTk.PhotoImage(explosion_gif.copy()))
            explosion_gif.seek(len(explosion_frames))
    except EOFError:
        pass
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    def get_random_position():
        return (random.randint(0, screen_width - 100), random.randint(0, screen_height - 100))
    
    def update_window_positions():
        current_time = root.tk.call('clock', 'seconds')
        
        for idx, window in enumerate(windows):
            # Check if window should explode
            if current_time - window_creation_times[idx] >= 10 and not hasattr(window, 'exploding'):
                start_explosion(window, idx)
                continue
            
            if hasattr(window, 'exploding'):
                continue
                
            current_x = window.winfo_x()
            current_y = window.winfo_y()
            target_x, target_y = window_targets[idx]
            
            dx = (target_x - current_x) * 0.05
            dy = (target_y - current_y) * 0.05
            
            new_x = int(current_x + dx)
            new_y = int(current_y + dy)
            
            if abs(new_x - target_x) < 5 and abs(new_y - target_y) < 5 or random.random() < 0.01:
                window_targets[idx] = get_random_position()
            
            window.geometry(f"+{new_x}+{new_y}")
            window.lift()  # Keep window on top
            window.attributes('-topmost', 1)  # Ensure window stays on top
        
        root.after(20, update_window_positions)
    
    def start_explosion(window, idx):
        window.exploding = True
        window.lift()  # Keep explosion on top
        window.attributes('-topmost', 1)  # Ensure explosion stays on top
        label = window.children['!label']
        
        def play_explosion(frame_num=0):
            if frame_num >= len(explosion_frames):
                window.destroy()
                return
                
            label.configure(image=explosion_frames[frame_num])
            window.lift()  # Keep explosion on top during animation
            window.attributes('-topmost', 1)  # Ensure explosion stays on top during animation
            window.after(100, lambda: play_explosion(frame_num + 1))
        
        play_explosion()
    
    # Create display windows
    for i in range(40):
        window = tk.Toplevel()
        window.title(f"GIF Display {i+1}")
        window.overrideredirect(True)
        window.lift()  # Make window stay on top initially
        window.attributes('-topmost', 1)  # Ensure window stays on top initially
        
        label = tk.Label(window, image=frames[0])
        label.frames = frames
        label.pack()
        
        initial_pos = get_random_position()
        window.geometry(f"+{initial_pos[0]}+{initial_pos[1]}")
        windows.append(window)
        window_targets.append(get_random_position())
        window_creation_times.append(root.tk.call('clock', 'seconds'))
        
        def create_update_frame(window_label):
            def update_frame(frame_num=0):
                if not window_label.winfo_exists():
                    return
                frame = window_label.frames[frame_num]
                window_label.configure(image=frame)
                next_frame = (frame_num + 1) % len(window_label.frames)
                window_label.after(100, lambda: update_frame(next_frame))
            return update_frame
        
        update_frame = create_update_frame(label)
        update_frame()
    
    update_window_positions()
    root.mainloop()

if __name__ == "__main__":
    create_multiple_windows()