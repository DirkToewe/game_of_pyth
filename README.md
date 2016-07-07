Game of Pyth(on)
================

Game of Pyth is my first Python project. It is an implementation of [Convay's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

Board
=====

The ```Board``` represents the current state of the simulation and keeps track of the living cells. The ```increment()``` method advances the Game of Life simulation by a single time step. For a ```Board``` ```board``` the ```board[row: int, col: int]``` method returns True if and only if the cell at row row and column col is alive. With ```board[row,col] = new_state``` changes the board state of a cell. All currently living cells can be iterated:

```python
for row,col in board:
  print( 'cell (%(row)d,%(col)d) lives' % locals() )
```

DenseBoard
-----------

The ```DenseBoard``` has a finite size of ```nRows```⨯```nCols``` cells. The board behaves, as if it was the surface of a toroid: the left and right side as well as top and bottom are connected to one another. The ```DenseBoard``` can be converted to a multi-line string representation using the str() method. The dense board can be crated from a twodimensional iterable:
```python
from org.jengineering import GameOfPyth

board = GameOfPyth.DenseBoard(
  [[0]*18]*4 +
  [[0]*5+[1,1,1,1,1,1,1,1]+[0]*5,
   [0]*5+[1,0,1,1,1,1,0,1]+[0]*5,
   [0]*5+[1,1,1,1,1,1,1,1]+[0]*5] +
  [[0]*18]*4
)
```

```DenseBoard``` can also be created from a...:
  * set[(int,int)] storing the living cell entries
  * map[(int,int),bool] representing cell states or a, which represents the alive (True) and dead (False) state for (some) cells
  * callable (int,int) -> bool, which returns True if a cell at the given input index is alive

```python
board = GameOfPyth.DenseBoard(56,56,lambda r,c: random() < 0.1)
```

SparseBoard
-----------

```SparseBoard``` has a potentially infinite number of cells. It can be created from a ```set[(int,int)]```:

```python
board = GameOfPyth.DenseBoard(
  set([(0,1), (3,3), (2,1), (1,0), (0,3), (3,4), (2,4), (3,5)])
)
```

Since ```Board``` is an ```iterable[(int,int)]```, a ```DenseBoard``` can easily be converted to a ```SparseBoard```:

```python
board = GameOfPyth.SparseBoard(
  set(GameOfPyth.DenseBoard([
    [1,1,1,0,1],
    [1,0,0,0,0],
    [0,0,0,1,1],
    [0,1,1,0,1],
    [1,0,1,0,1]
  ]))
)
```

Visualization
=============

The ```GameOfPyth.Widget``` allows You to display the ```Board```, run the simulation and vary the simulation speed. The mouse wheel allows You to zoom. Holding down the primary mouse button scrolls the view.

```python
from PyQt4.QtGui import QApplication
import sys

app = QApplication(sys.argv)
wdgt = GameOfPyth.Widget(board)
wdgt.setGeometry(200,200,800,600)
wdgt.show()
sys.exit( app.exec_() )
```
