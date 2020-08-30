from rpw.ui.forms import FlexForm, Button
import os

class draw:
    def __init__(self,filename):
        self.filename = filename
    
    def fgui(self):
        self.components = [Button("Open Excel",
                             on_click=self.openwb_conf),
                      Button("run",
                             on_click= self.run_gird)
                    ]
    def openwb_conf(self,sender, e):
        """
        open excel file by input path
        """
        self.form.close()
        os.startfile(self.filename)
    def run_gird(self,sender, e):
        """
        drawing gird by parameter from excel 
        """
        self.form.close()
        self.f()
        
    def __call__(self,f):
        self.f  = f 
        def wrapped_f(*args):
            self.fgui()
            self.form = FlexForm('DGrid', self.components) 
            self.form.show() 
        return wrapped_f 