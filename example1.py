#!/usr/bin/env python3
#coding: utf-8

'''
Created on 27 juin 2017

@author: <mineau.jean.marie@gmail.com>

First example of use.
'''
import pygame
from GraphicalMultiplicationTable import Graphic


if __name__ == "__main__":
    
    pygame.init()
    
    graphic = Graphic(2, 481)
    graphic.numberPointEvolutionAnim(time=500)
