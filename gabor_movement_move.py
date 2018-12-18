#!/usr/bin/env python2
from psychopy import core, visual, event
visual.useFBO=True#if available (try without for comparison)
import matplotlib
import pylab

# initialize
myWin = visual.Window([1024,768], 
                      allowGUI = True, 
                      fullscr = True, 
                      waitBlanking = True)
myWin.setRecordFrameIntervals()
# fixation points
point_a = visual.TextStim(myWin, text="+",  pos=(-0.7,0.1))
point_b = visual.TextStim(myWin, text="+",  pos=(0.7,0.1))
# instruction
instr = visual.TextStim(myWin, text="First, look at the gray flickering in the middle of the screen. Then, try to rapidly move your eyes back and forth between the left and right fixation points. Do you still see only gray?", 
                            pos=(0,-0.75),  wrapWidth = 1.8)

# gabor grating
gabor_size = 0.7
gabor = visual.GratingStim(myWin,
                            pos = (0,0.1),
                            tex="sin",
                            mask="gauss",
                            texRes=512, # 512
                            color="blue",
                            size=[gabor_size,gabor_size], 
                            sf=[6,0], 
                            ori = 0)

for i in range(15): # get the hardware ready
    gabor.draw()
    point_a.draw()
    point_b.draw()
    instr.draw()
    myWin.flip()


# phase
#    Phase of the stimulus in each dimension of the texture.
#    Should be an x,y-pair or scalar
#    NB phase has modulus 1 (rather than 360 or 2*pi) This is a little unconventional but has the nice effect that setting phase=t*n drifts a stimulus at n Hz
phase = 0.5
step = 0.025
frames_until_getKeys = 5

# start demo
end_demo = False
while end_demo == False:
    #    gabor.setPhase(phase,'+')
    gabor.phase += phase
    gabor.draw()
    point_a.draw()
    point_b.draw()
    instr.draw()
    myWin.flip()
    
    frames_until_getKeys -= 1
    # handle key presses after each 5th frame
    if frames_until_getKeys <= 0:
        for keys in event.getKeys(timeStamped=True):
            if keys[0] in ['escape','q']:
                end_demo = True
            elif keys[0] in ['s']:
                if phase<0.5:
                    phase += step
                    print(phase)
            elif keys[0] in ['a']:
                if phase>-0.5:
                    phase -= step
                    print(phase)
            frames_until_getKeys = 5

# end of demo
myWin.close()

# end of script
core.quit()


# plot the frameintervals: from timeByFrames PsychoPy Demo
intervalsMS = pylab.array(myWin.frameIntervals)*1000
m=pylab.mean(intervalsMS)
sd=pylab.std(intervalsMS)
se=sd/pylab.sqrt(len(intervalsMS)) # for CI of the mean
distString= "Mean=%.1fms, s.d.=%.2f, 99%%CI(frame)=%.2f-%.2f" %(m,sd,m-2.58*sd,m+2.58*sd)
nTotal=len(intervalsMS)
nDropped=sum(intervalsMS>(1.5*m))
droppedString = "Dropped/Frames = %i/%i = %.3f%%" %(nDropped,nTotal, 100*nDropped/float(nTotal))
# plot here
pylab.figure(figsize=[12,8])
pylab.subplot(1,2,1)
pylab.plot(intervalsMS, '-')
pylab.ylabel('t (ms)')
pylab.xlabel('frame N')
pylab.title(droppedString)

pylab.subplot(1,2,2)
pylab.hist(intervalsMS, 50, normed=0, histtype='stepfilled')
pylab.xlabel('t (ms)')
pylab.ylabel('n frames')
pylab.title(distString)
pylab.show()

