#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-
'''
Curve 0 : Mapping introduce an editor mode allowing to odify all points one by one.
Curve 1 : LineX
'''

import math
import gstt
from globalVars import *
import bhorosc
import colorify
import orbits
import settings
import pygame
import numpy as np
import ast
f_sine = 0

# Curve 0

def MappingConf(section):
    global mouse_prev, sections, warpd

    gstt.EditStep = 0
    gstt.CurrentWindow = -1
    gstt.CurrentCorner = 0
    gstt.CurrentSection = section
    mouse_prev = ((405, 325), (0, 0, 0))

    # Get all shapes points (="corners") for the given section of the conf file -> gstt.Windows 
    gstt.Windows = [] 
    sections = settings.MappingSections()

    print ""
    #print "Sections : ", sections
    print "Reading Section : ", sections[gstt.CurrentSection]

    gstt.Laser = settings.MappingRead([sections[gstt.CurrentSection],'laser'])
    print "Laser : ", gstt.Laser
    gstt.simuPL = gstt.Laser

    for Window in xrange(settings.Mapping(sections[gstt.CurrentSection])-1):
        print "Reading option :  ", str(Window)
        shape = [sections[gstt.CurrentSection], str(Window)]
        WindowPoints = settings.MappingRead(shape)
        gstt.Windows.append(WindowPoints)

    print "Section points : " ,gstt.Windows

    warpd = ast.literal_eval(gstt.warpdest[gstt.Laser])
    print "warpd", warpd

print ""
print "For Mapping(), reading Architecture Points from set0.conf"

#MappingConf(1)


def Mapping(fwork, keystates, keystates_prev):
    global mouse_prev, sections, warpd

    PL = gstt.Laser
    dots = []

    #switch to edit mode Key E ?
    if keystates[pygame.K_e] and not keystates_prev[pygame.K_e] and gstt.EditStep == 0:
            print "Switching to Edit Mode"
            gstt.EditStep = 1
            gstt.CurrentWindow = 0
            gstt.CurrentCorner = 0

    # Back to normal if ENTER key is pressed ?
    if keystates[pygame.K_RETURN] and gstt.EditStep == 1:    
            
            print "Switching to Warp Mode"
            gstt.EditStep =0
            gstt.CurrentCorner = 0
            print "Laser ", gstt.Laser, "Warpd points ", gstt.warpdest[gstt.Laser]
            warpd = ast.literal_eval(gstt.warpdest[gstt.Laser])
            print warpd


    # EDIT MODE : cycle windows if press e key to adjust corner position 
    # Escape edit mode with enter key
    if gstt.EditStep >0:

        dots = []
        CurrentWindowPoints = gstt.Windows[gstt.CurrentWindow]

        # Draw all windows points or "corners"
        for corner in xrange(len(CurrentWindowPoints)):   
            dots.append(proj(int(CurrentWindowPoints[corner][0]),int(CurrentWindowPoints[corner][1]),0))
        fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False )

        # Left mouse is clicked, modify current Corner coordinate
        if gstt.mouse[1][0] == mouse_prev[1][0] and mouse_prev[1][0] == 1:
            deltax = gstt.mouse[0][0]-mouse_prev[0][0]
            deltay = gstt.mouse[0][1]-mouse_prev[0][1]
            CurrentWindowPoints[gstt.CurrentCorner][0] += (deltax *2)
            CurrentWindowPoints[gstt.CurrentCorner][1] -= (deltay * 2)

        # Change corner if Z key is pressed.
        if keystates[pygame.K_z] and not keystates_prev[pygame.K_z]:
            if gstt.CurrentCorner < settings.Mapping(sections[gstt.CurrentSection]) - 1:
                gstt.CurrentCorner += 1
                print "Corner : ", gstt.CurrentCorner

        # Press E inside Edit mode : Next window 
        if keystates[pygame.K_e] and not keystates_prev[pygame.K_e]:

            # Save current Window and switch to the next one.
            if gstt.CurrentWindow < settings.Mapping(sections[gstt.CurrentSection]) -1:
                print "saving "
                settings.MappingWrite(sections,str(gstt.CurrentWindow),CurrentWindowPoints)
                gstt.CurrentWindow += 1
                gstt.CurrentCorner = -1
                if gstt.CurrentWindow == settings.Mapping(sections[gstt.CurrentSection]) -1:
                    gstt.EditStep == 0
                    gstt.CurrentWindow = 0              
                print "Now Editing window ", gstt.CurrentWindow

        mouse_prev = gstt.mouse
        gstt.PL[PL] = fwork.LinesPL(PL)

    # Press A : Next section ?
    if keystates[pygame.K_a] and not keystates_prev[pygame.K_a]: 
            
        if gstt.CurrentSection < len(sections)-1:
        
            gstt.CurrentSection += 1
        else:
             gstt.CurrentSection = 0
        print ""
        print "switching to section ", sections[gstt.CurrentSection]
        MappingConf(gstt.CurrentSection)



    # WARP Mode
    if gstt.EditStep == 0:
        
        #print "Warp mode"
        # Left mouse is clicked, modify current Corner coordinate
        #print gstt.mouse
        if gstt.mouse[1][0] == mouse_prev[1][0] and mouse_prev[1][0] == 1:
            deltax = gstt.mouse[0][0]-mouse_prev[0][0]
            deltay = gstt.mouse[0][1]-mouse_prev[0][1]
            
            print "Laser ", gstt.Laser, " Corner ", gstt.CurrentCorner, "deltax ", deltax, "deltay", deltay
            print warpd[gstt.CurrentCorner]
            warpd[gstt.CurrentCorner][0]+= (deltax *5)
            warpd[gstt.CurrentCorner][1] += (deltay *5)
            #int(gstt.warpdest[gstt.Laser][gstt.CurrentCorner][0]) += (deltax *20)
            #int(gstt.warpdest[gstt.Laser][gstt.CurrentCorner][1]) += (deltay * 2)
            print warpd

            #print int(gstt.warpdest[gstt.Laser][gstt.CurrentCorner][0]) + (deltax * 20)
        # Change corner if Z key is pressed.
        if keystates[pygame.K_z] and not keystates_prev[pygame.K_z]:
            if gstt.CurrentCorner < 4:
                gstt.CurrentCorner += 1
                print "Corner : ", gstt.CurrentCorner


        # Display all windows to current PL for display
        Window = ([-200, -200, 0], [200, -200, 0], [200, 200, 0], [-200, 200, 0], [-200, -200, 0])

        dots = []
        for corner in xrange(len(Window)):   
            #print "Editing : ", WindowPoints[corner]
            #print Window[corner][0]
            dots.append(proj(int(Window[corner][0]),int(Window[corner][1]),0))
        
        fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False  )
    
        gstt.PL[PL] = fwork.LinesPL(PL)

        mouse_prev = gstt.mouse


    '''
    # RUN MODE
    if gstt.EditStep == 0:
        
        # Add all windows to PL for display
        for Window in gstt.Windows:  
            print Window
            dots = []
            for corner in xrange(len(Window)):   
                #print "Editing : ", WindowPoints[corner]
                #print Window[corner][0]
                dots.append(proj(int(Window[corner][0]),int(Window[corner][1]),0))
            
            fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False  )
            print dots

        gstt.PL[PL] = fwork.LinesPL(PL)

        #print gstt.PL[PL]
        #print ''
    '''

# Curve 1
def LineX(fwork):

    joypads()
    # vertical line
    dots = []
    x = cc2scrX(gstt.cc[1]+1)
    y = 0
    dots.append((int(x),int(y)))
    dots.append((int(x),int(screen_size[1])))
    #print dots
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color))

    # horizontal line
    dots = []
    y = cc2scrY(gstt.cc[2]+1)
    x = 0       
    dots.append((int(x),int(y)))
    dots.append((int(screen_size[0]),int(y)))
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color))



# Remap values in different scales i.e CC value in screen position.
def cc2scrX(s):
    a1, a2 = 0,127  
    b1, b2 = -screen_size[0]/2, screen_size[0]/2
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def cc2scrY(s):
    a1, a2 = 0,127  
    b1, b2 = -screen_size[1]/2, screen_size[1]/2
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def cc2range(s,min,max):
    a1, a2 = 0,127  
    b1, b2 = min, max
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def extracc2scrX(s):
    a1, a2 = -66000,66000  
    b1, b2 = 0, screen_size[0]
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def extracc2scrY(s):
    a1, a2 = -66000,66000 
    b1, b2 = 0, screen_size[1]
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def extracc2range(s,min,max):
    a1, a2 = -66000,66000  
    b1, b2 = min, max
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


# 3D rotation and 2D projection for a given 3D point
def proj(x,y,z):

    # Skip trigo update if angleX didn't change 
    # TODO : gstt.prev_cc29 == -1 is useful only the first time to create cosa and sina values

    if gstt.prev_cc29 != gstt.cc[29] or gstt.prev_cc29 == -1: 
        gstt.angleX += cc2range(gstt.cc[29],0,0.1)    
        rad = gstt.angleX * PI / 180
        cosaX = math.cos(rad)
        sinaX = math.sin(rad)
        prev_cc29 = gstt.cc[29]

    y2 = y
    y = y2 * cosaX - z * sinaX
    z = y2 * sinaX + z * cosaX

    # Skip trigo update if angleY didn't change 
    if gstt.prev_cc30 != gstt.cc[30]: 
        gstt.angleY += cc2range(gstt.cc[30],0,0.1)
        rad = gstt.angleY * PI / 180
        cosaY = math.cos(rad)
        sinaY = math.sin(rad)
        prev_cc30 = gstt.cc[30]

    z2 = z
    z = z2 * cosaY - x * sinaY
    x = z2 * sinaY + x * cosaY


    # Skip trigo update if angleZ didn't change 
    if gstt.prev_cc31 != gstt.cc[31]: 
        gstt.angleZ += cc2range(gstt.cc[31],0,0.1)
        rad = gstt.angleZ * PI / 180
        cosZ = math.cos(rad)
        sinZ = math.sin(rad)
        
    x2 = x
    x = x2 * cosZ - y * sinZ
    y = x2 * sinZ + y * cosZ

    # 3D to 2D projection
    factor = 4 * gstt.cc[22] / ((gstt.cc[21] * 8) + z)
    x = x * factor + xy_center [0] 
    y = - y * factor + xy_center [1] 
    
    return x,y


def joypads():

    if gstt.Nbpads > 0:
        
        # Champi gauche
        # Move center on X axis according to pad
        if gstt.pad1.get_axis(2)<-0.1 or gstt.pad1.get_axis(2)>0.1:
            gstt.cc[1] += gstt.pad1.get_axis(2) * 2

        # Move center on Y axis according to pad
        if gstt.pad1.get_axis(3)<-0.1 or gstt.pad1.get_axis(3)>0.1:
            gstt.cc[2] += gstt.pad1.get_axis(3) * 2

        # Champi droite
        '''
        # Change FOV according to joypad
        if gstt.pad1.get_axis(0)<-0.1 or gstt.pad1.get_axis(0)>0.1:
            gstt.cc[21] += -gstt.pad1.get_axis(0) * 2

        # Change dist according to pad
        if gstt.pad1.get_axis(1)<-0.1 or gstt.pad1.get_axis(1)>0.1:
            gstt.cc[22] += gstt.pad1.get_axis(1) * 2
        ''' 
        # "1" pygame 0
        # "2" pygame 1
        # "3" pygame 2
        # "4" pygame 3
        # "L1" pygame 4
        # "L2" pygame 6
        # "R1" pygame 5
        # "R2" pygame 7
            
        # Hat gauche gstt.pad1.get_hat(0)[0] = -1
        # Hat droit  gstt.pad1.get_hat(0)[0] = 1

        # Hat bas gstt.pad1.get_hat(0)[1] = -1
        # Hat haut  gstt.pad1.get_hat(0)[1] = 1
        
                
        #Bouton "3" 1 : surprise ON
        
        if gstt.pad1.get_button(2) == 1 and gstt.surprise == 0:
            gstt.surprise = 1
            gstt.cc[21] = 21    #FOV
            gstt.cc[22] = gstt.surpriseon   #Distance
            gstt.cc[2] +=  gstt.surprisey
            gstt.cc[1] +=  gstt.surprisex
            print "Surprise ON"
        
        #Bouton "3" 0 : surprise OFF
        
        if gstt.pad1.get_button(2) == 0:
            gstt.surprise = 0
            gstt.cc[21] = 21    #FOV
            gstt.cc[22] = gstt.surpriseoff  #Distance
            
        #Bouton "4". cycle couleur
        
        #if gstt.pad1.get_button(3) == 1:
        #   print "3", str(gstt.pad1.get_button(3))
        '''
        if gstt.pad1.get_button(3) == 1:
            newcolor = random.randint(0,2)
            print newcolor
            
            if gstt.color[newcolor] == 0:
                gstt.color[newcolor] = 1
                
            else:
                gstt.color[newcolor] = 0
                
            print "Newcolor  : ",str(gstt.newcolor), " ", str(gstt.color[newcolor])
        
        '''
                
        '''
        #Bouton "3" : diminue Vitesse des planetes
        if gstt.pad1.get_button(2) == 1:
            print "2", str(gstt.pad1.get_button(2))
        if gstt.pad1.get_button(2) == 1 and gstt.cc[5] > 2:
            gstt.cc[5] -=1
            print "X Curve : ",str(gstt.cc[5])
            
            
        #Bouton "1" : augmente Vitesse des planetes
        if gstt.pad1.get_button(0) == 1:
            print "0", str(gstt.pad1.get_button(0))
        if gstt.pad1.get_button(0) == 1 and gstt.cc[5] < 125:
            gstt.cc[5] +=1
            print "X Curve : ",str(gstt.cc[5])
            
            
        #Bouton "4". diminue Nombre de planetes
        if gstt.pad1.get_button(3) == 1:
            print "3", str(gstt.pad1.get_button(3))
        if gstt.pad1.get_button(3) == 1 and gstt.cc[6] > 2:
            gstt.cc[6] -=1
            print "Y Curve : ",str(gstt.cc[6])
        
        
        
        #Bouton "2" augmente Nombre de planetes
        if gstt.pad1.get_button(1) == 1:
            print "1", str(gstt.pad1.get_button(1))
        if gstt.pad1.get_button(1) == 1 and gstt.cc[6] < 125:
            gstt.cc[6] +=1
            print "Y Curve : ",str(gstt.cc[6])
        
        '''


        # Hat bas : diminue Vitesse des planetes
        #if gstt.pad1.get_hat(0)[1] == -1:
            #print "2", str(gstt.pad1.get_hat(0)[1])
        if gstt.pad1.get_hat(0)[1] == -1 and gstt.cc[5] > 2:
            gstt.cc[5] -=1
            print "X Curve/vitesse planete : ",str(gstt.cc[5])
            
            
        #Hat haut : augmente Vitesse des planetes
        #if gstt.pad1.get_hat(0)[1] == 1:
            #print "0", str(gstt.pad1.get_hat(0)[1])
        if gstt.pad1.get_hat(0)[1] == 1 and gstt.cc[5] < 125:
            gstt.cc[5] +=1
            print "X Curve/Vitesse planete : ",str(gstt.cc[5])
            
            
        # hat Gauche. diminue Nombre de planetes
        #if gstt.pad1.get_hat(0)[0] == -1:
            #print "3", str(gstt.pad1.get_hat(0)[0])
        if gstt.pad1.get_hat(0)[0] == -1 and gstt.cc[6] > 2:
            gstt.cc[6] -=1
            print "Y Curve/ nombre planete : ",str(gstt.cc[6])
        
        
        
        # hat droit augmente Nombre de planetes
        #if gstt.pad1.get_hat(0)[0] == 1:
            #print "1", str(gstt.pad1.get_hat(0)[0])
        if gstt.pad1.get_hat(0)[0] == 1 and gstt.cc[6] < 125:
            gstt.cc[6] +=1
            print "Y Curve/nb de planetes : ",str(gstt.cc[6])
        
        #print "hat : ", str(gstt.pad1.get_hat(0)[1])

        


