from Tkinter import *
import urllib
import urllib2
import sgmllib
import tkMessageBox

class TranstParser(sgmllib.SGMLParser):
    def __init__(self):
        sgmllib.SGMLParser.__init__(self)
        self.results=[]
        self.indata=False

    def start_div(self,attrs):
        divs=[v for k,v in attrs if k=='id']

        if 'result_box' in divs:
            self.indata=True
            

    def handle_data(self,data):
        if self.indata:
            self.results.append(data)
            self.indata=False

class Application(Frame):
    def __init__( self, master=None):
        Frame.__init__( self, master)
        self.grid()
        self.input_text = StringVar(  )
        self.output_text = StringVar( )
        
        self.CreateWidgets()
        
        
    def CreateWidgets(self):
        self.Msg1 = Label( text = 'Input Word to Translate:' )
        self.Msg1.grid( row = 0, sticky = W , padx = 5)
        
        self.InputText = Entry( textvariable = self.input_text, width = 50  )
        self.InputText.grid( row =2, padx =5 )
        
        self.TranslateButton = Button( text = 'Translate', command = self.Translate)
        self.TranslateButton.grid( row =3, sticky = E, padx = 5, pady = 5)
        
        self.OutputText = Entry( textvariable = self.output_text, width = 50 )
        self.OutputText.grid( row=4)
        
        
        self.QuitButton = Button( text = 'Quit', command = self.quit )
        self.QuitButton.grid( row = 5, sticky = E, padx =5, pady =5 )
        
    def Translate(self):
        lin = 'en'
        lout = 'zh_CN'
        #lout = 'en'
        #text = 'flesh'
        text = self.input_text.get()
        
        if len(text)>0:
            req_data={"hl":"zh-cn","ie":"UTF-8",'text':text,"langpair":"%s|%s" % (lin,lout)}
            req_url='http://translate.google.cn/translate_t'
            
            data=urllib.urlencode(req_data)
            req=urllib2.Request(req_url,data)
            
            req.add_header('User-Agent','Mozilla/4.0')
            data=urllib2.urlopen(req).read()
            #print data
            
            tp=TranstParser()
            tp.feed(data)
            
            for a in tp.results:
                #print a
                self.output_text.set(a.decode('gbk','utf-8'))
        else:
            tkMessageBox.showwarning("Google Translate","You must input a word to translate!")
        
        
        
app = Application( )
app.master.title = 'Goolge Translate'
#app.setSize( 300,400)
app.mainloop()