"""
    Project: Part of PF2 to CSV Converter Project

    Project Description: Converts a '.pf2' file to a '.csv'

    Dependencies:
        None

    Author:
        Tom Stokke

    Project Contributor(s):
        run.py - Mason Motschke
"""
#egversion = __doc__.split()[1]

__all__ = [
      'selectDir'
    , 'selectOpenFile'
    , 'selectSaveFile'
    ]

import sys, os, string, types, pickle,traceback

from tkinter import *
import tkinter.filedialog as tk_FileDialog
from io import StringIO

def write(*args):
    args = [str(arg) for arg in args]
    args = " ".join(args)
    sys.stdout.write(args)
    
def writeln(*args):
    write(*args)
    sys.stdout.write("\n")
    
    
def dq(s):
    return '"%s"' % s

#-------------------------------------------------------------------
# selectOpenFile
#-------------------------------------------------------------------
def selectDirectory(msg=None
    , title=None
    , default=None
    ):
    """
    A dialog to get a directory name.
    Note that the msg argument, if specified, is ignored.

    Returns the name of a directory, or None if user chose to cancel.

    If the "default" argument specifies a directory name, and that
    directory exists, then the dialog box will start with that directory.
    """
    title=getFileDialogTitle(msg,title)      
    boxRoot = Tk()
    boxRoot.withdraw()
    if not default: default = None
    f = tk_FileDialog.askdirectory(
          parent=boxRoot
        , title=title
        , initialdir=default
        , initialfile=None
        )          
    boxRoot.destroy()     
    if not f: return None
    return os.path.normpath(f)



#-------------------------------------------------------------------
# getFileDialogTitle
#-------------------------------------------------------------------
def getFileDialogTitle(msg
    , title
    ):
    if msg and title: return "%s - %s" % (title,msg)
    if msg and not title: return str(msg)
    if title and not msg: return str(title)
    return None # no message and no title

#-------------------------------------------------------------------
# class FileTypeObject for use with fileOpenBox
#-------------------------------------------------------------------
class FileTypeObject:
    def __init__(self,filemask):
        if len(filemask) == 0:
            raise AssertionError('Filetype argument is empty.')
            
        self.masks = []
        
        if type(filemask) == type("abc"):  # a string
            self.initializeFromString(filemask)
            
        elif type(filemask) == type([]): # a list
            if len(filemask) < 2:
                raise AssertionError('Invalid filemask.\n'
                +'List contains less than 2 members: "%s"' % filemask)
            else:
                self.name  = filemask[-1]
                self.masks = list(filemask[:-1] )
        else:
            raise AssertionError('Invalid filemask: "%s"' % filemask)

    def __eq__(self,other):
        if self.name == other.name: return True
        return False
    
    def add(self,other):
        for mask in other.masks:
            if mask in self.masks: pass
            else: self.masks.append(mask)

    def toTuple(self):
        return (self.name,tuple(self.masks))
        
    def isAll(self):
        if self.name == "All files": return True
        return False
        
    def initializeFromString(self, filemask):
        # remove everything except the extension from the filemask
        self.ext = os.path.splitext(filemask)[1]
        if self.ext == "" : self.ext = ".*"
        if self.ext == ".": self.ext = ".*"
        self.name = self.getName()
        self.masks = ["*" + self.ext]
        
    def getName(self):
        e = self.ext
        if e == ".*"  : return "All files"
        if e == ".txt": return "Text files"
        if e == ".py" : return "Python files"
        if e == ".pyc" : return "Python files"
        if e == ".xls": return "Excel files"
        if e.startswith("."): 
            return e[1:].upper() + " files"
        return e.upper() + " files"


#-------------------------------------------------------------------
# selectOpenFile
#-------------------------------------------------------------------
def selectOpenFile(msg=None
    , title=None
    , default="*"
    , filetypes=None
    ):
    """
    A dialog to get a file name.
    
    About the "default" argument
    ============================
        The "default" argument specifies a filepath that (normally)
        contains one or more wildcards.
        fileOpenBox will display only files that match the default filepath.
        If omitted, defaults to "*" (all files in the current directory).
    
        WINDOWS EXAMPLE::
            ...default="c:/myjunk/*.py"  
        will open in directory c:\myjunk\ and show all Python files.

        WINDOWS EXAMPLE::
            ...default="c:/myjunk/test*.py"  
        will open in directory c:\myjunk\ and show all Python files
        whose names begin with "test".
        
        
        Note that on Windows, fileOpenBox automatically changes the path
        separator to the Windows path separator (backslash).

    About the "filetypes" argument
    ==============================
        If specified, it should contain a list of items,
        where each item is either::
            - a string containing a filemask          # e.g. "*.txt"        
            - a list of strings, where all of the strings except the last one
                are filemasks (each beginning with "*.",
                such as "*.txt" for text files, "*.py" for Python files, etc.).
                and the last string contains a filetype description
            
        EXAMPLE::
            filetypes = ["*.css", ["*.htm", "*.html", "HTML files"]  ]
        
    NOTE THAT
    =========

        If the filetypes list does not contain ("All files","*"),
        it will be added.

        If the filetypes list does not contain a filemask that includes
        the extension of the "default" argument, it will be added.
        For example, if     default="*abc.py"
        and no filetypes argument was specified, then
        "*.py" will automatically be added to the filetypes argument.

    @rtype: string or None
    @return: the name of a file, or None if user chose to cancel

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg default: filepath with wildcards
    @arg filetypes: filemasks that a user can choose, e.g. "*.txt"
    """
    boxRoot = Tk()
    boxRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fileSelectSetup(default,filetypes)

    #------------------------------------------------------------
    # if initialfile contains no wildcards; we don't want an
    # initial file. It won't be used anyway.
    # Also: if initialbase is simply "*", we don't want an
    # initialfile; it is not doing any useful work.
    #------------------------------------------------------------
    if (initialfile.find("*") < 0) and (initialfile.find("?") < 0):
        initialfile = None
    elif initialbase == "*":
        initialfile = None

    f = tk_FileDialog.askopenfilename(parent=boxRoot
        , title=getFileDialogTitle(msg,title)      
        , initialdir=initialdir                    
        , initialfile=initialfile
        #, filetypes=[('All Files', '*.*')]
        #, filetypes=[('All Files', '*.*'), ('Text files', "*.txt")]
        )

    boxRoot.update()
    boxRoot.destroy()     

    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
# selectSaveFile
#-------------------------------------------------------------------
def selectSaveFile(msg=None
    , title=None
    , default=""
    , filetypes=None
    ):
    """ 
    A file to get the name of a file to save.
    Returns the name of a file, or None if user chose to cancel.

    The "default" argument should contain a filename (i.e. the
    current name of the file to be saved).  It may also be empty,
    or contain a filemask that includes wildcards.
    
    The "filetypes" argument works like the "filetypes" argument to
    fileOpenBox.
    """

    boxRoot = Tk()
    boxRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fileSelectSetup(default,filetypes)
    
    f = tk_FileDialog.asksaveasfilename(parent=boxRoot
        , title=getFileDialogTitle(msg,title)     
        , initialfile=initialfile
        , initialdir=initialdir
        #, filetypes=filetypes
        )
    boxRoot.update()
    boxRoot.destroy()     
    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
#
# fileSelectSetup
#
#-------------------------------------------------------------------
def fileSelectSetup(default,filetypes):    
    if not default: default = os.path.join(".","*")
    initialdir, initialfile = os.path.split(default)
    if not initialdir : initialdir  = "."
    if not initialfile: initialfile = "*"
    initialbase, initialext = os.path.splitext(initialfile)
    initialFileTypeObject = FileTypeObject(initialfile)
    
    allFileTypeObject = FileTypeObject("*")
    ALL_filetypes_was_specified = False  

    if not filetypes: filetypes= []
    filetypeObjects = []

    for filemask in filetypes:
        fto = FileTypeObject(filemask)
        
        if fto.isAll(): 
            ALL_filetypes_was_specified = True # remember this
            
        if fto == initialFileTypeObject:
            initialFileTypeObject.add(fto) # add fto to initialFileTypeObject
        else:
            filetypeObjects.append(fto)

    #------------------------------------------------------------------
    # make sure that the list of filetypes includes the ALL FILES type.
    #------------------------------------------------------------------
    if ALL_filetypes_was_specified: 
        pass
    elif allFileTypeObject == initialFileTypeObject:
        pass
    else:
        filetypeObjects.insert(0,allFileTypeObject)
    #------------------------------------------------------------------
    # Make sure that the list includes the initialFileTypeObject
    # in the position in the list that will make it the default.
    # This changed between Python version 2.5 and 2.6
    #------------------------------------------------------------------ 
    if len(filetypeObjects) == 0:
        filetypeObjects.append(initialFileTypeObject)

    if initialFileTypeObject in (filetypeObjects[0], filetypeObjects[-1]):
        pass
    else:
        filetypeObjects.insert(0,initialFileTypeObject)     
        
    filetypes = [fto.toTuple() for fto in filetypeObjects]

    return initialbase, initialfile, initialdir, filetypes

#-----------------------------------------------------------------------
#
# test/demo easygui
#
#-----------------------------------------------------------------------
def _dummy():
    pass

