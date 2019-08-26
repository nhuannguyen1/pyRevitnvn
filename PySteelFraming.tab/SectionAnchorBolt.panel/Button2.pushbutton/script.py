__doc__ = "Test run Form with button"
__author__ = 'HO VAN CHUONG'
__title__ = 'Button Click'
# -*- coding: UTF-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
import System.Drawing
import System.Windows.Forms
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
from System.Drawing import *
from System.Windows.Forms import *
from Autodesk.Revit.UI.Selection import ObjectType
import rpw
from rpw import revit
doc = revit.doc
uidoc = revit.uidoc

from event import CustomizableEvent
def delete_elements():
	pick1 = uidoc.Selection.PickObject(ObjectType.Element)
	t = Transaction (doc,"Delete Element")
	t.Start()
	doc.Delete(pick1.ElementId)
	t.Commit()
def selectedobj():
	Nameobj = []
	picks = uidoc.Selection.PickObjects(ObjectType.Element)
	for  pick in picks:
		eleid = pick.ElementId
		ele = doc.GetElement(eleid)
		Nameobj.append(ele.Category.Name)
	MessageBox.Show(str(Nameobj),"Result")
	delete_allelement()
def delete_allelement():
	pick1 = uidoc.Selection.PickObjects(ObjectType.Element)
	t = Transaction (doc,"Delete Element")
	t.Start()
	for i in pick1:
		doc.Delete(i.ElementId)
	t.Commit()
customizable_event = CustomizableEvent()
class MainForm(Form):
	def __init__(self):
		self.InitializeComponent()
	def InitializeComponent(self):
		self._button1 = System.Windows.Forms.Button()
		self._button2 = System.Windows.Forms.Button()
		self.SuspendLayout()
		# 
		# button1
		# 
		self._button1.Location = System.Drawing.Point(118, 50)
		self._button1.Name = "button1"
		self._button1.Size = System.Drawing.Size(75, 23)
		self._button1.TabIndex = 0
		self._button1.Text = "button1"
		self._button1.UseVisualStyleBackColor = True
		self._button1.Click += self.button1
		# 
		# button2
		# 
		self._button2.Location = System.Drawing.Point(118, 126)
		self._button2.Name = "button2"
		self._button2.Size = System.Drawing.Size(75, 23)
		self._button2.TabIndex = 1
		self._button2.Text = "button2"
		self._button2.UseVisualStyleBackColor = True
		self._button2.Click += self.button2 
		# 
		# MainForm
		# 
		self.ClientSize = System.Drawing.Size(284, 261)
		self.Controls.Add(self._button2)
		self.Controls.Add(self._button1)
		self.Name = "MainForm"
		self.Text = "Name Program"
		self.ResumeLayout(False)
	def button1(self, sender, e):
		customizable_event.raise_event(selectedobj)
	def button2(self, sender, e):
		customizable_event.raise_event(delete_elements)
d= MainForm()
d.Show()
