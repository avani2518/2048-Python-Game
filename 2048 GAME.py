from tkinter import *   #standard python library for creating GUI
from tkinter import messagebox  #for messageboxes(alerts,messages, warnings, etc)
import random   #for generating random number, here : 2

class Board:    
    bg_color = {            #for background color of the blocks - dictionary
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#edc850',
        '16': '#edc53f',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#f2b179',
        '1024': '#f59563',
        '2048': '#edc22e',
    }
    color = {               #for the text of the numbers in the blocks - dictionary
        '2': '#776e65',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#776e65',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }

    def __init__(self):     #for attributes initialization
        self.n = 4  #attribute, 4x4 grid creation 
        self.window = Tk()  #attribute, creates new tkinter window object
        self.window.title('2048 Game by - AVANI HALBE')   #attribute, title of the tkinter window
        self.gameArea = Frame(self.window, bg='azure3') #attribute, creating a frame widget
        self.board = [] #attribute which is an empty list, holds the labels representing the tiles of the game board(represents the game board )
        self.gridCell = [[0] * 4 for i in range(4)] #attribute, 2D list with 4x4 dimensions, each cell is initialized with 0(empty), MATRIX = 2D LIST
        self.compress = False   #boolean flags which are attributes, to check whether any compression has been performed(initial state)
        self.merge = False  #boolean flags which are attributes, to check whether the tiles of the same number have been combined
        self.moved = False  #boolean flags which are attributes, to check whether any tile has moved
        self.score = 0  #attribute, initial score = 0

        #compress : moving in any of the four directions
        #merge : combining the tiles/blocks of the same number

        #frame widget : used to organize and group other widgets, a rectangular window
        #label widget : used to display text or images on a window or a frame


        for i in range(4):      #for loop for creating rows
            rows = []       #empty list, used to collect label widgets
            for j in range(4):      #for loop for creating columns
                l = Label(self.gameArea, text='', bg='azure4',  #l = label widget, represents a single cell on the game board
                          font=('arial', 22, 'bold'), width=4, height=2)
                l.grid(row=i, column=j, padx=7, pady=7)

                rows.append(l)      #the list collects the label widgets for the current row
            self.board.append(rows)     #appending rows to self.board
        self.gameArea.grid()        #to make the frame widget visible to the tkinter window

    def reverse(self):  #method, used to reverse the order of the elements within each row of the game
        for ind in range(4):    #loop iterates over the rows, ind = index    
            i = 0   #represents first element of the row
            j = 3   #represents last element of the row
            while(i < j):   #loop continues until i and j meet or cross each other
                self.gridCell[ind][i], self.gridCell[ind][j] = self.gridCell[ind][j], self.gridCell[ind][i] #swap operation, swap values of the elements in the same row
                i += 1  #increments value by 1
                j -= 1  #increments value by 1

    def transpose(self):    #method, transpose the matrix, switches rows and columns
        self.gridCell = [list(t) for t in zip(*self.gridCell)]  #zip : built - in python function which takes iterables and combines them, self.gridcell : 2D list
        #* : used for unpacking(extracting elements), zip : takes the transposed rows and returns an iterator - USED TO TRANSPOSE THE GAME BOARD


    def compressGrid(self):    #method, compresses the game board by removing the empty cells
        self.compress = False   #to check whether any compression has been performed
        temp = [[0] * 4 for i in range(4)]  #creates a list containing 4 zeros, for loop creates 4 copies of the list[0, 0, 0, 0], CREATES A 2D LIST - TEMP(4x4)
        for i in range(4):  #iterates over the rows of the game board
            cnt = 0 #count variable keeps track of the current index
            for j in range(4):  #iterates over the columns of the game board
                if self.gridCell[i][j] != 0:    #checks if the current tile/cell is non zero
                    temp[i][cnt] = self.gridCell[i][j]  # temp[i][cnt] : refers to a specific element in the 2D list(temporary storage), self.gridCell[i][j] : accesses a specific element in the 2D list
                    #performs an assignment operation
                    if cnt != j:    #checks if the current index in the temporary list (cnt) is different from the column index (j)
                        self.compress = True    #if a compression has occurred
                    cnt += 1    #increments the value by 1
        self.gridCell = temp    #updates the game board with the contents of the temporary list -   temp

    def mergeGrid(self):    #method, merges the adjacent tiles
        self.merge = False  #used to track whether any tiles have been merged
        for i in range(4):  #iterates over the rows
            for j in range(4 - 1):  #iterates three times upto the third column, avoiding index out of range
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0: #checks whether the current tile has the same value as the tile to its right(next column) and if the current tile is non zero
                    #if the above condition is true, the tiles can be merged
                    self.gridCell[i][j] *= 2    #doubles the value of the current tile as both the tiles have been merged. *= : multiplication and assignment operations done
                    self.gridCell[i][j + 1] = 0   #tile to the right of the current tile, assigns a value of 0 to the tile immediately to the right of the current tile, removes the tile from the game board
                    self.score += self.gridCell[i][j]   #increments the game score by the value of the current tile after it has been merged with its neighboring tile
                    self.merge = True   #indicates that atleast one merge operation has occurred

    def random_cell(self):  #generates a new tile with a value of 2 at a random empty cell on the game board
        cells = []    #initializes an empty list, stores the coordinates of the empty cells
        for i in range(4):  #iterates over the rows
            for j in range(4):  #iterates over the columns
                if self.gridCell[i][j] == 0:    #checks if the value of the cell at coordinates (i, j) on the game board is equal to 0, meaning the cell is empty(new tile can be placed)
                    cells.append((i, j))    #if emoty, a tuple (i, j) representing its coordinates is appended to the list(adds the tile to the list)
        curr=random.choice(cells)   #select a random tuple from the cells list
        i = curr[0]   #extract the row index (i) from the selected tuple curr
        j = curr[1]   #extract the column index (j) from the selected tuple curr
        self.gridCell[i][j] = 2   #assigns the value 2 to the randomly chosen empty cell at coordinates (i, j) on the game board(random 2 generation completed)
    
    def can_merge(self):    #method, determines whether any merge is possible on the game board, checks all the adjacent pairs of cells(horizontally and vertically)
        for i in range(4):  #for loop that iterates over the rows of the game board
            for j in range(3):  #for loop that iterates over the columns of the game board, loop runs uptill 3 because each cell is compared to its adjacent cell(j + 1)
                if self.gridCell[i][j] == self.gridCell[i][j + 1]:  #checks whether the current cell has the same value as that of the cell to its right(column)
                    return True #if a pair of adjacent cell is found, merge is possible

        for i in range(3):  #loop iterates from 0 to 3, prevents accessing out of bound indices
            for j in range(4):  #loop iterates over the columns
                if self.gridCell[i + 1][j] == self.gridCell[i][j]:  ##checks whether the current cell has the same value as that of the cell to its right(row)
                    return True #if a pair of adjacent cell is found, merge is possible
                
        return False    #returns false if no pair of adjacent cells are found

    def paintGrid(self):    #method, updates the graphical representation of the game board, iterates over each cell in the gridCell data structure
        for i in range(4):  #iterate over the rows
            for j in range(4):  #iterate over the columns
                if self.gridCell[i][j] == 0:    #checks if the current cell is zero, if yes it indicates an empty cell
                    self.board[i][j].config(text='', bg='azure4')   #configures the label widget, self.board[i][j] : accesses the label widget
                    #config() : method provided by the tkinter library, used to configure various properties of the widget(change the properties dynamically), text : an empty string(if the cell has value 0) 
                else:   #if the current cell in the game grid is not empty
                    self.board[i][j].config(text=str(self.gridCell[i][j]),  #converts the value of the current cell into a string
                                            bg=self.bg_color.get(str(self.gridCell[i][j])), #determines the bg color of the label widget, uses the bg_color dictionary's get() method to retrieve the corresponding background color of the cell
                                            fg=self.color.get(str(self.gridCell[i][j])))    #determines the color of the text of the label widget, uses the color dictionary's get() method to retrieve the corresponding foreground color of the cell

#class board completes

class Game:
    def __init__(self, gamepanel):  #for attributes initialization, two arguments : self and gamepanel, which is passed as an argument when creating a new Game object
        self.gamepanel = gamepanel  #assigns the value of the gamepanel paramete to the self.gamepanel attribute of the current instance of the Game class, ensures that the Game object has access to the gamepanel object
        self.end = False    #used to track whether the game has ended(initially false)
        self.won = False    #used to track whether the player has won the game(initially false)


    def start(self):    #responsible for initializing the game and setting up the game board
        self.gamepanel.random_cell()    #calls the random_cell() method of the gamepanel object, which is an instance of the Board class, randomly selects an empty cell on the game board and places a new tile with a value of 2 at that location
        self.gamepanel.random_cell()    #for random generation of 2 tiles
        self.gamepanel.paintGrid()    #updates the graphical representation of the game board based on the current state of the gridCell attribute
        self.gamepanel.window.bind('<Key>', self.link_keys) #accesses the window attribute of the gamepanel object
         #bind() : method provided by Tkinter, used to associate event handlers with specific events on a widget(allows you to define what should happen when a particular event occurs)
        #<Key> : specifies the event to bind to(for any key press), self.link_keys : event handler method that will be called when the specified event occurs
        #bind : widget.bind(event, handler) -> SYNTAX
        #widget : self.gamepanel.window, event : <key>, handler ; self.link_keys
        self.gamepanel.window.mainloop()    #accesses the window attribute of the gamepanel object, mainloop() : method, a Tkinter-specific function that enters the Tkinter event loop, responsible for running the tkinter event loop, handles events

    
    def link_keys(self,event):  #method, two paramteres : self and event, refres to the current instance of the class, responsible for handling key press events within the Tkinter window
        if self.end or self.won:    #if any one of the conditions is true, the the method exits without executing any further code(if the game has ended or the player has won)
            return

        self.gamepanel.compress = False #ndicates whether any compression (movement of tiles to remove empty spaces) has been performed on the game board(initially false)
        self.gamepanel.merge = False    #indicates whether any tiles of the same number have been merged (combined) during the previous move(initially false)
        self.gamepanel.moved = False    #indicates whether any tile has been moved during the previous move(initially false)

        presed_key=event.keysym #extracts the symbolic name of the key that was pressed during a key press event
        #event : parameter passed to the link_keys method, representing the event object associated with the key press event
        #event.keysym : represents the symbolic name of the key that was pressed

        if presed_key=='Up':    #checks if the up key has been pressed
            self.gamepanel.transpose()  #esponsible for transposing the game board, switching the rows and columns
            self.gamepanel.compressGrid()   #compresses the game board by removing empty cells and shifting tiles towards the top of the board.
            self.gamepanel.mergeGrid()  #merges adjacent tiles with the same value vertically, starting from the top of the board and moving downwards
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge  #updates the moved attribute based on whether any compression or merging occurred during the current move
            #if either compression or merging occurred, moved is set to true, otherwise it remains false
            self.gamepanel.compressGrid()
            self.gamepanel.transpose()

        elif presed_key=='Down':    #checks if the down key has been pressed
            self.gamepanel.transpose()
            self.gamepanel.reverse()    #responsible for reversing the order of elements within each row of the game board.
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
            self.gamepanel.transpose()

        elif presed_key=='Left':    #checks if the left key has been pressed
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()

        elif presed_key=='Right':   #checks if the right key has been pressed
            self.gamepanel.reverse()
            self.gamepanel.compressGrid()
            self.gamepanel.mergeGrid()
            self.gamepanel.moved = self.gamepanel.compress or self.gamepanel.merge
            self.gamepanel.compressGrid()
            self.gamepanel.reverse()
        else:
            pass
        
        #provides visual feedback to the player about the current state of the game board (through updating the display) and displays the score to keep the player informed about their progress
        self.gamepanel.paintGrid()  #updates the graphical representation of the game board
        print(self.gamepanel.score) #prints the current score of the game

        flag = 0    #used to indicate whether a tile with the value 2048 is found on the game board(maximum value on the game board)
        for i in range(4):  #loop iterates over the rows 
            for j in range(4):  #loop iterates over the columns
                if self.gamepanel.gridCell[i][j] == 2048:   #checks if the value of the cell is equal to 2048
                    flag = 1    #made flag 1 as a tile with the cell value 2048 is found
                    break   #used to exit the inner loop immediately when a tile with the value 2048 is found


        if(flag == 1): #found 2048
            self.won = True #as tile with 2048 is found indicating the player has won
            messagebox.showinfo('2048', message='You Wonnn!!')  #shows the message that the player has won
            print("won")
            return

        #determines the availability of empty cells (value = 0)
        for i in range(4):  #loop iterates over the rows
            for j in range(4):  #loop iterates over the columns
                if self.gamepanel.gridCell[i][j] == 0:   #checks if the value of the cell is equal to 0
                    flag = 1    #made flag 1 as a tile with the cell value 0 is found
                    break

        if not (flag or self.gamepanel.can_merge()):    #checks if the flag or the gamepanel.can_merge is true
            self.end=True   #set to true if the above condition is met
            messagebox.showinfo('2048','Game Over!!!')  #shows the message that the player has lost
            print("Over")

        if self.gamepanel.moved:
            self.gamepanel.random_cell()
        
        self.gamepanel.paintGrid()
    

gamepanel = Board() #gamepanel : instance of the board class
game2048 = Game( gamepanel) #game2048 : instance of the game class, with gamepanel as an argument
game2048.start()    #initiates the gameplay loop

#Board : Represents the game board and handles visual representation
#Game : Manages the game logic, including starting the game and determining win/loss conditions.

#object of the BOARD class : gamepanel
#object of the GAME class : game2048