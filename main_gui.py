import tkinter as tk
from threading import Thread
from tkinter import ttk
from tkinter import filedialog as fd, messagebox
import os
import sys
from h5ptranslate import H5PTranslator


class MainGUI(tk.Tk):

    def __init__(self):
        super().__init__()


        self.h5ptrans = H5PTranslator()
        self.geometry("800x800")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=1)
        self.resizable(0, 0)

        self.title("H5P Translator")

        button_height = 3
        button_width = 25

        padx = '3'
        pady = '3'

        curRow = 0
        ttk.Label(text="Translate your H5P file").grid(sticky=tk.E, row=curRow, column=0, padx=padx, pady=pady)
        curRow += 1

        self.btn_about = tk.Button(text="About...", width=10, height=2,command=self.about)
        self.btn_about.grid(row=0, column=3, columnspan=1, padx=padx, pady=pady)
        curRow += 1


        ttk.Label(text="Select source language:").grid(sticky=tk.E, row=curRow,column=1, padx=padx, pady=pady)
        self.select_source_lang = ttk.Combobox()
        self.select_source_lang['values'] = ('en', 'de')
        self.select_source_lang.grid(sticky=tk.W, row=curRow,column=2, padx=padx, pady=pady)
        self.select_source_lang.current(0)
        curRow += 1


        ttk.Label(text="Select target language:").grid(sticky=tk.E, row=curRow,column=1, padx=padx, pady=pady)
        self.select_target_lang = ttk.Combobox()
        self.select_target_lang['values'] = ('de', 'en', 'hu')
        self.select_target_lang.grid(sticky=tk.W, row=curRow,column=2, padx=padx, pady=pady)
        self.select_target_lang.current(0)
        curRow += 1

        self.btn_select_base_file = tk.Button(text="Select H5P base file",width=button_width,height=button_height,command=self.fileopen_base)
        self.btn_select_base_file.grid(row=curRow,column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1

        self.btn_translate = tk.Button(text="Translate",width=button_width,height=button_height,command=self.do_translate)
        self.btn_translate.grid(row=curRow,column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1
        self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=100)
        self.progressbar.grid(row=curRow, column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1

        self.btn_replace_images = tk.Button(text="Replace images",width=button_width,height=button_height,command=self.do_replace_images)
        self.btn_replace_images.grid(row=curRow,column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1

        ttk.Label(text="Untranslated IDs:").grid(row=curRow,column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1
        self.txt_untranslated_ids = tk.Text(height=10, width=60)
        self.txt_untranslated_ids.grid(row=curRow,column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1

        ttk.Label(text="Modified IDs:").grid(row=curRow,column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1
        self.txt_modified_ids = tk.Text(height=10, width=60)
        self.txt_modified_ids.grid(row=curRow,column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1

        self.btn_close_file = tk.Button(text="Close file",width=button_width,height=button_height,command=self.close_file)
        self.btn_close_file.grid(row=curRow, column=1, columnspan=2, padx=padx, pady=pady)
        curRow += 1



        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.translate_thread = None


        self.setComponentStates(False)



    def setComponentStates(self, open):
        if(open):
            self.btn_translate.config(state=tk.NORMAL)
            self.btn_replace_images.config(state=tk.NORMAL)
            self.btn_close_file.config(state=tk.NORMAL)
            self.btn_select_base_file.config(state=tk.DISABLED)
            self.select_target_lang.config(state=tk.DISABLED)
            self.select_source_lang.config(state=tk.DISABLED)
        else:
            self.btn_translate.config(state=tk.DISABLED)
            self.btn_replace_images.config(state=tk.DISABLED)
            self.btn_close_file.config(state=tk.DISABLED)
            self.btn_select_base_file.config(state=tk.NORMAL)
            self.select_target_lang.config(state=tk.NORMAL)
            self.select_source_lang.config(state=tk.NORMAL)
            self.txt_untranslated_ids.delete(1.0,tk.END)
            self.txt_modified_ids.delete(1.0,tk.END)


    def about(self):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        with(open(os.path.join(base_path, "version.txt"), "r")) as f:
            lines = f.read().splitlines()
            version = lines[0]
            hash = lines[1]
            aboutmessage = """
h5pTranslate

Authors: Michael Munz, Harald Groß, THU
Version: {}
Git hash: {}
https://github.com/michaelmunz/H5PTranslator/
            """.format(version, hash)
        messagebox.showinfo("About", message=aboutmessage)


    def __fileopen(self, text):
        filetypes = (
            ('h5p', '*.h5p'),
            ('json', '*.json')
        )
        filename = fd.askopenfilename(
            title=text,
            initialdir='.',
            filetypes=filetypes)
        return filename


    def fileopen_base(self):
        self.ori_file = self.__fileopen('Open base h5p file')
        if self.ori_file is None or self.ori_file == "":
            return
        fname = os.path.basename(self.ori_file)
        [name, ext] = os.path.splitext(fname)
        target_lang = self.select_target_lang.get()
        translate_name = name+"_"+target_lang+ext
        self.translate_file = os.path.abspath(os.path.join(os.path.dirname(self.ori_file), translate_name))
        try:
            self.h5ptrans.open(self.ori_file, self.translate_file)
            self.setComponentStates(True)
            self.update_h5pdata()
        except Exception as E:
            messagebox.showerror("Error while loading: ", message=str(E))



    def update_h5pdata(self):
        untranslated_ids = self.h5ptrans.getUntranslatedElementIDs()
        modified_ids = self.h5ptrans.getModifiedElementIDs()
        self.txt_untranslated_ids.delete("1.0", "end")
        for id in untranslated_ids:
            t = "Slide: {} (id: {})".format(self.h5ptrans.getSlideForElementID_original(id), id)
            self.txt_untranslated_ids.insert(tk.END, t + "\n")

        self.txt_modified_ids.delete("1.0", "end")
        for id in modified_ids:
            t = "Slide: {} (id: {})".format(self.h5ptrans.getSlideForElementID_original(id), id)
            self.txt_modified_ids.insert(tk.END, t + "\n")



    def translate_worker(self, untranslated_ids):
        for cnt,id in enumerate(untranslated_ids):
            source_lang = self.select_source_lang.get()
            target_lang = self.select_target_lang.get()
            self.h5ptrans.translate_element(source_lang, target_lang, id)
            self.progressbar.config(value=cnt/len(untranslated_ids)*100)

        self.progressbar.stop()
        self.btn_replace_images.config(state=tk.NORMAL)
        self.update_h5pdata()

    def do_translate(self):
        ids_to_translate = self.h5ptrans.getUntranslatedElementIDs() + self.h5ptrans.getModifiedElementIDs()

        self.translate_thread = Thread(target=self.translate_worker, args=(ids_to_translate,))
        self.translate_thread.start()



    def do_replace_images(self):
        dirname = fd.askdirectory(title="Select directory containing tranlated images")
        if dirname == '':
            tk.messagebox.showerror(title="No images selected", message="Please select a directory containing translated images first!")
        else:
            res = self.h5ptrans.replace_images("en", self.select_target_lang.get(), dirname)
            if not res:
                tk.messagebox.showerror(title="File error",
                                    message="The directory does not contain the required structure: subdirectory 'en' and subdirectory '{}' are required.".format(self.select_target_lang.get()))
            else:
                tk.messagebox.showinfo(title="Finished.",
                                        message="Images have been replaced.")


    def close_file(self):
        if self.h5ptrans.isOpen:
            confirm = messagebox.askyesnocancel(
                title="Closing",
                message="Do you want to save the changes?",
                default=messagebox.YES,
                parent=self)

            if confirm:
                self.h5ptrans.close(True)
            elif confirm==False:
                self.h5ptrans.close(False)
            else: # if None -> cancel has been chosen
                pass

            if confirm is not None:
                self.setComponentStates(False)
            return confirm is not None


    def on_closing(self):
        if self.h5ptrans.isOpen:
            confirm = self.close_file()
        else:
            confirm = messagebox.askyesno(
                title="Closing",
                message="Do you want to exit the application?",
                default=messagebox.YES,
                parent=self)

        if confirm is True:
            self.destroy()


if __name__ == "__main__":
    gui = MainGUI()
    gui.mainloop()

