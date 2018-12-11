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
# Constants and Variables
############################################################################################
scr_w = 1920
scr_h = 1060
exp_id = "PSY_G5"           # Name of the Disrectory where data is stored
presentation = 1            # When '1' number of trials are reduced for a faster demo
training_done = "False"     # To extend the training on user request
trials  = []                # List of all possible Stimuli
ttrials = []                # Training Trials List
etrials = []                # Experiment Trials List

############################################################################################
#Get date and timeStamped
############################################################################################
dt = datetime.datetime.now()
date = dt.strftime("%x");
time = dt.strftime("%X");

############################################################################################
# Generate User ID
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
if gui.OK:  
    print(gui.data[0])
else:
    sys.exit("user cancelled")
    
pattern=re.compile(r'^([1-9]{2})'
                   r'([m|M|f|F])'
                   r'([a-zA-Z]{4})')

valid_in = pattern.findall(gui.data[0])
if valid_in:
    usr_id = gui.data[0]
    os.chdir(exp_id+"/")
    file = usr_id+".csv"
    file = file.lower()

    if os.path.exists(file):
        gui = psychopy.gui.Dlg(title="File already exists", pos=(400, 800))
        gui.addText('Please contact the coordinator', color='Black')
        gui.show()
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
    size=(scr_w, scr_h),
    units='pix',
    #fullscr=True,
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
############################################################################################
for i in range (1,13):   # To generate all 12 possible stimuli
    # Congruent Trials
    if(i == 1):
        trials.append([0, rs_rect, rt_rect, 'm'])
    elif(i == 2):
        trials.append([0, rs_tri, rt_tri, 'o'])
    elif(i == 3):
        trials.append([0, bs_rect, bt_rect, 'x'])
    elif(i == 4):
        trials.append([0, bs_tri, bt_tri, 'w'])
    #Inconcruent Trials - Shape
    elif(i == 5):
        trials.append([1, rs_tri, rt_rect, 'o'])
    elif(i == 6):
        trials.append([1, rs_rect, rt_tri, 'm'])
    elif(i == 7):
        trials.append([1, bs_tri, bt_rect, 'w'])
    elif(i == 8):
        trials.append([1, bs_rect, bt_tri, 'x'])
    #incongruent trails - Color
    elif(i == 9):
        trials.append([2, bs_rect, rt_rect, 'x'])
    elif(i == 10):
        trials.append([2, bs_tri, rt_tri, 'w'])
    elif(i == 11):
        trials.append([2, rs_rect, bt_rect, 'm'])
    elif(i == 12):
        trials.append([2, rs_tri, bt_tri, 'o'])

if presentation == 1 :
    ttrials = [trials[0]]+[trials[4]]+[trials[8]]+[trials[6]]+[trials[10]]+[trials[2]]
    etrials = [trials[1]]+[trials[5]]+[trials[9]]+[trials[7]]+[trials[11]]+[trials[3]]
else:
    ttrials = trials
    etrials = trials + trials

shuffle(ttrials)
shuffle(etrials)
############################################################################################
# Fixation Sign
############################################################################################
#fixation = psychopy.visual.Rect(
#    win=win, 
#    size=100,
#    lineColor="Black",
#    fillColor="Black")    
fixation = psychopy.visual.TextStim(
    win=win, 
    text="*******", 
    color="black",
    pos=[0,0], 
    bold=True)
############################################################################################
 #Define message texts
############################################################################################
errormsg = psychopy.visual.TextStim(
    win=win,
    text="No valid button was pressed",
    color="DarkRed"
)

wrongAnswer = psychopy.visual.TextStim(
    win=win,
    text="Your answer was wrong",
    color="DarkRed"
)

intromsg1 = psychopy.visual.TextStim(
    win=win,
    wrapWidth=800,
    text="""
    You will see a Rectangle or Traingle drawn on the screen which can be either Blue or Red.\n
    
    You will also see some text printed in the middle of the shape. \n
    
    You are required to identify the shape and color of the figure while ignoring the text\n
    
    The following is the keys must be pressed corresponding to the shape you see \n
    'w' for Blue Triangle \n
    'x' for Blue Rectangle \n
    'o' for Red Triange \n
    'm' for Red Rectangle \n

    Press any key to see an example.""",
    color="Black"
)

ExampleMsg = psychopy.visual.TextStim(
    win=win,
    wrapWidth=800,
    text="""
    For the stimuli below you should press 'x' on the keyboard\n\n\n\n\n\n\n\n\n\n\n

    """,
    color="Black"
)

intromsg1_contd = psychopy.visual.TextStim(
    win=win,
    wrapWidth=800,
    text="""
    'w' for Blue Triangle \n
    'x' for Blue Rectangle \n
    'o' for Red Triange \n
    'm' for Red Rectangle \n

    We will start with a few training trials.\n
""",
    color="Black"
)

cont_training = psychopy.visual.TextStim(
    win=win,
    wrapWidth=800,
    text="""
    Are you confortable with the experiment?\n
    Press 'n' to continue training\n
    Press any other button to move to experiment trials\n
""",
    color="Black"
)


intromsg2 = psychopy.visual.TextStim(
    win=win,
    wrapWidth=800,
    text="""
    We will now start with the real experiment.\n
    Please try to press the correct button as fast as possible:\n\n\n
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

clock.reset()
while clock.getTime() < .2:
    trials[8][1].draw() 
    trials[8][2].draw()
    ExampleMsg.draw()
    win.flip()
    wait = psychopy.event.waitKeys()

intromsg1_contd.draw()
win.flip()
wait = psychopy.event.waitKeys()

while(training_done == "False"):
    for trial in ttrials: 
        shape = trial[1]
        text = trial[2]
        clock.reset()

        while clock.getTime() < .5:
            fixation.draw()
            win.flip()

        keys = []
        psychopy.event.clearEvents()
        clock.reset()
        while clock.getTime() < 2.5:
           shape.draw() 
           text.draw()
           win.flip()

        keys = psychopy.event.getKeys(
           keyList=["w","x","o","m"],
           timeStamped = clock
        )

        if not keys: 
            print (keys)
            currenttime = clock.getTime()
            while clock.getTime() < currenttime + 4:
               errormsg.text = "No valid button was pressed\nThe correct key would have been '" + trial[3] + "'"
               errormsg.draw()
               win.flip()

        else: 
            if(keys[0][0]=="w" and trial[3]=="w") or (keys[0][0]=="x" and trial[3]=="x") or (keys[0][0]=="o" and trial[3]=="o") or (keys[0][0]=="m" and trial[3]=="m"):
                print ('Correct Answer') 
            else:
                currenttime = clock.getTime()
                while clock.getTime() < currenttime + 4:
                    wrongAnswer.text = "You entered the wrong key \nThe correct key would have been '" + trial[3] + "'"
                    wrongAnswer.draw()
                    win.flip()
    
    cont_train = []
    psychopy.event.clearEvents()
    clock.reset()
    while clock.getTime() < 5:
        cont_training.draw()
        win.flip()

    cont_train = psychopy.event.getKeys(
                 keyList=["n"],
                 timeStamped = clock
    )
    
    if cont_train:
        if(cont_train[0][0] == "n"):
            training_done = "False"
        else:
            training_done = "True"
    else:
        training_done = "True"
#    gui = psychopy.gui.Dlg(title="Are you ready to continue ?", labelButtonOK='No', labelButtonCancel='Yes', pos=(600, 800))
#    gui.addText('Click No for more training trials', color='Black')
#    gui.show()
#    if gui.OK:  
#        training_done = "False"
#    else:
#        training_done = "True"
############################################################################################
# Run Experiment Trials
############################################################################################
intromsg2.draw()
win.flip()
wait = psychopy.event.waitKeys()

data = [["User ID","Date","Time","Trial No.","Congruent/Incongruent","Expected Responce","User Response","Timestamp"]]
count = 0

if presentation == 1:
    etrail_cnt = 6
else:
    etrail_cnt = 24

clock = psychopy.core.Clock()
while(count < etrail_cnt):
    for trial in etrials: 
        if(count == etrail_cnt):
            break
        else:
            count = count + 1
            
            clock.reset()
            
            while clock.getTime() < .5:
                fixation.draw()
                win.flip()
            
            keys = []
            
            psychopy.event.clearEvents()
            
            clock.reset()
            
            while clock.getTime() < 2.5:
                trial[1].draw()
                trial[2].draw()
                win.flip()
            
            keys = psychopy.event.getKeys(
                keyList=["o","m","w","x"],
                timeStamped = clock
            )

            if not keys: 
                print (keys)
                currenttime = clock.getTime()
                while clock.getTime() < currenttime + 4:
                    pressed = -999
                    reaction = -999
                    errormsg.text = "No valid button was pressed\nThe correct key would have been '" + trial[3] + "'"
                    errormsg.draw()
                    win.flip()

            else: 
                if(keys[0][0]=="w" and trial[3]=="w") or (keys[0][0]=="x" and trial[3]=="x") or (keys[0][0]=="o" and trial[3]=="o") or (keys[0][0]=="m" and trial[3]=="m"):
                    pressed = keys[0][0]
                    reaction = keys[0][1]
                    print ('Correct Answer') 
                else:
                    pressed = -999
                    reaction = -999
                    currenttime = clock.getTime()
                    while clock.getTime() < currenttime + 4:
                        wrongAnswer.text = "You entered the wrong key \nThe correct key would have been '" + trial[3] + "'"
                        wrongAnswer.draw()
                        win.flip()

            data.append( 
                [
                    usr_id,
                    date,
                    time,
                    count,
                    trial[0],
                    trial[3],
                    pressed,
                    reaction
                ]
            )
#print(data)
############################################################################################
# End message
############################################################################################
endmsg.draw()
win.flip()
wait = psychopy.event.waitKeys()
############################################################################################
# Make numeric
############################################################################################
for i in range(len(data)):
    if data[i][5] == "o" : data[i][5] = 0
    if data[i][6] == "o" : data[i][6] = 0
    
    if data[i][5] == "m" : data[i][5] = 1
    if data[i][6] == "m" : data[i][6] = 1
    
    if data[i][5] == "w" : data[i][5] = 2
    if data[i][6] == "w" : data[i][6] = 2
    
    if data[i][5] == "x" : data[i][5] = 3
    if data[i][6] == "x" : data[i][6] = 3

############################################################################################
# Save
############################################################################################
with open(file, mode="wb") as writefile: 
    writer = csv.writer(writefile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in data: 
        writer.writerow(row)

win.close()
