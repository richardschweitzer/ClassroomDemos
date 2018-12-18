# a demo to elucidate the concept of masking. It is not timing clean and doesn't have to be.
# 2017, richard schweitzer


from psychopy import visual, logging, core, event
visual.useFBO=True#if available (try without for comparison)
import numpy as np
import random


n_trials = [0, 0, 1, 1, 2, 2, 3, 3]
n_pre = 30
n_frames = 120
target_frames = 3
mask_frames = 15
after_answer_dur = 0.5
standard = "   "
mask = "###"
pre_mask = "%%%"
answer_key_right = 'right'
answer_key_left = 'left'
escape_key = 'q'
option_eccentricity = 0.2
text_height = 0.2
text_rgb = [1,1,1]


# create screen
# prepare window
win = visual.Window([900,800], fullscr=False, allowGUI=False, waitBlanking=True)
win.setRecordFrameIntervals(True)
win.setMouseVisible(False)
# get framerate
framerate = win.getActualFrameRate(nIdentical=80, nMaxFrames=100, nWarmUpFrames=80, threshold=0.5)
print("framerate: " + str(framerate))
# prepare stimuli
standard_stim = visual.TextStim(win, text=standard, height=text_height, color=text_rgb)
mask_stim = visual.TextStim(win, text=mask, height=text_height, color=text_rgb)
pre_mask_stim = visual.TextStim(win, text=pre_mask, height=text_height, color=text_rgb)
fixcross = visual.TextStim(win, text="+", height=text_height, color=text_rgb)
# timer
trial_timer = core.Clock()

for trial in n_trials:
    # prepare trial
    rt = 0.0
    correct = 0
    trial_timer.reset()
    
    # mask or no mask
    if trial==0:
        mask_code = 0 # no mask
    elif trial==1:
        mask_code = 2 # mask
    elif trial==2:
        mask_code = 2
        pre_mask_code = 3
    
    # produce a target number
    number = random.randint(100, 999)
    target_1_stim = visual.TextStim(win, text=str(number), height=text_height, color=text_rgb)

    # where will target appear
    target_presentations = np.zeros(n_frames)
    if mask_code < 3:
        target_pos = random.randrange(0, n_frames-target_frames-mask_frames)
    elif mask_code == 3:
        target_pos = random.randrange(mask_frames, n_frames-target_frames-mask_frames)
    
    for i in range(target_frames):
        target_presentations[target_pos+i] = 1 # set the position for the target frame
    for i in range(mask_frames):
        target_presentations[target_pos+target_frames+i] = mask_code
        if trial == 2:
            target_presentations[target_pos-mask_frames+i] = mask_code
        elif trial == 3:
            target_presentations[target_pos-mask_frames+i] = pre_mask_code
    
    fixcross.draw()
    win.flip()
    event.waitKeys()
    core.wait(0.5)
    
    print(target_presentations)
    
    event.clearEvents()
    ### start trial
    for frame in range(n_pre):
        standard_stim.draw()
        win.flip()
    for frame in target_presentations:
        if frame==0:
            standard_stim.draw()
        elif frame==1:
            target_1_stim.draw()
        elif frame==mask_code: # mask_code = 2
            mask_stim.draw()
        elif frame==pre_mask_code: 
            pre_mask_stim.draw()
        win.flip()
    ### answer screen
    fixcross.draw()
    answer_screen_time = win.flip()
    win.setRecordFrameIntervals(False)
    # prepare next window
    win.callOnFlip(trial_timer.reset) 
    win.callOnFlip(trial_timer.add, after_answer_dur) # wait while the answer is shown
    # expect answer
    event.clearEvents()
    fixcross.draw()
    win.flip()
    while trial_timer.getTime()<0:
        pass

core.wait(1)

# end experiment
win.saveFrameIntervals(fileName=None, clear=True)
win.close()
core.quit()