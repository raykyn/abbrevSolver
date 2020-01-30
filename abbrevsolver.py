#! /usr/bin/python3

import csv
import copy
import glob
try:
    from lxml import etree as et
except:
    import xml.etree.ElementTree as et
import re
import os
from tkinter import *
from tkinter import messagebox

"""
Version 2.1
- Fixed encoding for Windows machines
- Explained special chars variable
"""

# all chars in this list will be tagged as "insecure" if they are not part of an abbreviation in the tsv-file
# this is thought to mark abbreviations that are missing in the tsv-file
# all characters in this list strongly denote abbreviations in german transcriptions.
# change this to your needs or just delete everything inside the brackets if you don't want it
special_chars = [b'\xcc\x84', b"'", b'\xcc\x83', b'\xe2\x82\x8e', b'\xcb\x80']

class AbbrExp():
    """This is a custom class designed to store an abbreviation and all info about it."""
    
    def __init__(self, abbr, exp, insecure, context):
        self.abbr = abbr
        self.context = context
        if insecure == "X" or "|" in exp:
            self.exp = "PRÜFEN_"+exp
        else:
            self.exp = exp
            
    def title(self):
        titled_self = copy.copy(self)
        titled_self.abbr = self.abbr.title()
        titled_self.exp = self.exp.title()
        return titled_self
            
    def __len__(self):
        return len(self.abbr)
            
    def __str__(self):
        return self.abbr
        
    def __repr__(self):
        return self.abbr
        

class customChar():
    """This class stores all information about a unique character."""
    
    def __init__(self, letter, position, sentence):
        self.letter = letter
        self.position = position
        self.sent = sentence
        self.occupied = False
        self.sentence_starting = False
        self.enc = letter.encode("utf8")
        
    def check_for_untagged_special_char(self, previous):
        """Check for signature chars which are not already tagged."""
        if self.enc in special_chars and not self.occupied and not previous.occupied:
            self.occupied = True
            previous.occupied = True
            return True
        else:
            return False
    
    def compare_abbrev(self, abbrev, sent_starting):
        """
        This is where the magic happens. Most of this code is checking
        suffix, prefix and standalone though.
        """
        
        if sent_starting:
            # test once with normal abbrev, once with titled abbrev
            if self.compare_abbrev(abbrev, sent_starting=False):
                return True
            elif self.compare_abbrev(abbrev.title(), sent_starting=False):
                return "Titlecase"
            else:
                return False
        
        if abbrev.abbr == "NICHTAKTIV" and self.sent[self.position:self.position+len(abbrev)] == "NICHTAKTIV":
            print("PRINTING ACTIVATED")
            activate_prints = True
        else:
            activate_prints = False
        #~ print(self.sent[self.position:self.position+len(abbrev)], abbrev, self.occupied)
        if activate_prints:
            print(self.occupied)
        if activate_prints:
            print(self.sent[self.position:self.position+len(abbrev)] == abbrev.abbr)
        if (not self.occupied) and (self.sent[self.position:self.position+len(abbrev)] == abbrev.abbr):
            alone_on_line = False
            prefix = False
            suffix = False
            
            if self.position-1 < 0 and self.position+len(abbrev) >= len(self.sent):
                alone_on_line = True
                
            if (self.position-1 >= 0 and self.sent[self.position-1] in [".",","," "]) or self.position-1 < 0:
                prefix = True
                
            if (self.position+len(abbrev) < len(self.sent) and self.sent[self.position+len(abbrev)] in [".",","," "]) or self.position+len(abbrev) >= len(self.sent):
                suffix = True
                
            if abbrev.context.lower() == "sa": # standalone
                if alone_on_line or (prefix and suffix):
                    return True
                else:
                    return False
            elif abbrev.context.lower() == "px": # prefix
                if prefix and not suffix:
                    return True
                else:
                    return False
            elif abbrev.context.lower() == "sx": # suffix
                if suffix and not prefix:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
            
            
    def __str__(self):
        return self.letter
        
    def __repr__(self):
        return self.letter
        
        
            
class AbbrevSolver():
    """
    This application is built to read a given Page-XML, detect all
    occuring abbreviations and modify the Page-XML to mark them.
    """
    def __init__(self):
        """Initialization of the application, loading and building"""
        self.build_app()
        
            
    def loadAbbrevs(self, inf):
        """
        Method to read the abbreviation-expansion lists and store them
        in a sorted list (longer before shorter abbrevs).
        @param inf: file object (csv)
        """
        abbrList = []
        with open(inf, encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                if row["Abbreviation"] != "":
                    new_abbrev = AbbrExp(row["Abbreviation"], row["Expansion"], row["Insecure?"], row["Context"])
                    abbrList.append(new_abbrev)
        sorted_abbrList = sorted(abbrList, key=lambda x: len(x.abbr), reverse=True)        
        return sorted_abbrList
        
        
    def run(self):
        """
        Main work process, trigerred by the "run"-Button. Reads the XML
        from the Text Widget, detects all the abbreviations in it,
        then modifies the XML to mark those abbreviations and their 
        expansions. Prints the modified XML to the Text Widget.
        """
        try:
            abbrevList = self.loadAbbrevs("data/"+self.abbrevfile.get())
        except Exception as e:
            print(e)
            messagebox.showerror(title="Fail!", message="""Abbreviation-Expansion list could not be loaded, please make sure the chosen file doesn't contain any errors.""")
            return None
        content = self.entry_field.get("1.0",END)
        # delete the xml declaration (nec for parsing)
        content = re.sub("<\?xml version.*?>", "", content)
        root = et.fromstring(content)
        textlines = root.findall(".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}TextLine")
        for tl in textlines:
            current_info = tl.get("custom")
            # skip already solved lines
            if "abbrev" in current_info:
                continue
            to_add = [] # saves all the found abbreviations in format (offset, length, expansion)
            line = tl.find(".//{http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15}Unicode")
            if line is None:
                continue
            line_content = line.text
            custom_line_content = []
            if line_content is None:
                continue
            for n, char in enumerate(line_content):
                c = customChar(char, n, line_content)
                custom_line_content.append(c)
            #~ print(custom_line_content)
            for i in range(len(custom_line_content)):
                if i+2 < len(custom_line_content) and custom_line_content[i].letter == ".":
                    # mark as sentence start
                    custom_line_content[i+2].sentence_starting = True
                for abbr in abbrevList:
                    compare = custom_line_content[i].compare_abbrev(abbr, sent_starting=custom_line_content[i].sentence_starting)
                    if compare is True:
                        for character in custom_line_content[custom_line_content[i].position:custom_line_content[i].position+len(abbr)]:
                            character.occupied = True
                        to_add.append((custom_line_content[i].position, len(abbr.abbr), abbr.exp))
                        break
                    elif compare == "Titlecase":
                        for character in custom_line_content[custom_line_content[i].position:custom_line_content[i].position+len(abbr)]:
                            character.occupied = True
                        to_add.append((custom_line_content[i].position, len(abbr.abbr), abbr.exp.title()))
                        break
                if custom_line_content[i].check_for_untagged_special_char(custom_line_content[i-1]):
                    to_add.append((custom_line_content[i].position-1, 2, "UNBEKANNT"))
            #############################################################
            #~ print(to_add)
            for off, length, expan in to_add:
                current_info = current_info + " abbrev {{offset:{}; length:{};expansion:{};}}".format(off, length, expan)
            tl.attrib["custom"] = current_info
        # write the changed file to the field
        self.entry_field.delete("1.0", END)
        self.entry_field.insert(END, et.tostring(root, encoding="latin1"))
        self.entry_field.update()
        messagebox.showinfo(title="Success!", message="Process finished successfully! Copy XML back into Transkribus now.")
            
        
########################################## GRAPHICAL PART ####################################
        
    def build_app(self):
        """
        Building the graphical part.
        """
        self.root = Tk()
        self.root.title("Abbreviation Solver <(°u°)>")
        self.root.bind_class("Text","<Control-a>", self.selectall)
        
        # Paste and Copy buttons
        Button(self.root, text="Paste", command=self._paste).grid(row=0, column=0, sticky=W+E)
        Button(self.root, text="Copy", command=self._copy).grid(row=0, column=1, sticky=W+E)
        
        
        # build Text Field
        self.entry_field = Text(self.root)
        self.entry_field.grid(sticky=N+W+E, columnspan=2)
        
        Label(self.root, text="Choose Abbreviation Dictionary:").grid(columnspan=2)
        
        self.abbrevfile = StringVar()
        choices = glob.glob("data/*")
        choices = sorted([os.path.basename(c) for c in choices])
        dictmenu = OptionMenu(self.root, self.abbrevfile, *choices)
        self.abbrevfile.set(choices[0])
        dictmenu.grid(columnspan=2, sticky=W+E)
        
        b = Button(self.root, text="Run", command=self.run)
        b.grid(sticky=W+E+S, columnspan=2)
        
        mainloop()
        
    def selectall(self, event):
        """Selects everything in the Text Widget if Ctrl+A is pressed."""
        event.widget.tag_add("sel","1.0","end")
        
    def _paste(self):
        """Paste the clipboard content to the Text Widget."""
        try:
            to_paste = self.root.clipboard_get()
            self.entry_field.delete("1.0", END)
            self.entry_field.insert(END, to_paste)
            self.entry_field.update()
        except TclError:
            messagebox.showwarning(title="Clipboard empty", message="Clipboard is empty, try copying again.")
            
    def _copy(self):
        """Copy the content of the Text Widget to clipboard."""
        content = self.entry_field.get("1.0",END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        
        

if __name__ == "__main__":
    new_process = AbbrevSolver()
