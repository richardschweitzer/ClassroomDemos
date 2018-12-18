#### packages needed ####
from psychopy import visual, event, core, sound
from numpy import  *
import sys
from psychopy import logging, prefs
#from scikits.audiolab import wavread, wavwrite
from psychopy import gui

#### datasource
wait_time = 0.7
marker_dur = 0.400
marker_hz = 500
intervals = [0, 4, 13, 6, 10, 2, 8, 16, 19];
#intervals = [0, 1, 1, 2, 1, 2, 1, 1, 1];


#### the trial function
def present_interval(trial_id, interval):
    trial_timer = core.MonotonicClock()
    # make marker sound
    marker_sound = sound.Sound(marker_hz, marker_dur)
    # announce trial
    if interval == 0:
        trial_id = 'test'
        interval = 2
    # make text on screen
    trial_announce = visual.TextStim(win=myWin, text='Interval ' + str(trial_id) + ' - Ready?', pos=(0,0))
    trial_screen = visual.TextStim(win=myWin, text='Interval ' + str(trial_id), pos=(0,0))
    marker_stimulus = visual.GratingStim(myWin, tex=None, mask="gauss", size=0.5)
    marker_stimulus.setPos([0,-0.3])
    trial_announce.draw()
    myWin.flip()
    event.clearEvents()
    event.waitKeys()
    trial_screen.draw()
    myWin.flip()
    core.wait(wait_time) # pre-trial wait
    ## interval start
    # here we draw the visual stimulus and play the marker
    trial_screen.draw()
    marker_stimulus.draw()
    myWin.flip()
    marker_sound.play()
    play_start = trial_timer.getTime()
    core.wait(marker_dur)
    # here we wait with a blank screen
    trial_screen.draw()
    myWin.flip()
    core.wait(interval) # ISI
    ## interval end
    # here we draw the visual stimulus a second time 
    trial_screen.draw()
    marker_stimulus.draw()
    myWin.flip()
    marker_sound.play()
    core.wait(marker_dur) # post-trial wait
    myWin.flip()
    # save real interval duration (2 marker_dur have to be subtracted since sound.play() is a non-blocking method) 
    play_dur = trial_timer.getTime() - play_start - 2*marker_dur 
    return play_dur




#### here goes the MAIN EXPERIMENT ####
start_exp=True

   
if start_exp==True:
    # open file for saving all trial data
    clock_results = list()
    # create a window
    myWin =visual.Window((700,700), allowGUI=True, bitsMode=None, units='norm', winType='pyglet', fullscr=False )
    begin = visual.TextStim(win=myWin, text="Exp. 1: Estimation of Interval Duration")
    begin.draw()
    myWin.flip()
    event.waitKeys()
    core.wait(wait_time)
    
    # run trials
    trial_id = 0
    for interval in intervals:
        myWin.flip()
        core.wait(wait_time)
        real_dur = present_interval(trial_id, interval)
        trial_id += 1
        clock_results.append(real_dur)
    
    
    # goodbye and thank you
    myWin.flip()
    ending_1 = visual.TextStim(win=myWin, text="Experiment done.", pos=(0,0))
    ending_1.draw()
    myWin.flip()
    # button press to end
    event.waitKeys()
    # close everything
    print(clock_results)
    myWin.close()
    core.quit()