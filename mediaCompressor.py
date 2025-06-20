import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image
import threading
from pathlib import Path

class MediaCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Compressor")
        self.root.geometry("400x350")
        self.root.minsize(350, 250)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.compression_level = tk.StringVar(value="medium")
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame with grid layout
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # File selection
        self.create_file_section(main_frame, 0)
        
        # Compression settings
        self.create_settings_section(main_frame, 1)
        
        # File info
        self.create_info_section(main_frame, 2)
        
        # Progress and controls
        self.create_progress_controls(main_frame, 3)
        
    def create_file_section(self, parent, row):
        file_frame = ttk.LabelFrame(parent, text="File Selection", padding=5)
        file_frame.grid(row=row, column=0, sticky="ew", pady=5)
        file_frame.columnconfigure(1, weight=1)
        
        # Input file
        ttk.Label(file_frame, text="Input:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.input_entry = ttk.Entry(file_frame, textvariable=self.input_file, state="readonly")
        self.input_entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        ttk.Button(file_frame, text="Browse", command=self.select_input_file, bootstyle=PRIMARY).grid(row=0, column=2)
        
        # Output file
        ttk.Label(file_frame, text="Output:").grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(5, 0))
        self.output_entry = ttk.Entry(file_frame, textvariable=self.output_file, state="readonly")
        self.output_entry.grid(row=1, column=1, sticky="ew", padx=(0, 5), pady=(5, 0))
        ttk.Button(file_frame, text="Save As", command=self.select_output_file, bootstyle=SUCCESS).grid(row=1, column=2, pady=(5, 0))
        
    def create_settings_section(self, parent, row):
        settings_frame = ttk.LabelFrame(parent, text="Compression Settings", padding=5)
        settings_frame.grid(row=row, column=0, sticky="ew", pady=5)
        settings_frame.columnconfigure(1, weight=1)
        
        ttk.Label(settings_frame, text="Level:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        levels = ["low", "medium", "high"]
        self.compression_combo = ttk.Combobox(settings_frame, textvariable=self.compression_level, values=levels, state="readonly", width=15)
        self.compression_combo.grid(row=0, column=1, sticky="ew")
        
    def create_info_section(self, parent, row):
        self.info_text = ttk.Text(parent, height=3, wrap="word", state="disabled")
        self.info_text.grid(row=row, column=0, sticky="ew", pady=5)
        self.info_text.configure(font=("Courier", 8))
        
    def create_progress_controls(self, parent, row):
        # Progress
        self.progress_label = ttk.Label(parent, text="Ready")
        self.progress_label.grid(row=row, column=0, sticky="w", pady=(5, 0))
        
        self.progress_bar = ttk.Progressbar(parent, mode="indeterminate", bootstyle=SUCCESS)
        self.progress_bar.grid(row=row+1, column=0, sticky="ew", pady=(5, 0))
        
        # Buttons
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=row+2, column=0, sticky="ew", pady=5)
        btn_frame.columnconfigure((0, 1), weight=1)
        
        self.compress_btn = ttk.Button(btn_frame, text="Compress", command=self.start_compression, bootstyle=DANGER)
        self.compress_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_all, bootstyle=SECONDARY).grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=[
                ("Media Files", "*.mp4 *.avi *.mov *.mkv *.jpg *.jpeg *.png *.gif *.bmp"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.input_file.set(file_path)
            self.update_file_info()
            self.suggest_output_file()
            
    def select_output_file(self):
        if not self.input_file.get():
            messagebox.showwarning("Warning", "Select an input file first.")
            return
            
        file_type = self.determine_file_type(self.input_file.get())
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg" if file_type == "image" else ".mp4",
            filetypes=[("JPEG Files" if file_type == "image" else "MP4 Files", "*.jpg" if file_type == "image" else "*.mp4"), ("All Files", "*.*")],
            title="Save Compressed File As"
        )
        if file_path:
            self.output_file.set(file_path)
            
    def suggest_output_file(self):
        if self.input_file.get():
            input_path = Path(self.input_file.get())
            suggested_name = f"{input_path.stem}_compressed{input_path.suffix}"
            self.output_file.set(str(input_path.parent / suggested_name))
            
    def update_file_info(self):
        if not self.input_file.get():
            return
            
        file_path = self.input_file.get()
        if os.path.exists(file_path):
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            file_type = self.determine_file_type(file_path)
            
            info = f"File: {os.path.basename(file_path)}\nType: {file_type.title()}\nSize: {size_mb:.2f} MB"
            self.info_text.configure(state="normal")
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
            self.info_text.configure(state="disabled")
            
    def determine_file_type(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        return "image" if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp'] else "video" if ext in ['.mp4', '.avi', '.mov', '.mkv'] else "unknown"
            
    def start_compression(self):
        if not self.input_file.get() or not self.output_file.get():
            messagebox.showwarning("Warning", "Select both input and output files.")
            return
            
        if self.is_processing:
            messagebox.showinfo("Info", "Compression in progress.")
            return
            
        self.is_processing = True
        self.compress_btn.configure(state=DISABLED, text="Processing...")
        self.progress_bar.start()
        self.progress_label.configure(text="Compressing...")
        
        threading.Thread(target=self.compress_file, daemon=True).start()
        
    def compress_file(self):
        try:
            file_type = self.determine_file_type(self.input_file.get())
            success = False
            
            if file_type == "image":
                success = self.compress_image()
            elif file_type == "video":
                success = self.compress_video()
            else:
                self.progress_label.configure(text="Unsupported file type")
                messagebox.showerror("Error", "Unsupported file type.")
                
            if success:
                size_mb = os.path.getsize(self.output_file.get()) / (1024 * 1024)
                self.progress_label.configure(text=f"Done! Size: {size_mb:.2f} MB")
                messagebox.showinfo("Success", "Compression completed!")
            else:
                self.progress_label.configure(text="Compression failed")
                messagebox.showerror("Error", "Compression failed.")
                
        except Exception as e:
            self.progress_label.configure(text="Error occurred")
            messagebox.showerror("Error", f"Error: {str(e)}")
            
        finally:
            self.is_processing = False
            self.compress_btn.configure(state=NORMAL, text="Compress")
            self.progress_bar.stop()
            
    def compress_image(self):
        try:
            img = Image.open(self.input_file.get())
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                
            quality_map = {"low": 85, "medium": 60, "high": 40}
            img.save(self.output_file.get(), quality=quality_map[self.compression_level.get()], optimize=True)
            return True
        except Exception as e:
            print(f"Image compression error: {e}")
            return False
            
    def compress_video(self):
        try:
            settings_map = {
                "low": {"bitrate": "800k", "crf": 23},
                "medium": {"bitrate": "500k", "crf": 28},
                "high": {"bitrate": "300k", "crf": 32}
            }
            settings = settings_map[self.compression_level.get()]
            
            command = [
                "ffmpeg", "-i", self.input_file.get(),
                "-vcodec", "libx264", "-b:v", settings['bitrate'],
                "-crf", str(settings['crf']), "-preset", "medium",
                "-y", self.output_file.get()
            ]
            
            result = subprocess.run(command, capture_output=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Video compression error: {e}")
            return False
            
    def clear_all(self):
        self.input_file.set("")
        self.output_file.set("")
        self.compression_level.set("medium")
        self.info_text.configure(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.configure(state="disabled")
        self.progress_label.configure(text="Ready")
        
if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = MediaCompressorGUI(root)
    root.mainloop()