# coding=UTF-8

'''
LJay v0.8.0


LICENCE : CC
pclf, Sam Neurohack

'''

import pygame
import gstt
import math
import redis

if gstt.debug >0: 
	print "Point list server :",gstt.LjayServerIP
r = redis.StrictRedis(host=gstt.LjayServerIP, port=6379, db=0)

class Frame(object):
	'''
	classdocs
	'''


	def __init__(self):
		'''
		Constructor
		'''
		
		# legacy point list
		self.point_list = []
		
		# 4 point list
		self.pl = [[],[],[],[]]
		self.grid_points = [(300.0, 200.0, 0), (500.0, 200.0, 65280), (500.0, 400.0, 65280), (300.0, 400.0, 65280), (300.0, 200.0, 65280),(200.0, 100.0, 0), (600.0, 100.0, 65280), (600.0, 500.0, 65280), (200.0, 500.0, 65280), (200.0, 100.0, 65280)]

	def LineTo(self, xy, c, PL):
	
		self.point_list.append((xy + (c,)))				#add c to the tuple 
		self.pl[PL].append((xy + (c,)))
	
	
	def Line(self, xy1, xy2, c, PL):
		self.LineTo(xy1, 0, PL)
		self.LineTo(xy2, c , PL)
	

	def PolyLineOneColor(self, xy_list, c, PL , closed ):
		#print "--"
		#print "c",c
		#print "xy_list",xy_list
		#print "--"
		xy0 = None		
		for xy in xy_list:
			if xy0 is None:
				xy0 = xy
				#print "xy0:",xy0
				self.LineTo(xy0,0, PL)
			else:
				#print "xy:",xy
				self.LineTo(xy,c, PL)
		if closed:
			self.LineTo(xy0,c, PL)


	# Computing points coordinates for rPolyline function from 3D and around 0,0 to pygame coordinates
	def Pointransf( self, xy, xpos = 0, ypos =0, resize =1, rotx =0, roty =0 , rotz=0):

			x = xy[0] * resize
			y = xy[1] * resize
			z = 0

			rad = rotx * math.pi / 180
			cosaX = math.cos(rad)
			sinaX = math.sin(rad)

			y2 = y
			y = y2 * cosaX - z * sinaX
			z = y2 * sinaX + z * cosaX

			rad = roty * math.pi / 180
			cosaY = math.cos(rad)
			sinaY = math.sin(rad)

			z2 = z
			z = z2 * cosaY - x * sinaY
			x = z2 * sinaY + x * cosaY

			rad = rotz * math.pi / 180
			cosZ = math.cos(rad)
			sinZ = math.sin(rad)

			x2 = x
			x = x2 * cosZ - y * sinZ
			y = x2 * sinZ + y * cosZ

			#print xy, (x + xpos,y+ ypos)
			return (x + xpos,y+ ypos)
			'''
			to understand why it get negative Y
			
			# 3D to 2D projection
			factor = 4 * gstt.cc[22] / ((gstt.cc[21] * 8) + z)
			print xy, (x * factor + xpos,  - y * factor + ypos )
			return (x * factor + xpos,  - y * factor + ypos )
			'''
	
	# Send 2D point list around 0,0 with 3D rotation resizing and reposition around xpos ypos
	#def rPolyLineOneColor(self, xy_list, c, PL , closed, xpos = 0, ypos =0, resize =1, rotx =0, roty =0 , rotz=0):
	def rPolyLineOneColor(self, xy_list, c, PL , closed, xpos = 0, ypos =0, resize =0.7, rotx =0, roty =0 , rotz=0):
		xy0 = None		
		for xy in xy_list:
			if xy0 is None:
				xy0 = xy
				self.LineTo(self.Pointransf(xy0, xpos, ypos, resize, rotx, roty, rotz),0, PL)
			else:
				self.LineTo(self.Pointransf(xy, xpos, ypos, resize, rotx, roty, rotz),c, PL)
		if closed:
			self.LineTo(self.Pointransf(xy0, xpos, ypos, resize, rotx, roty, rotz),c, PL)


	# set all points for given laser. special behavior depends on GridDisplay flag
	# 0: point list / 1: Grid 
	def LinesPL(self, PL):

		if gstt.GridDisplay[PL] == 0:
			if r.set('/pl/'+str(PL), str(self.pl[PL])) == True:
				#print 'franken /pl/'+str(PL), str(self.pl[PL])
				return self.pl[PL]

		if gstt.GridDisplay[PL] == 1:
			r.set('/pl/'+str(PL), str(self.grid_points))
			return self.grid_points

	def ResetPL(self, PL):
		self.pl[PL] = []

				
	def RenderScreen(self, surface):
		if len(self.pl[gstt.simuPL]):
			#print gstt.simuPL
			xyc_prev = self.pl[gstt.simuPL][0]
			#pygame.draw.line(surface,self.black_hole_color,(x_bh_cur, y_bh_cur), (x_bh_next, y_bh_next))
			#pygame.draw.line(surface,self.spoke_color,(x_bh_cur, y_bh_cur), (x_area_cur, y_area_cur))
			for xyc in self.pl[gstt.simuPL]:
				c = int(xyc[2])
				if c: pygame.draw.line(surface,c,xyc_prev[:2],xyc[:2],3)
				xyc_prev = xyc



class FrameHolder(object):
	def __init__(self):
		self.f = None
		
