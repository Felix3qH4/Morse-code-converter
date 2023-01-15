# Author: Felix3qH4
# Date: 14/01/2023
# DD/MM/YYYY

import tkinter as tk
import json


FONT : str = "Arial"
TABLES_FILE : str = "tables.json"


with open(TABLES_FILE, "r", encoding="utf-8") as _file:
    TABLES = json.load(_file)


class Cryptor():
    def __init__(self, table:dict) -> None:
        """
        :param table: dict containing the morse code for each letter/number/special character
        :return: None
        """

        self.set_table(table)


    def encrypt(self, text:str, output_label:tk.Label = None, output_entry:tk.Entry=None) -> str:
        """
        Encrypt text to morse code

        :param text: String containing the text that should be encrypted to morse
        :param output_label: Tkinter label to write the morse code to

        :return str: morse code string
        """
        
        morse_code = ""

        for letter in text:
            if letter != " ":
                if letter.upper() in self.table:
                    morse_code += self.table[letter.upper()] + "/"
                else:
                    if letter != " " and letter != "\n":
                        morse_code += "??" + letter + "??/"
            else:
                morse_code += "/"


        if output_label:
            output_label.config(text=morse_code)
        if output_entry:
            output_entry.delete(1.0, tk.END)
            output_entry.insert(1.0, morse_code)

        return morse_code
    

    def decrypt(self, morse_code:str, output_label:tk.Label=None, output_entry:tk.Entry=None) -> str:
        """
        Decrypt morse code to text

        :param morse_code: String containing the morse code (each word has to be delimited by a '//' and each letter by a '/')
        
        :return str: String containing the decrypted text
        """
        text = ""
        current_letter = ""
        last_letter = ""

        for letter in morse_code:
            
            if letter != "/":
                current_letter += letter

            elif letter == "/":

                if current_letter in self.inverted_table:
                    text += self.inverted_table[current_letter]
                    current_letter = ""

                elif not current_letter in self.inverted_table and current_letter != " " and current_letter != "\n":
                    text += "??" + current_letter + "??"
                    current_letter = ""

                    
                if last_letter == "/" and letter == "/":
                    text += " "
            
            last_letter = letter
                        


        if output_label:
            output_label.config(text=text)
        if output_entry:
            output_entry.delete(1.0, tk.END)
            output_entry.insert(1.0, text)

        return text


    def set_table(self, table:dict) -> None:
        """
        Change the table with which the text is being encrypted/decrypted

        :param table: dict containing the translation from text to morse

        :return: None
        """

        if isinstance(table, dict):
            self.table = table
            self.inverted_table = {y: x for x, y in self.table.items()}
        
        else:
            raise TypeError(f"[Class][Cryptor][set_table]: Argument 'table' should be of type 'dict', got '{type(table)}' instead.")
    


def change_table(*args):
    encryptor.set_table(TABLES[tables_choices_var.get()])


encryptor = Cryptor(list(TABLES.values())[0])

window = tk.Tk()
window.geometry("500x600")

title = tk.Label(window, text="Convert text to morse", font=(FONT, 23, "underline"))
title.pack()

spacer = tk.Label(window, text="", font=(FONT, 15)).pack()

## Tables choice
tables_choices = list(TABLES.keys())
tables_choices_var = tk.StringVar()
tables_choices_var.set(tables_choices[0])
tables_choices_var.trace("w", change_table)

choices_text = tk.Label(window, text="Conversion table:", font=(FONT, 13, "underline")).pack()

tables_choices_combobox = tk.OptionMenu(window, tables_choices_var, *tables_choices)
tables_choices_combobox.config(font=(FONT, 13))
choices = tables_choices_combobox.nametowidget(tables_choices_combobox.menuname)
choices.config(font=(FONT, 13))
tables_choices_combobox.pack()

spacer = tk.Label(window, text="", font=(FONT, 15)).pack()


## Text part
text_to = tk.Label(window, text="Text:", font=(FONT, 15, "underline"))
text_to.pack()

text_entry_var = tk.StringVar()
text_entry = tk.Text(window, font=(FONT, 15), height=5, width=30)
text_entry.pack()

text_to_morse_btn = tk.Button(window, text="Convert to morse", font=(FONT, 15), command = lambda: encryptor.encrypt(text=text_entry.get(1.0, "end-1c"), output_entry = morse_entry))
text_to_morse_btn.pack()

spacer = tk.Label(window, text="", font=(FONT, 15)).pack()

## Morse code part
output_title = tk.Label(window, text="Morse code:", font=(FONT, 15, "underline")).pack()

morse_code_entry_var = tk.StringVar()
morse_entry = tk.Text(window, font=(FONT, 15), height=5, width=30)
morse_entry.pack()

morse_to_text_btn = tk.Button(window, text="Convert to text", font=(FONT, 15), command = lambda: encryptor.decrypt(morse_code=morse_entry.get(1.0, "end-1c"), output_entry = text_entry))
morse_to_text_btn.pack()


window.mainloop()