import tkinter as tk
import time
from tkmacosx import Button
import threading


GREEN = '#5ACD96' # Custom green

state = 'START' # state = text on button, opposite of clock ( state = start and the clock is pausing, state = stop and the clock is running )
color = True # Color of countdown - blue for workTime and green for pauseTime
phase = 0 # Phases from 0-7 jump between workTime, pauseTime and longPausetime

workTime = 25*60 # 25 minutes work time
pauseTime = 5*60 # 5 minute pause time
longPauseTime = 30*60 # 30 minute long pause time
currentTime = workTime # start current time with work time

minutes = currentTime // 60
seconds = currentTime % 60


# copied from another project (https://github.com/EVILBEAN-cmd/StockChartsPlotter)
class Buttons: 
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def placeButton(self):
        """
        inital creation of button
        """ 
        button = Button(root, text=state, height=5, width=10, bg='black', fg=GREEN, activeforeground=GREEN, borderless=1, activebackground='black', focuscolor=GREEN, command=lambda: self.changeButton(button) )
        button.grid(column=self.x, row=self.y, sticky='NSWE')


    
    def changeButton(self, button):
        """
        change button depending on state
        """ 
        global thread     
        global state


        if state == 'START':
            state = 'STOP'

            button.configure(height=5, width=10, fg='red', activebackground='black', activeforeground='red', focuscolor='red', text=state ) # change to red stop state

            thread.append(threading.Timer(1.0, logic)) # adds new thread too thread list
            thread[len(thread)-1].start() # runs thread in thread list

        elif state == 'STOP':
            state = 'START'

            button.configure(height=5, width=10, fg=GREEN, activebackground='black', activeforeground=GREEN, focuscolor=GREEN, text=state) # change to green start state  
            
            thread[len(thread)-1].cancel() # cancels thread in thread list
            thread.append(threading.Timer(1.0, logic)) # adds new thread in thread list
            


def changePhase():
    """
    changes phases of timer and updates currentTime to new time
    """
    global phase
    global currentTime
    global color
    

    phase += 1


    if phase%2 == 0:
        currentTime = workTime
    elif phase == 7:
        currentTime = longPauseTime
        color = False
        phase = 0
    else:
        currentTime = pauseTime
        color = False



def logic():
    """
    0. creates initial thread list that tracks the time
    1. updates current time, minutes, seconds and calls the changePhase() function
    2. chnages timer color
    3. calls itself every second in order to update the time (recursive)
    """
    global currentTime
    global thread
    global minutes 
    global seconds

    # 0.
    thread = [threading.Timer(1.0, logic)]
    

    # 1. 
    minutes = currentTime // 60
    seconds = currentTime % 60

    if currentTime == 0:
        changePhase()

    currentTime -= 1


    # 2. 
    if color:
        timer.configure(text=(minutes, ':', seconds), fg='blue')
    elif not(color):
        timer.configure(text=(minutes, ':', seconds), fg=GREEN)


    # 3.
    if state == 'STOP':

        thread.append(threading.Timer(1.0, logic))
        thread[len(thread)-1].start()
   






if __name__ == '__main__':
    """
    0. creates tkmacosx window
    1. places button and timer
    2. calls logic function
    """

    # 0.
    root = tk.Tk()

    root.title('Pomodoro')
    root.geometry('1133x600')
    root.config(bg='black')
    
    # Button Grid
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.rowconfigure(root, 1, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)


    # 1.
    b0 = Buttons(0, 1)
    b0.placeButton()
    
    timer = tk.Label(master=root, text=(minutes, ':', seconds), bg="black", fg='blue', font=('SF Pro', 100))
    timer.grid(column = 0, row = 0)
    

    # 2.
    logic()

    root.mainloop()