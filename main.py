from concurrent.futures import ThreadPoolExecutor
from tkinter import *
from tkinter import filedialog
from functools import partial
from time import sleep

class ConwayCells(Tk):
    """Class used to make conways game of life using the tkinter module"""

    def __init__(self, master):
        """Defualt constructer. Used to create the grid"""

        #Parallel dictionaries---------
        self.conwayButtons = {} #These are the individual buttons widgets that are displayed on the board
        self.identities = {} #Individual idetity of each button so down in self.changeCell() we are able to use it to change the properties of that button
        self.neighbors = {}  #Dictionary that corelates to the coordinate of the button and how many neighbors are alive
        self.state = {}      #Tells whether the button is alive or dead
        #-------------------------------

        self.pool = ThreadPoolExecutor(100)
        self.cycles = 0      #How many cycles have passed
        self.cycle_label = Label(text = 0)
        self.cycle_label.grid(row = 0, column = 10, rowspan = 4)

        #Construct the grid
        for x in range(20):
            for y in range(20):
                self.neighbors[(x, y)] = 0
                self.conwayButtons[(x, y)] = Button(master, width=1, text=" ", bg = "light grey", command = partial(self.changeCell, (x,y)))
                self.conwayButtons[(x, y)].grid(row = x+1, column = y)

                self.identities[(x, y)] = self.conwayButtons[(x, y)]
                self.state[(x, y)] = False

        #Go through just one cycle
        self.next_button = Button(master, width = 6, text = "Next", command = self.oneCycle)
        self.next_button.grid(row =21, column = 0, columnspan = 3)

        #Start the cycles
        self.start_button = Button(master,bg = "light grey", width = 6, text = "Start", command = self.startCycles)
        self.start_button.grid(row = 22, column = 0, columnspan = 3)

        #Stop the cycles
        self.stop_button = Button(master, width = 6, text = "Stop", command = self.stopCycles)
        self.stop_button.grid(row = 22, column = 3, columnspan = 3)

    def startCycles(self):
        """This starts incrementing through each cycle at .25 seconds for each one"""
        self.pool.submit(self.oneCycle)
        self.stop = self.next_button.after(250, self.startCycles)

    def stopCycles(self):
        """Stops cycling"""
        self.start_button.after_cancel(self.stop)

    def oneCycle(self):
        """Just goes through each cycle, and establishes the rules for Conways Game of Life"""
        instructions = []
        for c in self.state: #If the cell is alive
            if (self.state[c]):
                if (self.neighbors[c] == 2 or self.neighbors[c] == 3): #let them live
                    pass
                else: #Kill the cell
                    instructions.append(c)
            
            else:
                if (self.neighbors[c] == 3): #Bring a cell to life
                    instructions.append(c)

        for i in instructions:
            self.changeCell(i)
        self.cycles += 0
        self.cycle_label.configure(text = self.cycles)


    def changeCell(self, x):
        """Changes a cell from an alive state to a dead state OR a dead one to an alive one"""
        bname = (self.identities[x])
        if not (bname["bg"] == "red"):
            bname.configure(bg="red")
            self.state[x] = True
        else:
            bname.configure(bg = "light grey")
            self.state[x] = False
 
        for i in self.state:
            self.neighbors[i] = self.determineNeighbor(i)


    def determineNeighbor(self, tuplee):
        """Determines how many neighbors a cell has given the coordinate"""
        x = tuplee[0]
        y = tuplee[1]

        #----------------------------------
        #OOO (x-1, y+1) (x, y+1) (x+1, y+1)
        #OOO (x-1, y)   (x, y)   (x+1, y)
        #OOO (x-1, y-1) (x, y-1) (x+1, y-1)
        #----------------------------------
        
        def neighbor(x1, y1):
            """Determines if the cell is a neighbor"""
            try:
                self.state[(x1, y1)]
            except KeyError: #Doesn't exist
                return False
            else:
                return self.state[(x1, y1)] #The state is already True or False so just return that

        total = 0

        #Goes around ad checks every possible neighbor
        for n in [(x-1, y+1), (x, y+1), (x+1, y+1), (x-1, y), (x+1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]: 
            if (neighbor(n[0], n[1])):
                total += 1

        return total            

def main():
    """Establish the mainWindow and runs its mainloop"""
    mainWindow = Tk()
    x = ConwayCells(mainWindow)
    mainWindow.mainloop()

if __name__ == '__main__':
    main()