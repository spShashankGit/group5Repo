import psychopy.visual
import psychopy.event
import psychopy.core
import psychopy.gui
import datetime
import os
import sys
import random
import csv
import re
from random import shuffle
from psychopy.visual import ShapeStim
############################################################################################
# Constants
############################################################################################
exp_id = "PSY_G5"
trials  = []
ttrials = []
etrials = []

############################################################################################
#Get date and timeStamped
############################################################################################
dt = datetime.datetime.now()
date = dt.strftime("%x");
time = dt.strftime("%X");
#print(date, time)


############################################################################################
# Start: Input fields
############################################################################################
gui = psychopy.gui.Dlg(title="User ID", pos=(400, 800))
gui.addText('Format of User ID is', color='Black')
gui.addText('      1. AGE -> NN', color='Black')
gui.addText('      2. SEX -> M/F', color='Black')
gui.addText('      3. First 2 letters of your first name and last name', color='Black')
gui.addText('Example : For a guy named Sven Milz aged 32', color='Blue')
gui.addText('      User ID -> 32MSVMI', color='Blue')
gui.addField("User ID:")
gui.show()

pattern=re.compile(r'^([1-9]{2})'
                   r'([m|M|f|F])'
                   r'([a-zA-Z]{4})')

valid_in = pattern.findall(gui.data[0])
#valid_in = 1
#print(valid_in)
if valid_in:
    os.chdir(exp_id+"/")
    file = gui.data[0]+".csv"
    file = file.lower()

    if os.path.exists(file):
        sys.exit("File already exists")
else: 
    gui = psychopy.gui.Dlg(title="Invalid User ID", pos=(400, 800))
    gui.addText('Try Again', color='Black')
    gui.show()
    sys.exit("Invalid User ID \nTry Again")
############################################################################################
# Create window
############################################################################################
win = psychopy.visual.Window(
    #size=(1024, 768),
    units='pix',
    fullscr=True,
    color=[1, 1, 1]
)
############################################################################################
# Definition of stimuli
############################################################################################
triangle  = [(0,3500),(-2500,-1500),(2500,-1500)]
rectangle = [(-2000,2000),(-2000,-2000),(2000,-2000),(2000,2000)]

rs_rect = ShapeStim(win, vertices=rectangle, fillColor=(1,0,0), size=.05, lineColor=(1,0,0))
rt_rect = psychopy.visual.TextStim(win=win, text="Red Square", color="red",pos=[0,0], bold=True)

rs_tri = ShapeStim(win, vertices=triangle, fillColor=(1,0,0), size=.05, lineColor=(1,0,0))
rt_tri = psychopy.visual.TextStim(win=win, text="Red Triangle", color="red",pos=[0,0], bold=True)

bs_rect = ShapeStim(win, vertices=rectangle, fillColor=(0,0,1), size=.05, lineColor=(0,0,1))
bt_rect = psychopy.visual.TextStim(win=win, text="Blue Square", color="blue",pos=[0,0], bold=True)

bs_tri = ShapeStim(win, vertices=triangle, fillColor=(0,0,1), size=.05, lineColor=(0,0,1))
bt_tri = psychopy.visual.TextStim(win=win, text="Blue Triangle", color="blue",pos=[0,0], bold=True)

############################################################################################
# Create training and Experiment trials
# Each word is shown, colours completely randomized
############################################################################################
for i in range (1,13):   # To generate all 12 possible stimuli
    # Congruent Trials
    if(i == 1):
        trials.append([0, rs_rect, rt_rect])
    elif(i == 2):
        trials.append([0, rs_tri, rt_tri])
    elif(i == 3):
        trials.append([0, bs_rect, bt_rect])
    elif(i == 4):
        trials.append([0, bs_tri, bt_tri])
    #Inconcruent Trials - Shape
    elif(i == 5):
        trials.append([1, rs_tri, rt_rect])
    elif(i == 6):
        trials.append([1, rs_rect, rt_tri])
    elif(i == 7):
        trials.append([1, bs_tri, bt_rect])
    elif(i == 8):
        trials.append([1, bs_rect, bt_tri])
    #incongruent trails - Color
    elif(i == 9):
        trials.append([2, bs_rect, rt_rect])
    elif(i == 10):
        trials.append([2, bs_tri, rt_tri])
    elif(i == 11):
        trials.append([2, rs_rect, bt_rect])
    elif(i == 12):
        trials.append([2, rs_tri, bt_tri])

ttrials = trials
shuffle(ttrials)

etrials = trials + trials
shuffle(etrials)

while not psychopy.event.getKeys():
    ttrials[0][1].draw()
    ttrials[0][2].draw()

    win.flip()

win.close()
############################################################################################
# Fixation Sign
############################################################################################
fixation = psychopy.visual.Rect(
    win=win, 
    size=10,
    lineColor="Black",
    fillColor="Black")
    
############################################################################################
 #Define message texts
############################################################################################
errormsg = psychopy.visual.TextStim(
    win=win,
    text="No correct button was pressed",
    color="DarkRed"
)

intromsg1 = psychopy.visual.TextStim(
    win=win,
    wrapWidth=800,
    text="""
    You will see several word that are either printed
    in Blue or Green. Your task is to press the correct button
    as quickly as possible: \n\n
    A for Blue \n
    L for Green \n\n
    We will start with a few training trials.\n
    Press any key to start.""",
    color="Black"
)

intromsg2 = psychopy.visual.TextStim(
    win=win,
    wrapWidth=800,
    text="""
    We will now start with the real experiment.\n
    Please press again the correct button as fast as possible:\n\n
    A for Blue \n
    L for Green \n\n
    Press any key to start.""",
    color="Black"
)

endmsg = psychopy.visual.TextStim(
    win=win,
    wrapWidth=800,
    text="""
    Thank you.\n
    The experiment is now finished.\n""",
    color="Black"
)

############################################################################################
# Run training trials
############################################################################################
clock = psychopy.core.Clock()

intromsg1.draw()
win.flip()

wait = psychopy.event.waitKeys()

for trial in ttrials: 
    
    text = trial[3]
    
    clock.reset()
    
    while clock.getTime() < .5:
        fixation.draw()
        win.flip()
      
    keys = []

    psychopy.event.clearEvents()
    
    clock.reset()

    while clock.getTime() < 1.75:
        text.draw()
        win.flip()
    
    keys = psychopy.event.getKeys(
        keyList=["a","l"],
        timeStamped = clock
    )
    
    if not keys: 
        currenttime = clock.getTime()
        while clock.getTime() < currenttime + 4:
            errormsg.draw()
            win.flip()
    else: 
        if (keys[0][0]=="a" and trial[1]==1) or (keys[0][0]=="l" and trial[1]==2):
            currenttime = clock.getTime()
            while clock.getTime() < currenttime + 4:
                errormsg.draw()
                win.flip()

intromsg2.draw()
win.flip()

wait = psychopy.event.waitKeys()

############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
data = []

count=0

clock = psychopy.core.Clock()

for trial in etrials: 
    
    count = count + 1
    
    text = trial[4]
    
    clock.reset()
    
    while clock.getTime() < .5:
        fixation.draw()
        win.flip()
    
    keys = []
    
    psychopy.event.clearEvents()
    
    clock.reset()
    
    while clock.getTime() < 1.75:
        trial[1].draw()
        trial[2].draw()

        win.flip()
    
    keys = psychopy.event.getKeys(
        keyList=["w","x","o","m"],
        timeStamped = clock
    )
    
    if keys:      
        if (keys[0][0]=="a" and trial[2]==1) or (keys[0][0]=="l" and trial[2]==2):
            pressed = -999
            reaction = -999
            currenttime = clock.getTime()
            while clock.getTime() < currenttime + 4:
                errormsg.draw()
                win.flip()
        else: 
            pressed = keys[0][0]
            reaction = keys[0][1]
    else: 
        pressed = -999
        reaction = -999
        currenttime = clock.getTime()
        while clock.getTime() < currenttime + 4:
            errormsg.draw()
            win.flip()

    data.append( 
        [
            gui.data[0],
            date,
            time,
            count,
            trial[0],

            pressed,
            reaction
        ]
    )

# End message

endmsg.draw()
win.flip()
wait = psychopy.event.waitKeys()

# Make numeric

for i in range(len(data)):
    if data[i][7] == "a" : data[i][7] = 2
    if data[i][7] == "l" : data[i][7] = 1
