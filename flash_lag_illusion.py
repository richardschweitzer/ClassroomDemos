### packages ####
import pylab
import random
import numpy as np
from psychopy import logging, prefs
from psychopy import event, sound, core, visual
import matplotlib
matplotlib.use('Qt4Agg')#change this to control the plotting 'back end'


### parameters ####
window_size = (950,900)
# general
center = (0, 0)
fullscreen = False
background_rgb = [-1,-1,-1]
text_rgb = [1,1,1]
# Parameters
nDots = 140
dotSize = 0.15
Mradius = 0.2  # radius of movement
Cradius = 0.1 # radius of circle
circle_width = 10
flash_size = 0.1

start_exp=True
############### start demo ##################
if start_exp==True:
    
    # create screen
    myWin =visual.Window(size=window_size, fullscr=fullscreen, rgb=background_rgb, winType='pyglet', units='norm')
    myWin.setRecordFrameIntervals(True)
    myWin.setMouseVisible(False)
    # create standard visuals
    fixcross = visual.TextStim(win=myWin, text="+", color=text_rgb)
    fixcross.draw()
    myWin.flip()
    
    # Movement track
    anglesDeg = np.linspace(0, 360, nDots)
    anglesRad = anglesDeg * (np.pi / 180)
    xPosVectorT = np.sin(anglesRad)  * Mradius + center[0]
    yPosVectorT = np.cos(anglesRad) * Mradius + center[1]
    
    # prepare circle
    circle = visual.Circle(myWin, radius=Cradius, edges=128)
    circle.setLineWidth(circle_width)
    circle.setLineColor(text_rgb)
    
    # prepare flash
    flash = visual.GratingStim(myWin, tex=None, mask="gauss", size=flash_size)
    flash.setColor(text_rgb)
    
    i = 0
    flash_after_nr_frames = random.randint(nDots-80, nDots-1)
    # loop over frames
    end_loop = False
    while not end_loop:
        # draw fixcross
        fixcross.draw()
        # draw circle
        circle.setPos([xPosVectorT[i], yPosVectorT[i]])
        circle.draw()
        # draw flash
        if i == flash_after_nr_frames:
            flash.setPos(circle.pos)
            flash.draw()
            flash_after_nr_frames = random.randint(nDots-80, nDots-1)
            if event.getKeys():
                myWin.flip()
                event.waitKeys()
                end_loop = True
        # reset i
        i = i + 1
        if i >= nDots:
            i = 0
        # flip screen
        myWin.flip()

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