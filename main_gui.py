import tkinter as tk
from threading import Thread
from tkinter import ttk
from tkinter import filedialog as fd, messagebox
import os
from h5p_python.h5ptranslate import H5PTranslator


class MainGUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.h5ptrans = H5PTranslator()
        self.geometry("800x800")

        self.title("H5P Translator")

        ttk.Label(text="Select target language:").grid(sticky=tk.E, row=0,column=0)

        self.select_target_lang = ttk.Combobox()
        self.select_target_lang['values'] = ('de', 'en', 'it', 'hu')
        self.select_target_lang.bind('<<ComboboxSelected>>', self.on_target_lang_selected)
        self.select_target_lang.grid(sticky=tk.W, row=0,column=1)


        self.btn_select_base_file = tk.Button(text="Select H5P base file (english)",
                  width=25,
                  height=5,
                  command=self.fileopen_base, state=tk.DISABLED
                  )
        self.btn_select_base_file.grid(row=1,column=0, columnspan=2)

        self.btn_translate = tk.Button(text="Translate",
                                       width=25,
                                       height=5,
                                       command=self.do_translate, state=tk.DISABLED
                                       )
        self.btn_translate.grid(row=2,column=0, columnspan=2)
        self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=100)
        self.progressbar.grid(row=3, column=0, columnspan=2)

        self.btn_replace_images = tk.Button(text="Replace images",
                                            width=25,
                                            height=5,
                                            command=self.do_replace_images, state=tk.DISABLED
                                            )
        self.btn_replace_images.grid(row=4,column=0, columnspan=2)

        ttk.Label(text="Untranslated IDs:").grid(row=5,column=0, columnspan=2)
        self.txt_untranslated_ids = tk.Text(height=10, width=60)
        self.txt_untranslated_ids.grid(row=6,column=0, columnspan=2)

        ttk.Label(text="Modified IDs:").grid(row=7,column=0, columnspan=2)
        self.txt_modified_ids = tk.Text(height=10, width=60)
        self.txt_modified_ids.grid(row=8,column=0, columnspan=2)


        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.translate_thread = None



    def on_target_lang_selected(self, val):
        self.target_lang = self.select_target_lang.get()
        self.btn_select_base_file.config(state = tk.NORMAL)


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
        if self.ori_file is None:
            return
        fname = os.path.basename(self.ori_file)
        [name, ext] = os.path.splitext(fname)
        translate_name = name+"_"+self.target_lang+ext
        self.translate_file = os.path.abspath(os.path.join(os.path.dirname(self.ori_file), translate_name))
        self.btn_translate.config(state=tk.NORMAL)
        self.h5ptrans.open(self.ori_file, self.translate_file)


        self.update_h5pdata()


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
            elem = self.h5ptrans.getElementByID_original(id)
            print("Autotranslating id '{}': '{}'".format(id, elem.getText()))
            autotranslated_text = self.h5ptrans.getAutoTranslation("en", self.target_lang, elem.getText())
            print("Result: " + autotranslated_text)
            self.h5ptrans.setTranslation(id, autotranslated_text)
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
            self.h5ptrans.setTranslatedImages(dirname)


    def on_closing(self):
        confirm = messagebox.askyesnocancel(
            title="Closing",
            message="Do you want to save the changes?",
            default=messagebox.YES,
            parent=self)

        if confirm:
            self.h5ptrans.close(True)
            self.destroy()
        elif not confirm:
            self.h5ptrans.close(False)
            self.destroy()
        else:
            pass

if __name__ == "__main__":
    gui = MainGUI()
    gui.mainloop()

