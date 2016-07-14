#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Dirk Toewe
#
# This file is part of Game of Pyth.
#
# Game of Pyth is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Game of Pyth is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Game of Pyth. If not, see <http://www.gnu.org/licenses/>.
'''
Created on Jul 3, 2016

@author: Dirk Toewe
'''
from PyQt4.QtGui import QApplication
import sys

from org.jengineering import GameOfPyth


if __name__ == '__main__':
  app = QApplication(sys.argv)
  golWidget = GameOfPyth.Widget(
#     GameOfPyth.DenseBoard( 256, 512, set( ( int(randint(0,256)), int(randint(0,512)) ) for _ in range(256*256/8) ) )
#     GameOfPyth.SparseBoard( ( int(randint(0,256)), int(randint(0,512)) ) for _ in range(256*256/8) )
#     GameOfPyth.SparseBoard(
#       GameOfPyth.DenseBoard([
#         [0,0,1,1,1,0,0,0,1,1,1,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [1,0,0,0,0,1,0,1,0,0,0,0,1],
#         [1,0,0,0,0,1,0,1,0,0,0,0,1],
#         [1,0,0,0,0,1,0,1,0,0,0,0,1],
#         [0,0,1,1,1,0,0,0,1,1,1,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,1,1,1,0,0,0,1,1,1,0,0],
#         [1,0,0,0,0,1,0,1,0,0,0,0,1],
#         [1,0,0,0,0,1,0,1,0,0,0,0,1],
#         [1,0,0,0,0,1,0,1,0,0,0,0,1],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,1,1,1,0,0,0,1,1,1,0,0]
#       ])
#     )
#       GameOfPyth.SparseBoard(
#         set(GameOfPyth.DenseBoard([
#           [1,1,1,1,1,1,1,1],
#           [1,0,1,1,1,1,0,1],
#           [1,1,1,1,1,1,1,1]
#         ]))
#       )
#       GameOfPyth.DenseBoard(56,56,lambda r,c: random() < 0.1),
#       GameOfPyth.DenseBoard(
#         [[0]*18]*4 +
#         [[0]*5+[1,1,1,1,1,1,1,1]+[0]*5,
#          [0]*5+[1,0,1,1,1,1,0,1]+[0]*5,
#          [0]*5+[1,1,1,1,1,1,1,1]+[0]*5] +
#         [[0]*18]*4
#       )
#     GameOfPyth.SparseBoard(
#       set(GameOfPyth.DenseBoard([
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
#         [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
#         [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#       ]))
#     )
#     GameOfPyth.SparseBoard(
#       set(GameOfPyth.DenseBoard([
#         [1,1,1,0,1],
#         [1,0,0,0,0],
#         [0,0,0,1,1],
#         [0,1,1,0,1],
#         [1,0,1,0,1]
#       ]))
#     )
#     GameOfPyth.SparseBoard(
#       set(GameOfPyth.DenseBoard([
#         [0,0,0,0,0,0,1,0],
#         [0,0,0,0,1,0,1,1],
#         [0,0,0,0,1,0,1,0],
#         [0,0,0,0,1,0,0,0],
#         [0,0,1,0,0,0,0,0],
#         [1,0,1,0,0,0,0,0]
#       ]))
#     )
#     GameOfPyth.SparseBoard(
#       set(GameOfPyth.DenseBoard([
#         [1]*8+[0]+[1]*5+[0]*3+[1]*3+[0]*6+[1]*7+[0]+[1]*5
#       ]))
#     )
#     GameOfPyth.DenseBoard(256,256,
#       set( GameOfPyth.SparseBoard_load('data/spacefiller.rle') ),
#       rowOff =13-128, colOff=24-128
#     )
#     GameOfPyth.SparseBoard_load('data/switchengine.rle')
    GameOfPyth.SparseBoard_load('data/spacefiller.rle')
#     GameOfPyth.SparseBoard_load('data/rileysbreeder.rle')
#     GameOfPyth.SparseBoard_load('data/breeder1.cells')
  )
  golWidget.setGeometry(200,200,800,600)
  golWidget.show()
  sys.exit( app.exec_() )