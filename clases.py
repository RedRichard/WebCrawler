# -*- coding: utf-8 -*-
"""
Created on Sat May 28 14:15:16 2016

@author: gomri
"""

class url:
    global numRepeticiones
    def __init__(self, link):
      self.dir = link
      #self.id = ""
      self.repeticiones = 0
      self.profundidad = 0
      self.existe = True
