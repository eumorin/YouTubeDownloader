from tkinter import *
from tkinter import ttk, filedialog
import threading
import time
from downloader import *
from downloader import YouTubeDownloader
from utils import check_valid_url


class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("800x500")
        self.minsize(800, 500)
        self.maxsize(800, 500)
        self.protocol("WM_DELETE_WINDOW", self.finish)
        self.create_styles()
        self.create_widgets()
        self.create_bindings()
        self.format_box_values = []

        self.downloader = None

    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure("DL.TButton", foreground="black", background="black", font=("Arial Black", 10))

    def create_widgets(self):
        self.frm1 = ttk.Frame(borderwidth=2, padding=10)
        self.frm1.pack(expand=TRUE)

        self.btn_download = ttk.Button(master=self.frm1, text="Download",
                                       command=lambda: self.start('Download'),
                                       style="DL.TButton")
        self.btn_download.grid(row=1, column=1, ipadx=2, ipady=2)

        self.entry = ttk.Entry(master=self.frm1, foreground="grey", width=50, font=("Arial", 10))
        self.entry.insert(0, "Paste a link here")
        self.entry.grid(row=1, column=0, padx=(0, 20))

        self.lb_head = ttk.Label(master=self.frm1, text="Download video from YouTube", cursor="ibeam",
                                 font=("Arial Black", 14))
        self.lb_head.grid(row=0, columnspan=2, pady=(0, 10))

        self.lb_message = ttk.Label(master=self.frm1, text="", cursor="ibeam", foreground="red", font=("Arial", 8))

        self.frm2 = ttk.Frame(borderwidth=2, padding=10)
        self.frm2.pack(expand=TRUE, pady=(0, 0))

        self.lb_photo = ttk.Label(master=self.frm2)

        self.lb_video_name = ttk.Label(master=self.frm2, text="", font=("Arial", 10), wraplength=300)

        self.lb_format = ttk.Label(master=self.frm2, text="Choose preferable format:", font=("Arial", 10))

        self.box_format = ttk.Combobox(master=self.frm2, width=10, state="readonly", font=("Arial", 8))

        self.btn_save = ttk.Button(self.frm2, text="Save file",
                                   command=lambda: self.start('Save'),
                                   style="DL.TButton")

        self.progress_bar = ttk.Progressbar(orient='horizontal', value=0, maximum=100)
        self.progress_bar.pack(expand=TRUE, fill=X, anchor=S)

    def create_bindings(self):
        self.bind("<ButtonPress-1>", self.on_canvas_clicked)
        self.box_format.bind('<<ComboboxSelected>>', self.on_combobox_clicked)
        self.entry.bind("<FocusIn>", self.on_entry_focusin)
        self.entry.bind("<FocusOut>", self.on_entry_focusout)

    def on_combobox_clicked(self, event):
        self.btn_save.grid(row=0, column=1, sticky=W, pady=(15, 0), padx=(270, 0))

    def on_canvas_clicked(self, event):
        if event.widget == self:
            self.focus_set()
        if event.widget == self.frm1:
            self.frm1.focus_set()

    def on_entry_focusin(self, event):
        if self.entry.get() == "Paste a link here":
            self.entry.delete(0, last=END)
            self.entry.insert(0, '')
            self.entry.config(foreground="black")

    def on_entry_focusout(self, event):
        if self.entry.get() == '':
            self.entry.insert(0, "Paste a link here")
            self.entry.config(foreground='grey')

    def update_progress_bar(self, process, progress_bar):
        self.progress_bar.configure(mode='indeterminate')
        self.progress_bar.start()
        while process.is_alive():
            self.update_idletasks()
        self.progress_bar.stop()
        self.progress_bar.configure(mode='determinate')
        self.progress_bar['value'] = progress_bar['maximum']
        time.sleep(0.2)
        self.progress_bar['value'] = 0

    def update_interface(self, video_info):
        self.lb_photo.config(image=video_info['thumbnail'])
        self.lb_photo.grid_configure(row=0, rowspan=2, padx=(5, 0), pady=(5, 0), sticky=W)
        self.lb_video_name.config(text=video_info['title'])
        self.lb_video_name.grid_configure(row=0, column=1, sticky=W, pady=(0, 95), padx=(10, 0))
        self.lb_format.grid_configure(row=0, column=1, sticky=W, pady=(15, 0), padx=(10, 0))
        self.box_format.config(values=video_info['format_box_values'])
        self.box_format.grid_configure(row=0, column=1, sticky=W, padx=(165, 0), pady=(15, 0))

    def url_exception(self):
        if self.lb_message.cget('text') != "":
            self.lb_message.config(text="Access to video is denied.")
        else:
            self.lb_message.config(text="Access to video is denied.")
            self.lb_message.grid(row=2, columnspan=2, sticky=W, pady=(5, 0))

    def finish(self):
        if os.path.exists('thumbnail.jpg'):
            os.remove('thumbnail.jpg')
        self.destroy()

    def callback_handler(self, *args):
        if not args:
            print("Error: No callback name provided")
            return

        callback_name = args[0]
        additional_args = args[1:] if len(args) > 1 else None

        match callback_name:
            case 'Access Error':
                self.url_exception()
            case 'Interface Update':
                if additional_args and isinstance(additional_args[0], dict):
                    self.update_interface(video_info=additional_args[0])
            case _:
                print(f"Error: Unknown callback type '{callback_name}'")

    def start(self, function_type):
        download_thread = None
        match function_type:
            case 'Download':
                if self.frm2.grid_slaves():
                    for slave in self.frm2.grid_slaves():
                        slave.grid_remove()

                if self.lb_message.cget('text') != "":
                    self.lb_message.grid_remove()

                if check_valid_url(self.entry.get()):
                    self.downloader = YouTubeDownloader(self.entry.get(), self.callback_handler)
                    download_thread = threading.Thread(target=self.downloader.fetch_video_info)
                    download_thread.start()
                else:
                    self.lb_message.config(text="Given url is invalid, try again !")
                    self.lb_message.grid(row=2, columnspan=2, sticky=W, pady=(5, 0))
            case 'Save':
                selected_format = self.box_format.get()
                download_thread = threading.Thread(target=self.downloader.save_file, args=(selected_format, ))
                download_thread.start()

        if download_thread:
            progress_thread = threading.Thread(target=self.update_progress_bar,
                                               args=(download_thread, self.progress_bar))
            progress_thread.start()