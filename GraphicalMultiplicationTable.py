#!/usr/bin/env python3
#coding: utf-8

'''
Created on 27 juin 2017

Copyright 2017 Jean-Marie Mineau

    "Graphic Multiplication Tables" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    "Graphic Multiplication Tables" is distributed in the hope that it will be useful and 
    recreative, but WITHOUT ANY WARRANTY; without even the implied 
    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with "Graphic Multiplication Tables".  If not, see <http://www.gnu.org/licenses/>.

@author: <mineau.jean.marie@gmail.com

This is a programm which displays the multiplication tables in a graphic view.
Use pygame.
'''
import pygame
from math import cos, acos, asin, sin, pi, sqrt


class CartesianPoint:
    """A point, with cartesian coordinates."""
    
    def __init__(self, x, y):
        """Initialize x and y."""
        self.setPos((x, y))
        
    def getPos(self):
        """The pos getteur. Return the round values."""
        return (round(self.x), round(self.y))
    
    def setPos(self, pos):
        """The pos setteur."""
        self.x = pos[0]
        self.y = pos[1]
        
    pos = property(getPos, setPos)
    
    def convertPolar(self):
        """Return the point converted into polar coordinates."""
        ray = sqrt(self.x**2 + self.y**2)
        azimuth = acos(self.x/ray)
        if self.y > 0: #The mark is pointing downwards, it's not y < 0.
            azimuth *= -1;
        return PolarPoint(azimuth, ray)
    
    def changeMark(self, pos):
        """Change the point mark to the mark center with the pos."""
        x, y = pos
        self.x += x
        self.y += y
        return self
    

class PolarPoint:
    """A point, with polar coordinates."""
    
    def __init__(self, azimuth, ray):
        """Initialize the values of the  azimuth and the ray."""
        self.azimuth = azimuth
        self.ray = ray
    
    def getPos(self):
        """The pos getteur."""
        return (self.azimuth, self.ray)
    
    def setPos(self, pos):
        """The pos setteur."""
        self.azimuth = pos[0]
        self.ray[1]
        
    pos = property(getPos, setPos)
    
    def convertCartesian(self):
        """Return the point converted into cartesian coordinates."""
        x = self.ray * cos(self.azimuth)
        y = -self.ray * sin(self.azimuth) # - because the mark is pointing downwards 
        return CartesianPoint(x, y)


class Graphic:
    """The graphic, with pygame surface and points."""
    
    def __init__(self, pointsNumber, table):
        """The points number is the number of points in the graph,
        table is the table used, like 2, or 9."""
        
        self.modulo = pointsNumber
        #The table is displayed modulo the number of point.
        self.table = table
        
        self._size = (700, 700)
        self.screen =  pygame.display.set_mode(self._size)
        self.backgroundColor = (255, 255, 255)
        self.pointColor = (255, 255, 255)
        self.linesColor = (0, 0, 0)
        self.lineWidth = 1
        self.pointRadius = 1
        
        self.setPoints()
        
    def setSize(self, size):
        """Size setteur."""
        self._size = size
        self.screen = pygame.display.set_mode(self._size)
        self.setPoints()
        
    def getSize(self):
        """Size getteur."""
        return self._size
    
    size = property(getSize, setSize)
    
    def setPoints(self, pointsNumber=None, table=None):
        """Create the points size, with the possibility of changing 
        the point number and the table."""
        if pointsNumber is not None:
            self.modulo = pointsNumber
        
        #Place the points in a circle to equal distance
        polarPoints = []
        ray = min(self.size) // 2 - 20
        for i in range(self.modulo):
            azimuth = 2 * i * pi / self.modulo + pi / 2
            point = PolarPoint(azimuth, ray)
            polarPoints.append(point)
            
        center = self.size[0] // 2, self.size[1] // 2
        self.points = []
        for point in polarPoints:
            self.points.append(point.convertCartesian().changeMark(center))
            #convert polar coordinates to cartesian, and change the mark to the center.
        
        self.draw(table)
    
    def setTable(self, table):
        """Set the table."""
        self.draw(table)
        
    def draw(self, table = None):
        """Draw the multiplication table."""
        if table is not None:
            self.table = table
            
        self.screen.fill(self.backgroundColor)
        #Draw the points
        for p in self.points:
            pygame.draw.circle(self.screen, self.pointColor, p.pos, self.pointRadius)
        #Draw the lines.
        for i in range(len(self.points)):
            indexPoint2 = round(i * self.table) % self.modulo
            self.drawLine(i, indexPoint2)
            
        pygame.display.flip()

    def drawLine(self, indexPoint1, indexPoint2):
        """Draw a line between the two points."""
        pos1 = self.points[indexPoint1].pos
        pos2 = self.points[indexPoint2].pos
        pygame.draw.line(self.screen, self.linesColor, pos1, pos2, self.lineWidth)

    def tableEvolutionAnim(self, time=50):
        """Launch an animation. The graphic will be displayed with 
        the evolution of the table."""
        forever = True
        i = 2.0
        coeff = 0.01
        while forever:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.setTable(table = i)
            i += coeff
            if i >= 500:
                coeff = -0.01
            elif i <= 2:
                coeff = 0.01
            pygame.time.wait(time)
            
    def numberPointEvolutionAnim(self, time=100):
        """Launch an animation. The graphic will be displayed with 
        the evolution of the umber of point."""
        forever = True
        i = 2
        coeff = 1
        while forever:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.setPoints(pointsNumber = i)
            i += coeff
            if i >= 500:
                coeff = -1
            elif i <= 2:
                coeff = 1
            pygame.time.wait(time)
        

if __name__ == "__main__":

    pygame.init()

    #graphic = Graphic(885, 2)
    #graphic.tableEvolutionAnim()
    graphic = Graphic(2, 481)
    graphic.numberPointEvolutionAnim(time=500)
