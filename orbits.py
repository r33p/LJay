"""

Orbits generators

by Sam Neurohack 
from /team/laser

Kept here as example : how to adapt previous code
In your main use :

import orbits

def Orbits(fwork):

    orbits.Draw(fwork)

"""

from globalVars import *
import frame,gstt
import sys, math, random
import set1
import colorify



class Orbits(object):
	
	def __init__(self):

		self.width = screen_size[0]
		self.height = screen_size[1]
		
		# elliptical orbit equation : r = (SemiMajorAxis*(1 - eccentricity**2))/(1 + eccentricity * cos(angle))
		# for each planet : (Angle,SemiMajorAxis length, eccentricity)
		
		self.planets = [[0,100,0.4],[90,55,0.2],[230,46,0.5],[30,90,0.5],[190,60,0.4],[90,80,0.2],[60,55,0.3],[120,67,0.2],[90,30,0.1],[15,34,0.45]]
		self.planet = [0,0,0]
		
		self.centerX = 50 + self.width / 2
		self.centerY = self.height / 2

		
		self.fov = 256
		self.viewer_distance = 100.2
		
		self.angleX = 0
		self.angleY = 0
		self.angleZ = 0
		self.color = 0xFF0000
		self.speed = 0

	# Remap values in different scales i.e CC value in screen position.
	def cc2scrX(self,s):
		a1, a2 = 0,127  
		b1, b2 = -screen_size[0]/2, screen_size[0]/2
		return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

	def cc2scrY(self,s):
		a1, a2 = 0,127  
		b1, b2 = -screen_size[1]/2, screen_size[1]/2
		return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

	def cc2range(self,s,min,max):
		a1, a2 = 0,127  
		b1, b2 = min, max
		return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

	def extracc2scrX(self,s):
		a1, a2 = -66000,66000  
		b1, b2 = 0, screen_size[0]
		return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

	def extracc2scrY(self,s):
		a1, a2 = -66000,66000 
		b1, b2 = 0, screen_size[1]
		return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

	def extracc2range(self,s,min,max):
		a1, a2 = -66000,66000  
		b1, b2 = min, max
		return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


	def Move(self,centerX,centerY):
		self.centerX = centerX
		self.centerY = centerY	

	def joypads(self):

		if gstt.Nbpads > 0:
       
			# Champi gauche
			# Move center on X axis according to pad
			if gstt.pad1.get_axis(2)<-0.1 or gstt.pad1.get_axis(2)>0.1:
				gstt.cc[1] += gstt.pad1.get_axis(2) * 2

			# Move center on Y axis according to pad
			if gstt.pad1.get_axis(3)<-0.1 or gstt.pad1.get_axis(3)>0.1:
				gstt.cc[2] += gstt.pad1.get_axis(3) * 2
        
			if gstt.pad1.get_button(2) == 1 and gstt.surprise == 0:
				gstt.surprise = 1
				gstt.cc[21] = 21    #FOV
 				gstt.cc[22] = gstt.surpriseon   #Distance
				gstt.cc[2] +=  gstt.surprisey
				gstt.cc[1] +=  gstt.surprisex
				print "Surprise ON"
        
			if gstt.pad1.get_button(2) == 0:
				gstt.surprise = 0
				gstt.cc[21] = 21    #FOV
				gstt.cc[22] = gstt.surpriseoff  #Distance
            
			if gstt.pad1.get_hat(0)[1] == -1 and gstt.cc[5] > 2:
				gstt.cc[5] -=1
				print "X Curve/vitesse planete : ",str(gstt.cc[5])

			if gstt.pad1.get_hat(0)[1] == 1 and gstt.cc[5] < 125:
				gstt.cc[5] +=1
				print "X Curve/Vitesse planete : ",str(gstt.cc[5])

			if gstt.pad1.get_hat(0)[0] == -1 and gstt.cc[6] > 2:
				gstt.cc[6] -=1
				print "Y Curve/ nombre planete : ",str(gstt.cc[6])
        
			# hat droit augmente Nombre de planetes
			if gstt.pad1.get_hat(0)[0] == 1 and gstt.cc[6] < 125:
				gstt.cc[6] +=1
			print "Y Curve/nb de planetes : ",str(gstt.cc[6])

	
	def Draw(self,f):
		
		#f.LineTo((self.centerX,self.centerY), 0x000000)
		'''
		self.angleX += 0.0
		self.angleY += 0.0
		self.angleZ += 0.0
		'''
		PL = 0
		self.joypads()
		
		gstt.angleX += self.cc2range(gstt.cc[29],0,0.1)
		gstt.angleY += self.cc2range(gstt.cc[30],0,0.1)
		gstt.angleZ += self.cc2range(gstt.cc[31],0,0.1)


		for number in range(int(self.cc2range(gstt.cc[6],1,10))):

			planet = self.planets[number]
			planet[0] += self.cc2range(gstt.cc[5],0,25)
			
			rad = planet[0] * PI / 180
			r = (planet[1]*(1 - planet[2]**2))/(1 + (planet[2] * math.cos(rad))) #* gstt.
			
			
			x = r * math.cos(rad)
			y = r * math.sin(rad)
			z = 0
			# print x,y,z
			
			
			# 3D rotation along self.angleX, self.angleX, self.angleX
			
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
			
			#print x,y

			# 3D to 2D projection
			factor = 4 * gstt.cc[22] / ((gstt.cc[21] * 8) + z)
			x = x * factor + self.centerX + gstt.cc[1] -100
			y = - y * factor + self.centerY - gstt.cc[2]
			
			'''
			angle = 90
			angle = angle * PI / 180
			x2 = x* math.cos(angle) - y*math.sin(angle)  
			y2 = x* math.sin(angle) + y*math.cos(angle) 
			x2 = x2 * factor + self.centerX
			y2 = - y2 * factor + self.centerY

			angle = 270
			angle = angle * PI / 180
			x3 = x* math.cos(angle) - y*math.sin(angle)
			y3 = x* math.sin(angle) + y*math.cos(angle)
			x3 = x2 * factor + self.centerX
			y3 = - y3 * factor + self.centerY
			'''


			#print x,y
			
				
			f.Line((x,y),(x+5,y+5),  c=colorify.rgb2hex(gstt.color), PL = PL)

			#f.Line((x2,y2),(x2+5,y2+5),  c=colorify.rgb2hex(gstt.color))

			#f.Line((x3,y3),(x3+5,y3+5),  c=colorify.rgb2hex(gstt.color))

		gstt.PL[PL] = f.LinesPL(PL)

