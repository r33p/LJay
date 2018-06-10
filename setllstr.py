#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

import math
import gstt
from globalVars import *
import bhorosc
import colorify
import orbits
import numpy as np
import collections
import time


dotsosc = collections.deque(maxlen=10)
dotsosc0 = collections.deque(maxlen=10)
dotsosc1 = collections.deque(maxlen=10)
dotsoscT = [dotsosc0,dotsosc1]
currentdotsosc=0

f_sine = 0

screenSizeX=screen_size[0]
screenSizeY=screen_size[1]

# Curve 0
def NozMode(fwork):
    global f_sine,x
    global dotsosc
    global dotsosc0
    global dotsosc1
    global dotsoscT
    global currentdotsosc
    #global dots
    #dots = []
        
    amp = 200
    nb_point = 40
    nbplow=10
    nbphigh=100
    '''
    for t in range(0, nb_point+1):
    
        #y = cc2scrX((66000 + gstt.osc[4])%127)
        #x = cc2scrX((66000 + gstt.osc[5])%127)
        #rint x,y
        x = 3.5 *(extracc2scrX(gstt.osc[gstt.X]) - 400)
        y = 3.5 *(extracc2scrY(gstt.osc[gstt.Y]) - 300)
        #print proj(int(x),int(y),0)
        dots.append(proj(int(x),int(y),0))
        
    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color)  )
    '''
    #x = cc2scrX((66000 + gstt.osc[4])%127)
    #x += 1
    #if x >= 840:
    #    x = -840

    #read lfo # or osc #
    #x = 1.8 *(extracc2scrX(gstt.osc[1]) - 300)

    #x = 1.8 *(extracc2scrX(gstt.osc[gstt.X]) - 400) 
    #print gstt.OscXY[0]
    #print gstt.OscXY[1]
    #print gstt.OscXY[2]

    if gstt.X != 0:
    #print "gstt.X != 0 (== %d)" % gstt.X
        if (dotsosc.maxlen == nbphigh and gstt.Y != 0):
            print "X changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbplow)
            dotsoscT[0] = collections.deque(maxlen=nbplow)
            dotsoscT[1] = collections.deque(maxlen=nbplow)
            dotsosc = collections.deque(maxlen=nbplow)
        xT = gstt.osc[gstt.X]
        x = 3.5 * (extracc2scrX(xT) - screenSizeX/2)
    else:
    #print "gstt.X == 0"
        if (gstt.Y != 0 and dotsosc.maxlen == nbplow):
            print "X changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbphigh)
            dotsoscT[0] = collections.deque(maxlen=nbphigh)
            dotsoscT[1] = collections.deque(maxlen=nbphigh)
            dotsosc = collections.deque(maxlen=nbphigh)
        xT = (((time.time()*50000) % 65536) - 32768)
        x = 3.5 * (extracc2scrX(xT) - screenSizeX/2)
    #print "x:%r,xT:%r" % (x,xT)

    #x = 3.5 * (extracc2scrX(xT) - 400)
    #x = 3.5 *(extracc2scrX(gstt.osc[gstt.X]) - 400)
    #y = cc2scrX((32000 + gstt.osc[4])%127)
    #y = 3 *(extracc2scrY(gstt.osc[2]) - 300)

    if gstt.Y != 0:
    #print "gstt.Y != 0 (== %d)" % gstt.Y
        if (dotsosc.maxlen == nbphigh and gstt.X != 0):
            print "Y changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbplow)
            dotsoscT[0] = collections.deque(maxlen=nbplow)
            dotsoscT[1] = collections.deque(maxlen=nbplow)
            dotsosc = collections.deque(maxlen=nbplow)
        yT = gstt.osc[gstt.Y]
        y = 3.5 * (extracc2scrY(yT) - screenSizeY/2)
    else:
    #print "gstt.Y == 0"
        if (gstt.X != 0 and dotsosc.maxlen == nbplow):
            print "Y changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbphigh)
            dotsoscT[0] = collections.deque(maxlen=nbphigh)
            dotsoscT[1] = collections.deque(maxlen=nbphigh)
            dotsosc = collections.deque(maxlen=nbphigh)
        yT = (((time.time()*50000) % 65536) - 32768)
        y = 3.5 * (extracc2scrY(yT) - screenSizeY/2)
    #print "y:%r,yT:%r" % (y,yT)

    if gstt.X == 0 and gstt.Y == 0:
        x = 0
        y = 0

    #y = 3.5 * (extracc2scrY(yT) - 300)
    #y = 3.5 *(extracc2scrY(gstt.osc[gstt.Y]) - 300)
    #print x,y
    #gstt.cc[22]=extracc2range(gstt.osc[6],0,127)
    newx,newy =  proj(int(x),int(y),0)
    #print "NX: %r, NY: %r" % (newx,newy)
    #dots.append(proj(int(x),int(y),0))    
    #if len(dots) >= 5:
    #   dots = []
    #newxR=newx+random.randint(-200,200)
    #newyR=newy+random.randint(-100,100)
    #dots.append((newx+random.randint(-200,200),newy+random.randint(-100,100)))
    #dotsosc.append((newx+random.randint(-200,200),newy+random.randint(-100,100)))
    #dots.append((newxR,newyR))
    #dotsosc.append((newxR,newyR))

    #print dotsosc
    #print len(dotsosc)

    if gstt.X != 0 and gstt.Y == 0:
        if 1 < len(dotsoscT[currentdotsosc]) and newy > dotsoscT[currentdotsosc][-1][1]:
            dotsoscT[currentdotsosc]=collections.deque(maxlen=nbphigh)
            currentdotsosc=(currentdotsosc+1)%2
            #print "Switching dotosc to #%d"%currentdotsosc
            dotsoscT[currentdotsosc]=collections.deque(maxlen=nbphigh)
        dotsoscT[currentdotsosc].append((newx,newy))

    if gstt.X == 0 and gstt.Y != 0:
        if 1 < len(dotsoscT[currentdotsosc]) and newx < dotsoscT[currentdotsosc][-1][0]:
            dotsoscT[currentdotsosc]=collections.deque(maxlen=nbphigh)
            currentdotsosc=(currentdotsosc+1)%2
            #print "Switching dotosc to #%d"%currentdotsosc
            dotsoscT[currentdotsosc]=collections.deque(maxlen=nbphigh)

        dotsoscT[currentdotsosc].append((newx,newy))

    if (gstt.X == 0 and gstt.Y == 0) or (gstt.X != 0 and gstt.Y != 0):
        #dotsosc.append((newx,newy))
        dotsoscT[0].append((newx,newy))
        dotsoscT[1].append((newx,newy))

#       fwork.PolyLineOneColor( dotsosc, c=colorify.rgb2hex(gstt.color)  )
#    if currentdotosc == 0:
#   if newx >= dotosc0

#    dotsosc0.append((newx,newy))
#    dotsosc1.append((newx,newy))

    #print dots

    #print dotsosc

    #print "LastP X",type(dotsosc[-1][0])
    #print "LastP X",type(dotsosc[-1][0])
    #print "LastP Y",dotsosc[-1][1]
    
    #fwork.Line((newx,newy),(newx+ 5,newy+5), colorify.rgb2hex(gstt.color) )



    #fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color)  )

    #fwork.PolyLineOneColor( dotsosc, c=colorify.rgb2hex(gstt.color)  )
    fwork.PolyLineOneColor( dotsoscT[0], c=colorify.rgb2hex(gstt.color)  )
    fwork.PolyLineOneColor( dotsoscT[1], c=colorify.rgb2hex(gstt.color)  )

    #print "dotsoscT[0]",dotsoscT[0]
    #print "dotsoscT[1]",dotsoscT[1]

#    fwork.PolyLineOneColor( dotsosc0, c=colorify.rgb2hex(gstt.color)  )
#    fwork.PolyLineOneColor( dotsosc1, c=colorify.rgb2hex(gstt.color)  )

    #fwork.PolyLineOneColor( reversed(dotsosc), c=colorify.rgb2hex(gstt.color)  )
    #fwork.Line((newx,newy),(newx+ 1,newy+1), colorify.rgb2hex(gstt.color) )
#    fwork.Line((newx,10),(newx+ 1,10+1), colorify.rgb2hex(gstt.color) )
#    fwork.Line((10,newy),(10,newy+1), colorify.rgb2hex(gstt.color) )
    #time.sleep(0.0005)

# Curve 1
def NozMode2(fwork):
    import mikuscope as mk
    dots = []
    nb_point=100
    #print mk.x
    #print mk.y
    #print "Hey! Hey!"
    #print "x:",type(x),x.shape,x.dtype
    #print "y:",type(y),y.shape,y.dtype

    for idx, valx in enumerate(mk.x):
            if not np.isnan(valx):
                    #print idx,valx,mk.y[idx]
                xT = valx*20000
                x = 3.5 * (extracc2scrX(xT) - 400)
                yT = mk.y[idx]*15000
                y = 3.5 * (extracc2scrY(yT) - 300)
                dots.append(proj(int(x),int(y),0))
            else:
            #dots.append(proj(0,0,0))
                fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
            #dots=[]
        #if not idx%nb_point:
            #   fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
    #raw_input("Hit Enter to continue")

# Curve 2
def Sine(fwork):
    global f_sine

    dots = []
        
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2 * PI * (float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2 * PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color)  )
    
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01

# Curve 3
def Orbits(fwork):

    orbits.Draw(fwork)

# Curve 4
def Circle(fwork):
    global f_sine

    dots = []
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2* PI * f_sine *(float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2* PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
    
    #print f_sine
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01
		

# Curve 5
def CC(fwork):

    dots = []
        
    amp = 200
    nb_point = 60
    for t in range(0, nb_point+1):
        y = 1 - amp*math.sin(2*PI*cc2range(gstt.cc[5],0,24)*(float(t)/float(nb_point)))
        x = 1 - amp*math.cos(2*PI*cc2range(gstt.cc[6],0,24)*(float(t)/float(nb_point))) 
        #bhorosc.send5("/point", [proj(int(x),int(y),0),colorify.rgb2hex(gstt.color)])       
        dots.append(proj(int(x),int(y),0))
        
    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )



# Curve 6
def Slave(fwork):
    
    fwork.LineTo([gstt.point[0],gstt.point[1]],gstt.point[2])

# Curve 7

def Osci(fwork):
    Pass

def ssawtooth(samples,freq,phase):

	t = np.linspace(0+phase, 1+phase, samples)
	for ww in range(samples):
		samparray[ww] = signal.sawtooth(2 * np.pi * freq * t[ww])
	return samparray

def ssquare(samples,freq,phase):

	t = np.linspace(0+phase, 1+phase, samples)
	for ww in range(samples):
		samparray[ww] = signal.square(2 * np.pi * freq * t[ww])
	return samparray

def ssine(samples,freq,phase):

	t = np.linspace(0+phase, 1+phase, samples)
	for ww in range(samples):
		samparray[ww] = np.sin(2 * np.pi * freq  * t[ww])
	return samparray


	
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



def proj(x,y,z):

    gstt.angleX += cc2range(gstt.cc[29],0,0.1)
    gstt.angleY += cc2range(gstt.cc[30],0,0.1)
    gstt.angleZ += cc2range(gstt.cc[31],0,0.1)
    
    rad = gstt.angleX * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    y2 = y
    y = y2 * cosa - z * sina
    z = y2 * sina + z * cosa

    rad = gstt.angleY * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    z2 = z
    z = z2 * cosa - x * sina
    x = z2 * sina + x * cosa

    rad = gstt.angleZ * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x2 = x
    x = x2 * cosa - y * sina
    y = x2 * sina + y * cosa

    # 3D to 2D projection
    factor = 4 * gstt.cc[22] / ((gstt.cc[21] * 8) + z)
    x = x * factor + xy_center [0]
    y = - y * factor + xy_center [1]

    return x,y

