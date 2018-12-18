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



#### the trial function
def make_interval(min, max):
    import random
    return random.randint(min, max)


def present_interval(trial_id, interval, announce):
    trial_timer = core.MonotonicClock()
    # make marker sound
    marker_sound = sound.Sound(marker_hz, marker_dur)
    marker_stimulus = visual.GratingStim(myWin, tex=None, mask="gauss", size=0.5)
    marker_stimulus.setPos([0,-0.3])
    # announce trial
    if interval == 0:
        trial_id = 'test'
        interval = 2
    # make text on screen
    if announce:
        trial_screen = visual.TextStim(win=myWin, text='Interval ' + str(trial_id), pos=(0,0))
        myWin.flip()
        trial_screen.draw()
    myWin.flip()
    core.wait(wait_time) # pre-trial wait
    ## first sound
    marker_stimulus.draw()
    if announce:
        trial_screen.draw()
    myWin.flip()
    marker_sound.play()
    play_start = trial_timer.getTime()
    core.wait(marker_dur)
    if announce:
        trial_screen.draw()
    myWin.flip()
    core.wait(interval) # ISI
    ## second sound
    marker_stimulus.draw() 
    if announce:
        trial_screen.draw()
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
    exp_timer = core.Clock()
    # create a window
    myWin =visual.Window((700,700), allowGUI=True, bitsMode=None, units='norm', winType='pyglet', fullscr=False )
    
    ## 1. estimation of interval duration
    interval = make_interval(2, 5)
    solution = visual.TextStim(win=myWin, text="The interval had a duration of " + str(interval) + " seconds.")
    begin = visual.TextStim(win=myWin, text="Verbal Estimation. Please say much time passed in the following interval.")
    begin.draw()
    myWin.flip()
    event.waitKeys()
    core.wait(wait_time)
    # run trial
    myWin.flip()
    core.wait(wait_time)
    real_dur = present_interval(0, interval, False)
#    print(real_dur)
    # show solution
    myWin.flip()
    event.clearEvents()
    event.waitKeys()
    solution.draw()
    myWin.flip()
    event.waitKeys()
    
    ## 2. production
    interval = make_interval(2, 5)
    myWin.flip()
    begin = visual.TextStim(win=myWin, text="Production. Please produce an interval of " + str(interval) + " seconds by pressing the space bar twice.")
    begin.draw()
    myWin.flip()
    # run trial
    event.clearEvents()
    event.waitKeys()
    start_production = exp_timer.getTime()
    myWin.flip()
    event.clearEvents()
    event.waitKeys()
    production_interval = exp_timer.getTime() - start_production
    solution = visual.TextStim(win=myWin, text="The interval you produced had a duration of " + str(round(production_interval, 2)) + " seconds.")
    myWin.flip()
    core.wait(wait_time)
    myWin.flip()
    # show solution
    solution.draw()
    myWin.flip()
    event.clearEvents()
    event.waitKeys()
    myWin.flip()

    ## 3. reproduction
    interval = make_interval(2, 5)
    begin = visual.TextStim(win=myWin, text="Reproduction. First listen to the following interval and then reproduce this interval by pressing space twice.")
    begin.draw()
    myWin.flip()
    event.waitKeys()
    core.wait(wait_time)
    # first play interval
    myWin.flip()
    core.wait(wait_time)
    real_dur = present_interval(0, interval, False)
#    print(real_dur)
    begin = visual.TextStim(win=myWin, text="Now reproduce. Start by pressing space. Then press space again to stop.")
    myWin.flip()
    begin.draw()
    myWin.flip()
    # now reproduce interval
    event.clearEvents()
    event.waitKeys()
    start_production = exp_timer.getTime()
    myWin.flip()
    event.clearEvents()
    event.waitKeys()
    production_interval = exp_timer.getTime() - start_production
    myWin.flip()
    solution = visual.TextStim(win=myWin, text="The interval you heard had a duration of " + str(interval) + " seconds. You reproduced an interval of " + str(round(production_interval, 2)) + " seconds.")
    myWin.flip()
    solution.draw()
    myWin.flip()
    event.clearEvents()
    event.waitKeys()
    myWin.flip()
    
    
    ## 4. Comparison
    interval_1 = make_interval(2, 5)
    interval_2 = make_interval(2, 5)
    while interval_1 == interval_2: # randomize long enough to produce an interval which is not the same as interval 1
        interval_2 = make_interval(2, 5)
    solution = visual.TextStim(win=myWin, text="Interval 1 = " + str(interval_1) + " s,    interval 2 = " + str(interval_2) + " s.")
    begin = visual.TextStim(win=myWin, text="Comparison. You'll hear two intervals. Please decide which of them was longer.")
    begin.draw()
    myWin.flip()
    event.waitKeys()
    core.wait(wait_time)
    # run interval 1
    myWin.flip()
    core.wait(wait_time)
    myWin.flip()
    real_dur = present_interval(1, interval_1, True)
#    print(real_dur)
    # run interval 2
    myWin.flip()
    core.wait(wait_time)
    core.wait(wait_time)
    myWin.flip()
    real_dur = present_interval(2, interval_2, True)
#    print(real_dur)
    # show solution
    myWin.flip()
    event.clearEvents()
    event.waitKeys()
    solution.draw()
    myWin.flip()
    event.waitKeys()
    
    # goodbye and thank you
    myWin.flip()
    ending_1 = visual.TextStim(win=myWin, text="Demo done.", pos=(0,0))
    myWin.flip()
    ending_1.draw()
    myWin.flip()
    # button press to end
    event.waitKeys()
    # close everything
    myWin.close()
    core.quit()