import tkinter as tk
from tkinter import ttk
from pytube import YouTube

class Downloader:
    def __init__(self):
        self.saveto = ""
        self.window = tk.Tk()
        self.window.title("Youtube Downloader")
        self.credits_label = tk.Label(text="Created By Pratyush", anchor="se")
        self.credits_label.pack(side="top")
        self.url_label = tk.Label(text="Enter Youtube Video URL")
        self.url_label.pack()
        self.url_entry = tk.Entry()
        self.url_entry.pack()
        self.quality_button = tk.Button(text="Show Available Quality", command=self.show_quality)
        self.quality_button.pack()
        self.quality_listbox = tk.Listbox(self.window)
        self.quality_listbox.pack()
        self.quality_listbox.bind("<<ListboxSelect>>", self.on_select)
        self.download_button = tk.Button(text="Download",command=self.download_video)
        self.download_button.pack()
        self.selected_choice = None
        self.download_label = tk.Label(text="")
        self.download_label.pack()
        self.reset_button = tk.Button(text="Reset",command=self.reset)
        self.reset_button.pack()
        self.window.geometry("450x350")
        self.window.mainloop()

    def show_quality(self):
        url = self.url_entry.get()
        yt = YouTube(url)
        video_streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
        quality_options = [f"{stream.resolution} ({self.format_size(stream.filesize)})" for stream in video_streams]
        self.quality_listbox.delete(0, tk.END)  # Clear the listbox before updating
        for i, quality in enumerate(quality_options, start=1):
            self.quality_listbox.insert(tk.END, f"{i}. {quality} ")

    def on_select(self, event):
        selection = self.quality_listbox.get(self.quality_listbox.curselection())
        numbers = ''.join(filter(str.isdigit, selection))
        self.selected_choice = int(numbers[0])-1

    def download_video(self):
        if self.selected_choice is not None:
            url = self.url_entry.get()
            yt = YouTube(url)
            video_streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
            if 0 <= self.selected_choice < len(video_streams):
                selected_stream = video_streams[self.selected_choice]
                selected_stream.download()
                self.download_label.config(text="Download completed.")
            else:
                self.download_label.config(text="Invalid choice. Please select a valid quality option.")
        else:
            self.download_label.config(text="No quality option selected.")

    @staticmethod
    def format_size(size):
        power = 2**10
        n = 0
        size_labels = ['B', 'KB', 'MB', 'GB', 'TB']
        while size > power:
            size /= power
            n += 1
        return f"{size:.2f} {size_labels[n]}"
    
    def reset(self):
        self.url_entry.delete(0, tk.END)
        self.quality_listbox.delete(0, tk.END)
        self.selected_choice = None
        self.download_label.config(text="")

Downloader()
