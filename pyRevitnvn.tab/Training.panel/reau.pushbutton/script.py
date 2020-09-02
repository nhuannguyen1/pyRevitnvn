"""
TESTED REVIT API: 2019
"""
__doc__ = 'automation revit'
__author__ = 'pyan.vn'

import math
import rpw
from Autodesk.Revit.DB import (ElementId,
                               XYZ,
                               Line,
                               Structure,
                               CurveArray,
                               Wall,
                               HostObjectUtils,
                               ShellLayerType,
                               Plane,
                               ElementTransformUtils
                               
                               )
import Autodesk.Revit.UI.Selection
from Autodesk.Revit.DB import Transaction 
from rpw.ui.forms import (Console, 
                          FlexForm, 
                          Label,
                          ComboBox, 
                          TextBox, 
                          TextBox, 
                          CheckBox, 
                          Separator, 
                          Button
                          )
from pyrevitnvn.units import Convert_length,Convert_Display_length_To_Internal
from pyrevitnvn.reauto import get_edges_lines_corners_main,plot_design_cordninates

doc = __revit__.ActiveUIDocument.Document
tt = Transaction(doc, "Retail Automation")

#UI form organization
components_1 = [Label('SUITE EXTENTS'),
              Label('Bays Length'),
			  TextBox('textbox1', Text="4000, 5000, 6000, 7000, 4000, 5000, 4500"),
              Label('Bays Width'),
			  TextBox('textbox2', Text="2000, 4000, 4000, 5000, 4000"),  
              Label('Wall Heights'),
			  TextBox('textbox3', Text="7000"),
              Label('Ceiling Heights'),
			  TextBox('textbox4', Text="7000"),
              Label('Storefront Distance From Front'),
			  TextBox('textbox5', Text="5000"),
			  CheckBox('checkbox1', 'Rear Left Door'),
			  CheckBox('checkbox2', 'Rear Right Door'),
			  Separator(),
			  Button('Go')
              ]

components_2 = [Label('FURNITURE & FIXTURES'), 
			  Label('Shelving Type:'),
			  ComboBox("combobox1", {"Small": "2000x1200x300mm", "Medium": "2000x2000x300mm", "Large": "2000x2500x300mm"}), 
			  Label('Table Type:'),
			  ComboBox("combobox2", {"Small": "1200x760x760mm", "Medium": "1800x760x760mm", "Large": "2500x750x750mm"}), 
              Label('#Tables Length'),
			  TextBox('textbox6', Text="4"),              
              Label('Tables Lengthwise Spacing'),
			  TextBox('textbox7', Text="7000"),
              Label('#Tables Width'),
			  TextBox('textbox8', Text="4"),
              Label('Tables Widthwise Spacing'),
			  TextBox('textbox9', Text="5000"),
			  Separator(),
			  Button('Go')]

components_3 = [Label('FURNITURE & FIXTURES'), 
              Label('Tables Offset From Front'),
			  TextBox('textbox10', Text="5000"),
			  Label('Back Television Family:'),
			  ComboBox("combobox3", {"Small": "2540", "Medium": "3810", "Large": "5080"}), 
			  Label('Primary Lighting Fixture:'),
			  ComboBox("combobox4", {"Linear Short": "1200 - 120V", "Linear Long": "900 - 120V", "Pendant": "Pendant"}), 
			  Label('Secondary Light Fixture:'),
			  ComboBox("combobox5", {"Linear Short": "1200 - 120V", "Linear Long": "900 - 120V", "Pendant": "Pendant"}), 
			  Separator(),
			  Button('Go')
              ]

form_1 = FlexForm("Retail Layout", components_1)
form_2 = FlexForm("Retail Layout", components_2)
form_3 = FlexForm("Retail Layout", components_3)

form_1.show()
form_2.show()
form_3.show()

#Form Inputs
shelvingType = form_2.values["combobox1"]
tableType = form_2.values["combobox2"]
tvType = form_3.values["combobox3"]
primLight = form_3.values["combobox4"]
secLight = form_3.values["combobox5"]

wall_height = Convert_Display_length_To_Internal(float(form_1.values["textbox3"]))

lcp_height = Convert_Display_length_To_Internal(float(form_1.values["textbox4"]))

sf_dist = Convert_Display_length_To_Internal(float(form_1.values["textbox5"]))


rr_lf_dr = form_1.values["checkbox1"]
rr_rt_dr = form_1.values["checkbox2"]

tables_ln = int(form_2.values["textbox6"])

tables_sp_ln = Convert_Display_length_To_Internal(float(form_2.values["textbox7"]))

tables_wd = int(form_2.values["textbox8"])

tables_sp_wd = Convert_Display_length_To_Internal(float(form_2.values["textbox9"]))

tb_offset = Convert_Display_length_To_Internal(float(form_3.values["textbox10"]))

#Identify Shelving to Place
if shelvingType == "2000x1200x300mm":
	shelvingTypeId = ElementId(37980)
elif shelvingType == "2000x2000x300mm":
	shelvingTypeId = ElementId(37953)
elif shelvingType == "2000x2500x300mm":
	shelvingTypeId = ElementId(2918)
shlv_type = doc.GetElement(shelvingTypeId)

#Identify Tables to Place
if tableType == "1200x760x760mm":
	tableTypeId = ElementId(38007)
elif tableType == "1800x760x760mm":
	tableTypeId = ElementId(2916)
elif tableType == "2500x750x750mm":
	tableTypeId = ElementId(38033)
table_type = doc.GetElement(tableTypeId)

#Identify Television to Place
if tvType == "2540":
	tvTypeId = ElementId(38063)
elif tvType == "3810":
	tvTypeId = ElementId(38073)
elif tvType == "5080":
	tvTypeId = ElementId(2921)
tv_wall = doc.GetElement(tvTypeId)

#Identify Primary Light Fixture to Place
if primLight == "1200 - 120V":
	primLightId = ElementId(2920)
elif primLight == "900 - 120V":
	primLightId = ElementId(38126)
elif primLight == "Pendant":
	primLightId = ElementId(2923)
primary_light = doc.GetElement(primLightId)

#Identify Secondary Light Fixture to Place
if secLight == "1200 - 120V":
	secLightId = ElementId(2920)
elif secLight == "900 - 120V":
	secLightId = ElementId(38126)
elif secLight == "Pendant":
	secLightId = ElementId(2923)
second_light = doc.GetElement(secLightId)

#Level Inputs
levelId = ElementId(13999)
level = doc.GetElement(levelId)

#List spacing of grids from front to back. The number of entries determine the number of master grid lines

string_list1 = form_1.values["textbox1"]

#List spacing of grids from left to right

string_list2 = form_1.values["textbox2"]

list1_tp = [float(i) for i in string_list1.split(',')]
list2_tp = [float(i) for i in string_list2.split(',')]

list1 = list(map(Convert_length,list1_tp))
list2 = list(map(Convert_length,list2_tp))

# 3D plot edges, plot lines and corners
edges, lines, corners = get_edges_lines_corners_main(list1, list2, do_3d=False)
 
ocorner_x1=corners[0][0]
ocorner_y1=corners[0][1]
ocorner_x2=corners[1][0]
ocorner_y2=corners[1][1]
ocorner_x3=corners[3][0]
ocorner_y3=corners[3][1]
ocorner_x4=corners[2][0]
ocorner_y4=corners[2][1]

corner_x1=ocorner_x1-(ocorner_x1+ocorner_x4)
corner_y1=ocorner_y1-((ocorner_y1+ocorner_y2)/2)
corner_x2=ocorner_x2-(ocorner_x1+ocorner_x4)
corner_y2=ocorner_y2-((ocorner_y1+ocorner_y2)/2)
corner_x3=ocorner_x3-(ocorner_x1+ocorner_x4)
corner_y3=ocorner_y3-((ocorner_y1+ocorner_y2)/2)
corner_x4=ocorner_x4-(ocorner_x1+ocorner_x4)
corner_y4=ocorner_y4-((ocorner_y1+ocorner_y2)/2)

#Setting point locations
pt1 = XYZ(corner_x1, corner_y1, 0)
pt2 = XYZ(corner_x2, corner_y2, 0)
pt3 = XYZ(corner_x3, corner_y3, 0)
pt4 = XYZ(corner_x4, corner_y4, 0)

tt.Start()

#Divider strips
div_stripId = ElementId(2836)
divider_strip = doc.GetElement(div_stripId)

for i in plot_design_cordninates(list1[0:-2]):
	dv1_start = XYZ(i-(ocorner_x1+ocorner_x4), corner_y1, 0)
	dv1_end = XYZ(i-(ocorner_x1+ocorner_x4), corner_y2, 0)
	dv1_line = Line.CreateBound(dv1_start, dv1_end) 
	create_dv1 = doc.Create.NewFamilyInstance(dv1_line, divider_strip, level, Structure.StructuralType.NonStructural)

dv1b_start = XYZ(corner_x3+0.3333, corner_y1, 0)
dv1b_end = XYZ(corner_x4+0.3333, corner_y2, 0)
dv1b_line = Line.CreateBound(dv1b_start, dv1b_end) 
create_dv1b = doc.Create.NewFamilyInstance(dv1b_line, divider_strip, level, Structure.StructuralType.NonStructural)
	
for i in plot_design_cordninates(list2[0:-1]):
	dv2_start = XYZ(corner_x1, i-((ocorner_y1+ocorner_y2)/2), 0)
	dv2_end = XYZ(corner_x4, i-((ocorner_y1+ocorner_y2)/2), 0)
	dv2_line = Line.CreateBound(dv2_start, dv2_end) 
	create_dv2 = doc.Create.NewFamilyInstance(dv2_line, divider_strip, level, Structure.StructuralType.NonStructural)

#Floor
floor_typeId = ElementId(2915)
floor_type = doc.GetElement(floor_typeId)

profile = CurveArray()

profile.Append(Line.CreateBound(pt1, pt2))
profile.Append(Line.CreateBound(pt2, pt3))
profile.Append(Line.CreateBound(pt3, pt4))
profile.Append(Line.CreateBound(pt4, pt1))

create_floor = doc.Create.NewFloor(profile, floor_type, level, Structure.StructuralType.NonStructural)

tt.Commit()

tt.Start()

#Shelving walls
ext_wall_typeId = ElementId(2835)
ext_wall_type = doc.GetElement(ext_wall_typeId)
ext_wall_width = ext_wall_type.Width
ext_wall_width_hf = ext_wall_width/2

pt1b = XYZ(corner_x1, corner_y1-ext_wall_width_hf, 0)
pt2b = XYZ(corner_x2, corner_y2+ext_wall_width_hf, 0)
pt3b = XYZ(corner_x4, corner_y4-ext_wall_width_hf, 0)
pt4b = XYZ(corner_x3, corner_y3+ext_wall_width_hf, 0)
pt1c = XYZ(corner_x1-ext_wall_width_hf, corner_y1, 0)
pt2c = XYZ(corner_x2-ext_wall_width_hf, corner_y2, 0)

shlv_lf_wall = Line.CreateBound(pt3b, pt1b) 
shlv_rt_wall = Line.CreateBound(pt4b, pt2b) 

shlv_lf_create = Wall.Create(doc, shlv_lf_wall, ext_wall_type.Id, level.Id, wall_height, 0, True, False)
shlv_rt_create = Wall.Create(doc, shlv_rt_wall, ext_wall_type.Id, level.Id, wall_height, 0, False, False)

#Back walls
back_md_pt = (corner_y1+corner_y2)/2
back_wall = Line.CreateBound(pt1c, pt2c) 
back_create = Wall.Create(doc, back_wall, ext_wall_type.Id, level.Id, wall_height, 0, False, False)
		
#Storefront wall
sf_wall_type = ElementId(2832)

storefront_lfx_pt = corner_x4-sf_dist
storefront_rtx_pt = corner_x3-sf_dist

pt8 = XYZ(storefront_lfx_pt, corner_y4, 0)
pt9 = XYZ(storefront_rtx_pt, corner_y3, 0)

storefront_wall = Line.CreateBound(pt8, pt9) 

sf_create = Wall.Create(doc, storefront_wall, sf_wall_type, level.Id, lcp_height, 0, False, False)

#Place tables & Shelves
tb_len = table_type.LookupParameter('Length').AsDouble()
tb_wd = table_type.LookupParameter('Width').AsDouble()

shlv_depth = shlv_type.LookupParameter('Depth').AsDouble()
	
tb_array_cenx = (tables_ln-1)*(tables_sp_ln-tb_len)
tb_array_ceny = (tables_wd*tb_wd)+(tables_wd-1)*(tables_sp_wd-tb_wd)

shlv_list=[]

for i in range(0,int(tables_ln)):
	tb_x = (i*tables_sp_ln)+corner_x4-(tables_ln*tb_len)-tb_array_cenx-tb_offset
	for j in range(0,int(tables_wd)):
		tb_y = (j*tables_sp_wd)+back_md_pt-(tb_array_ceny/2)
		loc = XYZ(tb_x, tb_y, 0) 
		place_tables = doc.Create.NewFamilyInstance(loc, table_type, Structure.StructuralType.NonStructural)

	shlv_yoffset = corner_y2-(shlv_depth/2)
	shlv2_loc = XYZ(tb_x, shlv_yoffset, 0)

	place_shlv2 = shlv_list.append(doc.Create.NewFamilyInstance(shlv2_loc, shlv_type, shlv_rt_create, Structure.StructuralType.NonStructural))

#Place television wall
vwall_loc = XYZ(corner_x1, back_md_pt, 1.5)
place_vwall = doc.Create.NewFamilyInstance(vwall_loc, tv_wall, XYZ(0,1,0), back_create, Structure.StructuralType.NonStructural)

tt.Commit()

#Start Transaction
tt.Start()

#Place Shelves
shlvy_offset = (corner_y2-corner_y1)/2

reference = HostObjectUtils.GetSideFaces(shlv_lf_create, ShellLayerType.Exterior)

face = shlv_lf_create.GetGeometryObjectFromReference(reference[0])

bboxMin = face.GetBoundingBox().Min
   
plane = Plane.CreateByNormalAndOrigin(face.ComputeNormal(bboxMin), face.Evaluate(bboxMin).Add(XYZ(0, shlvy_offset, 0)))

for i in shlv_list:
	place_shlv1 = ElementTransformUtils.MirrorElement(doc, i.Id, plane)

#Rear doors
rear_drId = ElementId(2926)
rear_dr = doc.GetElement(rear_drId)

rr_lf_offset = corner_y1+1.6667
rr_rt_offset = corner_y2-1.6667

rr_lf_loc = XYZ(corner_x1, rr_lf_offset, 0) 
rr_rt_loc = XYZ(corner_x2, rr_rt_offset, 0) 

if rr_lf_dr == True:
	place_rr_lf = doc.Create.NewFamilyInstance(rr_lf_loc, rear_dr, back_create, Structure.StructuralType.NonStructural)
	rl_flip_face = place_rr_lf.flipFacing()
	rl_flip_hand = place_rr_lf.flipHand()	

if rr_rt_dr == True:
	place_rr_rt = doc.Create.NewFamilyInstance(rr_rt_loc, rear_dr, back_create, Structure.StructuralType.NonStructural)
	rr_flip_face = place_rr_rt.flipFacing()

    #LCP Panels
lcpId = ElementId(2833)
lcp = doc.GetElement(lcpId)

def lcpy(list_values):
	new_list_cor = []
	sum_val=0
	for i in list_values:
		sum_val += i
		new_list_cor.append(float(sum_val-(i/2)))
	return new_list_cor

def replace_element(lst, new_element, indices):
	for i in indices:
		lst[i] = new_element
	return lst
	
lcp_list2 = lcpy(list2)	
st_panel_yloc = lcp_list2[0]+0.0989583333
ed_panel_yloc = lcp_list2[-1]-0.0989583333
lcp_list2 = replace_element(lcp_list2, st_panel_yloc, [0])
lcp_list2 = replace_element(lcp_list2, ed_panel_yloc, [-1])
	
lcp_list=[]

#Store Dimensions
store_len = corner_x1-corner_x4
store_wd = corner_y2-corner_y1

for i in lcp_list2:
	lcp_loc = XYZ((store_len/2)-(sf_dist/2), i-((ocorner_y1+ocorner_y2)/2), lcp_height-12) 
	create_lcp = lcp_list.append(doc.Create.NewFamilyInstance(lcp_loc, lcp, Structure.StructuralType.NonStructural))

tt.Commit()

# Get and Set LCP dimension parameters

length = corner_x4-corner_x1-sf_dist-0.895833
width = list2[1]-0.5

#Start Transaction
tt.Start()

for i in lcp_list:
	l_param = i.GetParameters('Length')
	for j in l_param:
		j.Set(length)      

for i in lcp_list:
	l_param = i.GetParameters('Width')
	for j in l_param:
		j.Set(width)  
					
#Place primary lights and referenced elements
for i in plot_design_cordninates(list2[0:-1]):
	for j in range(0,int(tables_ln)):
		ttr_x = (j*tables_sp_ln)+corner_x4-(tables_ln*tb_len)-tb_array_cenx-tb_offset+(tb_len/2)
		ttr_loc = XYZ(ttr_x, i-((ocorner_y1+ocorner_y2)/2), lcp_height) 
		place_ttr= doc.Create.NewFamilyInstance(ttr_loc, primary_light, Structure.StructuralType.NonStructural)		

#Place secondary lights and referenced elements
for i in plot_design_cordninates(list2[0:-1]):
	for j in range(0,int(tables_ln-1)):
		str_x = j*int(tables_sp_ln)+corner_x4-(tables_ln*tb_len)-tb_array_cenx-tb_offset+(tb_len/2)+(tables_sp_ln/2)
		str_loc = XYZ(str_x, i-((ocorner_y1+ocorner_y2)/2), lcp_height) 
		place_str= doc.Create.NewFamilyInstance(str_loc, second_light, Structure.StructuralType.NonStructural)	
        
#Stop Transaction
tt.Commit()