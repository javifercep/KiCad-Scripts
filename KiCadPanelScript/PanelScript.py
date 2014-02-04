#!/usr/bin/env python
import sys
from pcbnew import *


def Min(coor):
    #print "This is a function"
    minP = wxPoint(300000000,300000000)
    for index in range(0,3):
        if coor[index].x < minP.x:
            minP.x=coor[index].x
        if coor[index].y < minP.y:
            minP.y=coor[index].y
    print "X min: %u, Y min: %u"%(minP.x,minP.y)
    return minP

def Max(coor):
    #print "Calculating"
    maxP = wxPoint(0,0)
    
    for index in range(0,3):
        if coor[index].x > maxP.x:
            maxP.x=coor[index].x
        if coor[index].y > maxP.y:
            maxP.y=coor[index].y
    print "X max: %u, Y max: %u"%(maxP.x,maxP.y)
    return maxP

def Panel(MaxCoor, MinCoor , xdist, ydist, panelType = "SQUA"):
    print "STARTING..."
    print ""
    
    index = long(0)
    indey = long(0)
    xdist = long(xdistance*1000000)
    ydist = long(ydistance*1000000)
    coor = wxPoint(0,0)
    
    if panelType == "SQUA":
        for module in pcb.GetModules():
            modcoor = module.GetPosition()
            print "* Modulimpore: %s at %s"%(module.GetReference(),ToUnits(modcoor))
            if MinCoor.x + xdist/2 +xdist*index < MaxCoor.x:
                coor.Set(MinCoor.x + xdist/2 +xdist*index, MinCoor.y + ydist/2 + ydist*indey)
                module.SetPosition(coor)
                print "* Module %s moved at %s"%(module.GetReference(),ToUnits(coor))
                index+=1
            else:
                index=0
                indey+=1
                if MinCoor.y + ydist/2 + ydist*indey < MaxCoor.y:
                    coor.Set(MinCoor.x + xdist/2 +xdist*index, MinCoor.y + ydist/2 + ydist*indey)
                    module.SetPosition(coor)
                    print "* Module %s moved at %s"%(module.GetReference(),ToUnits(coor))
                    index+=1
                else:
                    break;
                
    elif panelType == "TRIAN":
        rotate = 0
        line=(indey+rotate)%2
        for module in pcb.GetModules():
            modcoor = module.GetPosition()
            if rotate == 1:
                module.Rotate(modcoor,1800.0)
            print "* Module %s at %s"%(module.GetReference(),ToUnits(modcoor))
            if MinCoor.x + xdist/2*(1+line) +xdist*index < MaxCoor.x:
                coor.Set(MinCoor.x + xdist/2*(1+line) +xdist*index, MinCoor.y + ydist/2 + ydist*indey)
                module.SetPosition(coor)
                print "* Module %s moved at %s"%(module.GetReference(),ToUnits(coor))
                index+=1
            else:
                index=0
                indey+=1
                line=(indey + rotate)%2
                if MinCoor.y + ydist/2 + ydist*indey < MaxCoor.y:
                    coor.Set(MinCoor.x + xdist/2*(1+line) +xdist*index, MinCoor.y + ydist/2 + ydist*indey)
                    module.SetPosition(coor)
                    print "* Module %s moved at %s"%(module.GetReference(),ToUnits(coor))
                    index+=1
                else:
                    if rotate == 0:
                        rotate = 1
                        index = 0
                        indey = 0
                        line = (indey+rotate)%2
                    else:
                        print ""
                        print "FINISHED"
                        break
                        
    else:
        print "Sorry! You have a problem..."
            
    return 0

#Get Arguments
#TODO: Arguments control
filename=sys.argv[1]
pcb = LoadBoard(filename)

xdistance = int(sys.argv[2]) #Get X distance between modules
ydistance = int(sys.argv[3]) # Get Y distance between modules
typePanel = sys.argv[4]

ToUnits=ToMils
FromUnits=FromMils


print ""
print "LISTING DRAWINGS:"
coor = []
for item in pcb.GetDrawings():
    if type(item) is TEXTE_PCB:
        print "* Text:    '%s' at %s"%(item.GetText(),item.GetPosition())
    elif type(item) is DRAWSEGMENT:
        print "* Drawing: %s in layer %s"%(item.GetShapeStr(),item.GetLayerName()) # dir(item)
        print item.GetPosition()
        coor.append(item.GetPosition())
    else:
        print type(item)

print ""
print "Calculating edge limits..."  
MinCoor = Min(coor)
MaxCoor = Max(coor)

  
print ""
print "Moving modules:"
Panel(MaxCoor, MinCoor, xdistance, ydistance, typePanel)

print ""
print "Saving file %s"%filename
pcb.Save(filename)
print "File saved."


