#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

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
Created on Jul 4, 2016

@author: dtitx
'''
from PyQt4 import QtCore
from PyQt4.Qt import QGridLayout, QSlider, Qt
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QWidget, QPushButton, QPainter, QColor, QLabel
from _abcoll import Iterable
from copy import copy
import re
from collections import Counter


class Widget(QWidget):

  def __init__(self,board):
    super(Widget,self).__init__()
    if not isinstance(board,Board):
      raise Exception('Constructor argument of type Board expected.')
    canvas = _Canvas(board)
    self.setWindowTitle('Game of Pyth')
    
    def tick():
      board.increment()
      canvas.update()

    timer = QTimer()
    timer.timeout.connect(tick)

    speedLabel = QLabel('? ticks/sec')
    speedLabel.setToolTip('Simulation speed [ticks/sec.].')
    speedLabel.resize(speedLabel.sizeHint())

    startStop = QPushButton('Start/Stop')
    startStop.setToolTip('Start the simulation.')
    startStop.resize(startStop.sizeHint())
    
    speedSlider = QSlider(QtCore.Qt.Horizontal)
    speedSlider.resize(speedSlider.sizeHint())
    speedSlider.setMinimum(0)
    speedSlider.setMaximum(20)
    speedSlider.setTickPosition(QSlider.TicksBelow)

    def tpsChange(value): # <- called whenever ticks/sec. change
      value = 2.0**( value/2.0 - 2 )
      speedLabel.setText( '%(value)6.2f ticks/sec.' % locals() )
      timer.setInterval(1000/value)

    speedSlider.valueChanged[int].connect(tpsChange)
    speedSlider.setValue(8)

    def startStopClick():
      startStopClick.running ^= True 
      if startStopClick.running:
        timer.start()
        startStop.setText('Stop')
      else:
        timer.stop()
        startStop.setText('Start')
    startStopClick.running = True

    startStop.clicked.connect(startStopClick)
    startStopClick()

    grid = QGridLayout(self)
    grid.addWidget(startStop,0,0)
    grid.addWidget(speedSlider,0,1)
    grid.addWidget(speedLabel,0,2)
    grid.addWidget(canvas,1,0,1,3)

class _Canvas(QWidget):

  def __init__(self,board):
    super(_Canvas,self).__init__()
    self.__ppc = 8 # <- current zoom factor in pixels/cell
    self.__rowOff = 0
    self.__colOff = 0
    self.__board = board # <- current zoom factor in pixels/cell
    self.setMouseTracking(False)

  def mouseReleaseEvent(self,event):
    if hasattr(self,'_mousePos'):
      del(self._mousePos)

  def mouseMoveEvent(self,event):
    if event.buttons() == Qt.LeftButton:
      if hasattr(self,'_mousePos'):
        delta = event.pos() - self._mousePos
        self.__colOff += delta.x()
        self.__rowOff += delta.y()
        self.update()
      self._mousePos = event.pos()

  def paintEvent(self,event):
    ppc   = self.__ppc
    board = self.__board
    rOff  = self.__rowOff
    cOff  = self.__colOff
    c = QPainter()
    c.begin(self)
    c.setPen( QColor(0,0,0) )
    # DRAW BOUNDARY FOR DENSE BOARD
    if isinstance(board,DenseBoard):
      c.drawRect( cOff-2+board.colOff*ppc, rOff-2+board.rowOff*ppc, board.nCols*ppc+2, board.nRows*ppc+2 )
    for row,col in board:
      c.fillRect(
        ppc*col+cOff, ppc*row+rOff, max(1,ppc-1), max(1,ppc-1),
        QColor(0,0,0)
      )
    c.end()

  def wheelEvent(self,event):
    pos = event.pos()
    c,r = pos.x(), pos.y()
    r -= self.__rowOff
    c -= self.__colOff
    ppc = max(1,min(64,self.__ppc+event.delta()/120)) # <- new pixels/cell count
    # move rowOff and colOff so that you always zoom into the cursor position
    self.__rowOff += r - r * ppc/self.__ppc
    self.__colOff += c - c * ppc/self.__ppc
    self.__ppc = ppc
    self.update()

class Board(object):
  '''
  An abstract game of life board consisting of cells addressable by two dimensional integer indices.
  '''

  def _indexOnBoard(self,row,col):
    return row,col
  
  def _calculateNextChangesIntitially(self):
    '''
    Returns a set of the cells that are going to change during the first time step increment.
    '''
    counter = Counter(
      self._indexOnBoard(r,c)
      for row,col in self
      for r in range(row-1,row+2)
      for c in range(col-1,col+2)
    )
    def changes(cell,neighbors):
      alive = self[cell]
      aliveTomorrow = alive
      neighbors -= alive 
      if alive:
        if neighbors  < 2: aliveTomorrow = False
        if neighbors  > 3: aliveTomorrow = False
      elif neighbors == 3: aliveTomorrow = True
      return alive ^ aliveTomorrow
    return { x for x,n in counter.iteritems() if changes(x,n) }

  def _calculateNextChanges(self):
    '''
    Returns a set of the cells that are going to change during the next time step increment.
    '''
    def changes(row,col):
      alive = self[row,col]
      aliveTomorrow = alive
      neighbors = -alive + sum(
        self[r,c]
        for r in range(row-1,row+2)
        for c in range(col-1,col+2)
      )
      if alive:
        if neighbors  < 2: aliveTomorrow = False
        if neighbors  > 3: aliveTomorrow = False
      elif neighbors == 3: aliveTomorrow = True
      return alive ^ aliveTomorrow
    return {
      self._indexOnBoard(r,c)  
      for row,col in self._nextChanges
      for r in range(row-1,row+2)
      for c in range(col-1,col+2)
      if changes(r,c)
    }
    
#     self.__previousChanges = self.__changes # <- could be used to redraw more cleverly
#     # TODO: only consider cells that changes last turn and their neighbors (should improve performance on spacefillers)
#     counter = Counter(
#       self._indexOnBoard(r,c)
#       for row,col in self
#       for r in range(row-1,row+2)
#       for c in range(col-1,col+2)
#     )
#     for (row,col),neighbors in counter.iteritems():
#       alive = self[row,col]
#       neighbors -= alive 
#       if alive:
#         if neighbors  < 2: alive = False
#         if neighbors  > 3: alive = False
#       elif neighbors == 3: alive = True
#       self[row,col] = alive

class DenseBoard(Board): # namedtuple('Board','nRows, nCols, cells')

  def __init__(self,*args,**kwargs):#//,nRows,nCols,values=lambda r,c: False):
    '''
    Creates a new dense Game of Life board. The constructor expects either 1 (list[list[bool]]), 2 (int,int) or 3 (int,int,(int,int) -> bool) arguments.
    '''
    keywords = {'rowOff','colOff'}
    for key in kwargs:
      if not keywords:
        raise Exception( 'Illegal keyword argument: "%(key)s". Only %(keywords)s allowed.' % locals() )
    self.__rowOff = 0
    self.__colOff = 0
    if 'rowOff' in kwargs: self.__rowOff += kwargs['rowOff']
    if 'colOff' in kwargs: self.__colOff += kwargs['colOff']
    if 3 < len(args): raise Exception('Only 1,2 or 3 non-keyword arguments allowed, (), (iterable[iterable[int]]), (nRows: int,nCols: int), (nRows: int,nCols: int,vals: set[int,int]), (nRows: int,nCols: int,vals: map[(int,int)->bool]), (nRows: int,nCols: int,vals: (row: int,col: int) -> alive: bool)')
    if 1 == len(args):
      self.__cells = [ [col for col in row] for row in args[0] ]
      self.__nRows = len(self.__cells)
      self.__nCols = len(self.__cells[0])
      # validity checks
      for (iRow,row) in enumerate(self.__cells):
        # check for correct length of all rows
        if len(row) != self.__nCols:
          raise Exception( 'len(val[0]) != len(vals[%(iRow)d]).' % locals() )
    else:
      if 2 == len(args):
        args = args[0], args[1], lambda r,c: False
      self.__nRows, self.__nCols, vals = args
      if not isinstance(self.nRows,int): raise Exception('When using 2 or 3 arguments the 1st argument must be the number of rows (nRows: int).')
      if not isinstance(self.nCols,int): raise Exception('When using 2 or 3 arguments the 2nd argument must be the number of columns (nCols: int).')
      if   isinstance(vals,set ): values = lambda r,c: (r,c) in vals
      elif isinstance(vals,dict): values = lambda r,c: (r,c) in vals and vals[r,c]
      else: values = vals
      if not callable(values): raise Exception('Invalid 3rd argument. Must be of type set[int,int], map[(int,int) => bool] or (int,int)-> bool')
      self.__cells = [
        [ bool( values( r+self.rowOff, c+self.colOff ) )
          for c in range(self.nCols)
        ] for r in range(self.nRows)
      ]
    self._nextChanges = self._calculateNextChangesIntitially()

  @property
  def rowOff(self): return self.__rowOff

  @property
  def colOff(self): return self.__colOff

  @property
  def nRows(self):
    '''
    Returns the number of rows (horizontal lines) this Game of Life board has.
    '''
    return self.__nRows
  @property
  def nCols(self):
    '''
    Returns the number of columns (vertical lines) this Game of Life board has. 
    '''
    return self.__nCols
  @property
  def dim(self):
    '''
    Returns (nRows,nCols).
    '''
    return (self.nRows,self.nCols)

  @property
  def move(self,dRow,dCol):
    self.__rowOff += dRow
    self.__colOff += dCol
                        
  def __str__(self):
    '''
    Returns a human readable string version of this Game of Life board. Contains new-line characters.
    '''
    return (
#       '\n'.join( ''.join( '[X]' if cell else '[ ]' for cell in iRow ) for iRow in self.__cells )
        '┌' + 2*self.nCols*'─' + '┐\n'
      + '\n'.join( '│' + ''.join( '██' if cell else '  ' for cell in iRow ) + '│' for iRow in self.__cells )
      + '\n└' + 2*self.nCols*'─' + '┘\n'
    )

  def __getitem__(self,slc): # TODO allow toroidal access outside the boundaries
    '''
    If the input argument is of type (slice,slice), retrieves the specified subregion of this board as a new Board.
    If the input argument is of type (int,int), retrieves the specified cell's state as bool (True means alive, False means dead).
    If the input argument is of type (int,slice) or (slice,int), retrieves the specified row/colum strip as list[bool]
    
    For indexing the board is considered to be toroidal, i.e. if an index exceeds the bounds of the board it continues
    on the other side of the board.
    '''
    iRows, iCols = slc # <- called unpacking apparently
    # RETURN CELL VALUE
    if isinstance(iRows,int) and isinstance(iCols,int):
      iRows -= self.rowOff
      iCols -= self.colOff
      iRows %= self.nRows
      iCols %= self.nCols
      return self.__cells[iRows][iCols]
    # CHECK ROW SLICE VALIDITY
    if isinstance(iRows,int):
      iRows = [iRows]
    else:
      if not isinstance(iRows,    slice): raise Exception('Invalid row index/slice type: ' + str(type(iRows)) )
      if not isinstance(iRows.start,int): raise Exception("Invalid row slice's start attribute (must be int).")
      if not isinstance(iRows.stop ,int): raise Exception("Invalid row slice's stop  attribute (must be int).")
      step = iRows.step
      if None == step: step = 1
      if not isinstance(step,int): raise Exception('Invalid row step type: ' + str(type(step)) )
      iRows = range( iRows.start, iRows.stop, step )
    # CHECK COLUMN SLICE VALIDITY
    if isinstance(iCols,int):
      iCols = [iCols]
    else:
      if not isinstance(iCols,    slice): raise Exception('Invalid row index/slice type: ' + str(type(iCols)) )
      if not isinstance(iCols.start,int): raise Exception("Invalid column slice's start attribute (must be int).")
      if not isinstance(iCols.stop ,int): raise Exception("Invalid column slice's stop  attribute (must be int).")
      step = iCols.step
      if None == step: step = 1
      if not isinstance(step,int): raise Exception('Invalid column step type: ' + str(type(step)) )
      iCols = range( iCols.start, iCols.stop, step)
    # RETURN SUB-BOARD
    return DenseBoard(
      ( self[row,col] for col in iCols ) for row in iRows
    )

  def _indexOnBoard(self,row,col):
    row %= self.nRows
    col %= self.nCols
    if 0 > row: row = self.nRows - row
    if 0 > col: col = self.nCols - col
    return row,col

  def increment(self):
    '''
    Advances the Game of Life simulation by a single tick (time step).
    '''
    if not hasattr(self,'_nextChanges'):
      self._nextChanges = self._calculateNextChangesIntitially()
    for cell in self._nextChanges:
      self[cell] ^= True
    self._nextChanges = self._calculateNextChanges()

  def __iter__(self):
    '''
    Returns an iterator over the row and column indices of all living cells as an iterator[(int,int)].
    '''
    for iRow,row in enumerate(self.__cells):
      for iCol,cell in enumerate(row):
        if cell:
          yield self.rowOff+iRow, self.colOff+iCol

  def __setitem__(self, slc, val ):
    iRows, iCols = slc
    if isinstance(iRows,int) and isinstance(iCols,int):
      iRows -= self.rowOff
      iCols -= self.colOff
      iRows %= self.nRows
      iCols %= self.nCols
      self.__cells[iRows][iCols] = val
    else:
      raise Exception('Only __setitem__(self,(int,int)) implemented yet.')      

  def __copy__(self):
    return Board(self.__cells)

  def __deepcopy__(self, memodict={}):
    return copy(self)

def SparseBoard_load(path):
  board = SparseBoard( set() )
  row = 0
  with open(path) as f:
    if path.endswith('.cells'):
      for line in f:
        if not line.startswith('!'):
          for col,char in enumerate(line):
            if 'O' == char:
              board[row,col] = True
        row += 1
    elif path.endswith('.rle'):
      rle = filter(lambda x: not x.startswith('#'),f) # skip comments
      rle = [ line if not line.endswith('\n') else line[:-1] for line in rle ] # remove line breaks
      rle = ''.join(rle[1:]) # remove first line
      if not rle.endswith('!'):
        raise Exception('Invalid RLE ending.')
      rle = rle[:-1] # remove trailing '!'
      regex = r'(?P<NUM>\d+)|(?P<DEAD>b)|(?P<ALIVE>o)|(?P<NEW_ROW>\$)|(?P<MISMATCH>.)'
      count, col = 1, 0
      for mo in re.finditer(regex,rle):
        kind = mo.lastgroup
        if kind == 'MISMATCH':
          char = mo.group(kind)
          raise Exception( "Invalid character in RLE: '%(char)s'" % locals() )
        if   kind == 'NUM'    : count = int( mo.group(kind) )
        elif kind == 'NEW_ROW': row += count; count = 1; col = 0;
        elif kind == 'DEAD'   : col += count; count = 1 
        elif kind == 'ALIVE'  :
          for i in range(count):
            board[row,col+i] = True
          col += count
          count = 1
        else: raise Exception
#     elif path.endswith('.lif'): 
#       header = line[0]
#       if not header != '# Life 1.06 ':
#         raise Exception('Life (.lif) file version not supported.')
#       lines = f[1:]
    else: raise Exception('Unknown file ending.')
  return board

class SparseBoard(Board):
  
  def __init__(self,vals):
    '''
    Creates a new Game of Life board. The constructor expects either 1 (list[list[bool]]), 2 (int,int) or 3 (int,int,(int,int) -> bool) arguments.
    '''
    def checkEntry(x):
      row,col = x
      if not isinstance(row,int): raise Exception( 'Invalid key/enty: %(x)s.' % locals() )
      if not isinstance(col,int): raise Exception( 'Invalid key/enty: %(x)s.' % locals() )
      return (row,col)
    if   isinstance(vals,dict    ): self.__cells = { checkEntry(x) for x in filter(lambda x: vals[x], vals) }
    elif isinstance(vals,Iterable): self.__cells = { checkEntry(x) for x in map(checkEntry, vals) }
    else:
      raise Exception('Invalid argument.')

  def __getitem__(self,slc): # TODO allow toroidal access outside the boundaries
    '''
    If the input argument is of type (slice,slice), retrieves the specified subregion of this board as a new Board.
    If the input argument is of type (int,int), retrieves the specified cell's state as bool (True means alive, False means dead).
    If the input argument is of type (int,slice) or (slice,int), retrieves the specified row/colum strip as list[bool]
    
    For indexing the board is considered to be toroidal, i.e. if an index exceeds the bounds of the board it continues
    on the other side of the board.
    '''
    iRows, iCols = slc # <- called unpacking apparently
    # RETURN CELL VALUE
    if isinstance(iRows,int) and isinstance(iCols,int):
      return (iRows,iCols) in self.__cells
    # CHECK ROW SLICE VALIDITY
    if isinstance(iRows,int):
      iRows = [iRows]
    else:
      if not isinstance(iRows,    slice): raise Exception('Invalid row index/slice type: ' + str(type(iRows)) )
      if not isinstance(iRows.start,int): raise Exception("Invalid row slice's start attribute (must be int).")
      if not isinstance(iRows.stop ,int): raise Exception("Invalid row slice's stop  attribute (must be int).")
      step = iRows.step
      if None == step: step = 1
      if not isinstance(step,int): raise Exception('Invalid row step type: ' + str(type(step)) )
      iRows = range( iRows.start, iRows.stop, step )
    # CHECK COLUMN SLICE VALIDITY
    if isinstance(iCols,int):
      iCols = [iCols]
    else:
      if not isinstance(iCols,    slice): raise Exception('Invalid row index/slice type: ' + str(type(iCols)) )
      if not isinstance(iCols.start,int): raise Exception("Invalid column slice's start attribute (must be int).")
      if not isinstance(iCols.stop ,int): raise Exception("Invalid column slice's stop  attribute (must be int).")
      step = iCols.step
      if None == step: step = 1
      if not isinstance(step,int): raise Exception('Invalid column step type: ' + str(type(step)) )
      iCols = range( iCols.start, iCols.stop, step)
    # FIXME REMOVE IN PYTHON 3 {
    iRows = set(iRows)
    iCols = set(iCols)
    # }
    # RETURN SUB-BOARD
    return SparseBoard(
      filter(lambda (r,c): (r in iRows) and (c in iCols), self)
    )

  def increment(self):
    '''
    Advances the Game of Life simulation by a single tick (time step).
    '''
    if not hasattr(self,'_nextChanges'):
      self._nextChanges = self._calculateNextChangesIntitially()
    self.__cells ^= self._nextChanges
    self._nextChanges = self._calculateNextChanges()

  def __iter__(self):
    '''
    Returns an iterator over the row and column indices of all living cells as an iterator[(int,int)].
    '''
    return iter(self.__cells)

  def __setitem__(self, slc, val):
    iRows, iCols = slc
    if isinstance(iRows,int) and isinstance(iCols,int):
      if val: self.__cells.    add( (iRows,iCols) )
      else  : self.__cells.discard( (iRows,iCols) )
    else:
      raise Exception('Only __setitem__(self,(int,int)) implemented yet.')      

  def __copy__(self):
    return Board(self.__cells)

  def __deepcopy__(self, memodict={}):
    return copy(self)