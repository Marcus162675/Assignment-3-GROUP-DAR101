from tkinter import *
from tkinter import ttk, messagebox
import googletrans
import textblob

class TranslatorApp(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Language Translator for Assignment 3')
        self.master.geometry("950x300")
        self.create_widgets()

    def create_widgets(self):
        # Text boxes
        self.original_text = Text(self.master, height=10, width=40)
        self.original_text.grid(row=0, column=0, pady=20, padx=10)

        self.translate_button = Button(self.master, text="Please translate", font=("Arial", 20), command=self.help_me)
        self.translate_button.grid(row=0, column=1, padx=10)

        self.translated_text = Text(self.master, height=10, width=40)
        self.translated_text.grid(row=0, column=2, pady=20, padx=10)

        # comboboxes
        self.original_combo = ttk.Combobox(self.master, width=50, values=self.language_list())
        self.original_combo.current(21)
        self.original_combo.grid(row=1, column=0)

        self.translated_combo = ttk.Combobox(self.master, width=50, values=self.language_list())
        self.translated_combo.current(22)
        self.translated_combo.grid(row=1, column=2)

        # clear button
        self.clear_button = Button(self.master, text="clear", command=self.clear)
        self.clear_button.grid(row=2, column=1)

    def help_me(self):
        # deleting completed translations
        self.translated_text.delete(1.0, END)
        try:
            # get languages from googletrans key
            # get from language
            from_language_key = ""
            to_language_key = ""
            for key, value in self.languages().items():
                if value == self.original_combo.get():
                    from_language_key = key
                if value == self.translated_combo.get():
                    to_language_key = key
            
            # turning original text into textblob
            words = textblob.TextBlob(self.original_text.get(1.0, END))

            # translate text
            words = words.translate(from_lang=from_language_key, to=to_language_key)

            # output the text
            self.translated_text.insert(1.0, words)
        
        except Exception as e:
            messagebox.showerror("translator", e)

    def clear(self):
        self.original_text.delete(1.0, END)
        self.translated_text.delete(1.0, END)

    def languages(self):
        return googletrans.LANGUAGES

    def language_list(self):
        return list(self.languages().values())

if __name__ == "__main__":
    root = Tk()
    app = TranslatorApp(master=root)
    app.mainloop()
