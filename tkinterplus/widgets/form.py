from tkinter import W, CENTER, E, filedialog, BooleanVar, Entry, Text, IntVar, Radiobutton, Checkbutton, StringVar, OptionMenu, Button, Frame, Tk, Label
import os

from .. import Picture

class Form(Frame):
    def __init__(self,parent:Tk,title=None,description=None,tearoff=False):
        Frame.__init__(self,parent)
        self.row=0
        self.column=0
        if title:
            Label(self,text=title,font=('bold',12)).grid(row=0,column=0,sticky=W)
            self._size(1)
            if description:
                Label(self,text=description).grid(row=1,column=0,sticky=W)
                self._size(1)

    def _size(self,row=None,colum=None):
        """The size of the form item"""
        if row: self.row+=row
        if colum: self.column+=colum
        return self.row, self.column

    def _Button(self,name,command=None):
        """Internal function"""
        r,c=self._size()
        Button(self,text=name,command=command).grid(row=r,column=c,sticky=W)
        self._size(1)
        
    def _Label(self,text,font=None):
        """Internal function"""
        r,c=self._size()
        Label(self,text=text,font=font).grid(row=r,column=c,sticky=W)
        self._size(1)

    def _upload(self,multiple,size,**kw):
        """Internal function"""
        def checkSize(p):
            if size < os.path.getsize(p):
                print('File too large! max: %s bytes'%(size))

        if type(multiple) == bool:
            if multiple==True:
                path = filedialog.askopenfilenames(**kw)
                for i in path:
                    checkSize(i)
            else:
                path = filedialog.askopenfilename(**kw)
                checkSize(path)
       
    def add_radio(self,question,*options):
        """Add multiple choice"""
        self._Label(question)
        tmp=IntVar()
        tmp.set(0)
        count=0
        for option in options:
            r,c=self._size()
            Radiobutton(self,text=option,variable=tmp,value=count).grid(row=r,column=c,sticky=W)
            count+=1
            self._size(1)

    def add_checkbox(self,question,*options):
        """Add checkbox"""
        self._Label(question)
        for option in options:
            r,c=self._size()
            Checkbutton(self,text=option).grid(row=r,column=c,sticky=W)
            self._size(1)

    def add_dropdown(self,question,*options):
        """Add dropdown list"""
        self._Label(question)
        test=StringVar()
        test.set('Choose')
        r,c=self._size()
        OptionMenu(self,test,*options).grid(row=r,column=c,sticky=W)
        self._size(1)
        
    def add_file(self,question,filetypes=None,multiple=False,maxsize=None):
        """Add file upload"""
        self._Label(question)

        def convert(type):
            """Converts type to a list of all the ext name"""
            if type=='document':
                return ' *.text *.txt'
            elif type=='spreadsheet':
                return ' *.xls *.xlsx'
            elif type=='pdf':
                return ' *.pdf'
            elif type=='video':
                return ' *.3gp *.3g2 *.avi *.m4v *.mp4 *.mpg *.mpeg *.ogm *.ogv *.mov *.webm *.m4v *.mkv *.asx *.wm *.wmv *.wvx *.avi'
            elif type=='image':
                return ' *.bmp *.gif *.heic *.heif *.pjp *.jpg *.pjpeg *.jpeg *.jfif *.png *.tif *.tiff *.ico *.webp'
            elif type=='audio':
                return ' *.flac *.mid *.mp3 *.m4a *.opus *.ogg *.oga *.wav'
            else:
                print('Unknown filetype "%s"'%(i))
                return '*.*'

        if type(filetypes) == list:
            if type(filetypes[0]) == str:
                out = ''
                for i in filetypes:
                    out+=convert(i)
                filetype = [('Custom Files', out),('All files','*.*')]
            elif type(filetypes[0]) == tuple:
                filetype = filetypes
        elif type(filetypes) == str:
            filetype = [('Custom Files', convert(filetypes)),('All files','*.*')]
        self._Button('Add file',lambda: self._upload(multiple,maxsize,filetypes=filetype))
        self._size(1)
        
    def add_linear_scale(self,question,from_=1,to=5,start=None,end=None):
        """Add linear scale"""
        self._Label(question)
        r,c=self._size()
        scale = Frame(self)
        SCALE = IntVar()
        count=from_
        for i in range(to):
            Label(scale,text=str(count),justify=CENTER).grid(row=0,column=i+1)
            Radiobutton(scale,variable=SCALE,value=count,justify=CENTER).grid(row=1,column=i+1)
            count+=1
        Label(scale,text=start).grid(row=1,column=0,sticky=E)
        Label(scale,text=end).grid(row=1,column=to+1,sticky=W)
        scale.grid(row=r,column=c,sticky=W)
        self._size(1)

    def add_radio_grid(self,question,row,column):
        """Add multiple choice grid"""
        self._Label(question)
        r,c=self._size()

        grid = Frame(self)

        values=[]

        countr=0
        countc=0
        for rr in row:
            Label(grid,text=rr).grid(row=countr+1,column=0)
            values.append(IntVar())
            values[countr].set(-1)
            countr+=1
        for cc in column:
            Label(grid,text=cc).grid(row=0,column=countc+1)
            countc+=1

        countrr=0
        for rr in row:
            countcc=0
            for cc in column:
                Radiobutton(grid,variable=values[countrr],value=countcc).grid(row=countrr+1,column=countcc+1)                
                countcc+=1
            countrr+=1
        grid.grid(row=r,column=c,sticky=W)
        self._size(1)

    def add_checkbox_grid(self,question,row,column):
        """Add checkbox grid"""
        self._Label(question)
        r,c=self._size()

        grid=Frame(self)

        values=[]

        countr=0
        countc=0
        for rr in row:
            Label(grid,text=rr).grid(row=countr+1,column=0)
            countr+=1
        for cc in column:
            Label(grid,text=cc).grid(row=0,column=countc+1)
            countc+=1

        for temp in range(len(row+column)+3):
            values.append(BooleanVar())
            values[temp].set(False)

        countrr=0
        total=0
        for rr in row:
            countcc=0
            for cc in column:
                Checkbutton(grid,variable=values[total],onvalue=True,offvalue=False).grid(row=countrr+1,column=countcc+1)                
                countcc+=1
                total+=1
            countrr+=1

        grid.grid(row=r,column=c,sticky=W)
        self._size(1)

    def add_short_answer(self,question):
        """Add short answer"""
        self._Label(question)
        r, c = self._size()
        # Label(self,text=question).grid(row=r,column=c,sticky=W)
        Entry(self).grid(row=r+1,column=c,sticky=W)
        self._size(2)

    def add_paragraph(self,question):
        """Add paragraph"""
        self._Label(question)
        r, c = self._size()
        # Label(self,text=question).grid(row=r,column=c,sticky=W)
        Text(self,width=16,height=1).grid(row=r+1,column=c,sticky=W)
        self._size(2)

    def add_title(self,title,description=None):
        """Add title and description""" 
        if title:
            self._Label(title)
            if description:
                self._Label(description)

    def add_image(self,file,title=None,**kw):
        """Add image"""
        if title:
            self._Label(title)
        r, c = self._size()
        Picture(self,file,**kw).grid(row=r,column=c,sticky=W)
        self._size(1)

    def add_submit_button(self,command):
        """Add submit button"""
        self._Button('Submit',command)

    def add_reset_button(self,command):
        """Add reset button"""
        self._Button('Clear from',command)
