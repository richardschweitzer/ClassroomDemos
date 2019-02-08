### packages ####
import pylab
import random
import numpy as np
from psychopy import logging, prefs
from psychopy import event, sound, core, visual
import matplotlib
matplotlib.use('Qt4Agg')#change this to control the plotting 'back end'


### parameters ####
# general
window_size = (980,900)
Ccenter = (0, 0)
fullscreen = False
background_rgb = [-1,-1,-1]
text_rgb = [1,1,1]
# Parameters
nDots = 60
dotSize = 0.01
Cradius = 0.33 # Clock radius
Tradius = 0.3 # Hand track radius
numbers_on_clock = 12
flash_size = 0.1
frames_per_second = 3
final_wait = 2

start_exp=True
############### start demo ##################
if start_exp==True:
    
    # create screen
    myWin =visual.Window(size=window_size, fullscr=fullscreen, allowGUI=True, rgb=background_rgb, winType='pyglet', units='norm')
    myWin.setRecordFrameIntervals(True)
    myWin.setMouseVisible(False)
    # create standard visuals
    fixcross = visual.TextStim(win=myWin, text="+", color=text_rgb)
    fixcross.draw()
    myWin.flip()
    # Clock: 12 numbers
    anglesDeg = np.linspace(30, 360, numbers_on_clock)
    anglesRad = anglesDeg * (np.pi / 180)
    xPosVector = np.sin(anglesRad) * Cradius + Ccenter[0]
    yPosVector = np.cos(anglesRad) * Cradius + Ccenter[1]
    # prepare numbers
    numbers = list()
    for i in range(1,numbers_on_clock+1):
        number = visual.TextStim(win=myWin, text=str(i), pos=[xPosVector[i-1], yPosVector[i-1]], height=0.05)
        numbers.append(number)
    
    # Hand track: 60 small dots
    anglesDeg = np.linspace(6, 360, nDots)
    anglesRad = anglesDeg * (np.pi / 180)
    xPosVectorT = np.sin(anglesRad)  * Tradius + Ccenter[0]
    yPosVectorT = np.cos(anglesRad) * Tradius + Ccenter[1]
    dotsT = visual.ElementArrayStim(myWin, elementTex=None, elementMask='gauss', 
        nElements=nDots, sizes=dotSize)
    dotsT.setXYs(np.rot90(np.matrix([xPosVectorT, yPosVectorT])))
    dotsT.setColors(text_rgb)
    
    # clock hand
    hand_anchor = Ccenter
    hand_target_x = xPosVectorT
    hand_target_y = yPosVectorT
    second = 0
    
    # prepare flash
    flashPosX = xPosVectorT*1.5
    flashPosY = yPosVectorT*1.5
    flash = visual.GratingStim(myWin, tex=None, mask="gauss", size=flash_size)
    flash.setColor(text_rgb)
    flash_after_nr_frames = random.randint(0, nDots-1)
    
    # loop over frames
    end_loop = False
    while not end_loop:
        second = second + 1
        if second >= 60:
            second = 0
        hand = visual.Line(myWin, hand_anchor, (hand_target_x[second], hand_target_y[second]), lineColor = text_rgb)
        for i in range(frames_per_second):
            # draw dots
            dotsT.draw()
            # draw numbers
            for n in numbers:
                n.draw()
            # draw hand
            hand.draw()
            # draw flash
            if second == flash_after_nr_frames and i == 0:
                flash.setPos([flashPosX[second],flashPosY[second]])
                flash.draw()
                flash_after_nr_frames = random.randint(0, nDots-1)
                if event.getKeys():
                    end_loop = True
                    myWin.flip()
                    core.wait(final_wait)
                    event.waitKeys()
                    break
            # flip screen
            myWin.flip()
        #core.wait(0.040) # make the frames longer artificially

    #### close everything ####
    myWin.close()
    
    # frametiming (timeByFrames)
    #calculate some values
    intervalsMS = pylab.array(myWin.frameIntervals)*1000
    m=pylab.mean(intervalsMS)
    sd=pylab.std(intervalsMS)
    # se=sd/pylab.sqrt(len(intervalsMS)) # for CI of the mean
    distString= "Mean=%.1fms, s.d.=%.2f, 99%%CI(frame)=%.2f-%.2f" %(m,sd,m-2.58*sd,m+2.58*sd)
    nTotal=len(intervalsMS)
    nDropped=sum(intervalsMS>(1.5*m))
    droppedString = "Dropped/Frames = %i/%i = %.3f%%" %(nDropped,nTotal, 100*nDropped/float(nTotal))
    
    #plot the frameintervals
    pylab.figure(figsize=[12,8])
    pylab.subplot(1,2,1)
    pylab.plot(intervalsMS, '-')
    pylab.ylabel('t (ms)')
    pylab.xlabel('frame N')
    pylab.title(droppedString)
    #
    pylab.subplot(1,2,2)
    pylab.hist(intervalsMS, 50, normed=0, histtype='stepfilled')
    pylab.xlabel('t (ms)')
    pylab.ylabel('n frames')
    pylab.title(distString)
    pylab.show() 