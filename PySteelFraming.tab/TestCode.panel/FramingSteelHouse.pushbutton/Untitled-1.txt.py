import time
from System.Windows import Application, Window
from time import localtime
class MyWindow(Window):

    someMember = None   

    def __init__(self):
    wpf.LoadComponent(self, 'test.xaml')
    self.someMember = "Hello World"

    @property
    def SomeMember(self):
        return self.someMember 

    @psetter.SomeMember
    def SomeMember(self, value):
        self.someMember = value 


if __name__ == '__main__':
Application().Run(MyWindow())
time1()