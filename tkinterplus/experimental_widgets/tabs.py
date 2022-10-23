from tkinter import Frame, Tk, StringVar, Button

#NOTE This widget is still being worked on. Expect issues for missing features!
class Tabs(Frame):
    def __init__(self,master:Tk=None,textvariable:StringVar=None,**kw):
        """WIP"""
        self.master=master
        self._row=0
        self._column=0
        self._widgets={}

        Frame.__init__(self,master,bg='red',width=100,height=100,**kw)

        self._tabs = Frame(self,bg='blue')
        self._tabs.id='no_del'
        self._tabs.grid(row=0,column=0)


    def _test(self,value:str):
        print('Tab: ',self._widgets[value])

        self._widgets[value].grid(row=1,column=0)

    def add_tab(self,label:str,value:str,widget=None,command=None):
        self._widgets[value] = widget
        self._widgets[value].id = 'del'
        Button(self._tabs, text=label,command=lambda: self._test(value)).grid(row=self._row,column=self._column)
        self._column+=1

    # NOT ADDED

    def config(self,**kw):
        """Not addedd yet"""
        pass
    