######
# HOW TO USE ABBREVSOLVER
######
# First Version By Ismail Prada, 10.10.2017
# Latest Version By Ismail Prada, 30.10.2017
######

### REQUIREMENTS ###
- Make sure you have Python 3.5 or newer installed, you can find it here:
    - https://www.python.org/

### INSTALLATION AND STARTUP ###
- Unzip the directory into a place of your choice.
- Open a terminal (or command line).
- Navigate to the Abkürzungsauflöser-Directory.
- Type: python3 abbrevsolver.py
- Press enter to start the application.

### USE ###
- This application tags abbreviations in a Page-XML file. 
- Additionally to the tags, the expansions are filled in.
- Lines which already contain abbreviation tags will be ignored!

### HOW TO USE ###
- Copy the Page-XML content of you Transkribus-file onto the clipboard.
    - Mark everything and press Ctrl+C or CMD+C.
- Now press the "Paste"-Button in the application.
- Chosse the data file below that should be used. You can create new data
    files by adding them to the "data"-folder. Use existing data-files
    as examples on how to create it. While file ending is unimportant,
    the file should be written as a .tsv-file (fields separated by tabs).
- Press "Run" and wait for the Success-confirmation to pop up. 
- Now press "Copy" to copy the modified Page-XML to your clipboard again.
- Replace the old Page-XML with the modified version in Transkribus
    - Mark everything (except the first line) and delete it, then 
        press Ctrl+V or CMD+V to insert the modified version.
        
### UNKNOWN SIGNS ###
Some signs are typical for abbreviations and are thus always tagged, if
they are not found as part of another abbreviation. The tag given to
those is "UNBEKANNT".
        
### DATA ###
In the "data" folder are the files kept, which assign expansions to each
abbreviation. Abbreviation with multiple possible expansions are separated
by a pipe sign (|). If there is an "X" in the column "Insecure?",
the application will add a tag "PRÜFEN" in front of every expansion, so
a human worker can search for the tag to control all the abbreviations
which are not always expanded the same way.
The fourth column "context" can contain three different tags, everything
else will be ignored: SA, SX, PX.
- SA: Standalone, abbrev will only be found if it has a whitespace or punctuation
    to the left and right.
- SX: Suffix, abbrev will only be found if it has a whitespace or punctuation
    to the right.
- PX: Prefix, abbrev will only be found if it has a whitespace or punctuation
    to the left.

### TO DO ###
- Prettify script

### LICENSE ###

MIT

Copyright 2017 Historisches Seminar Editionsprojekt Königsfelden (SNF Projekt)

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
