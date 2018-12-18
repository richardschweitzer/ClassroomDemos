### packages ####
import pylab
import random
import numpy as np
import pandas as pd
from psychopy import logging, prefs
from psychopy import event, sound, core, visual


### parameters ####

TRAINING_MODE = False

path_to_exp = "/home/richard/Dropbox/STUDIUM_MIND_BRAIN/Active Vision/PRESENTATION/demo exp/"
path_to_result = path_to_exp + "design.csv"

# general
window_size = (1000,1000)
Ccenter = (0, 0)
fullscreen = False
background_rgb = [0,0,0]
text_rgb = [1,1,1]

# Parameters
nStim = 8
stimWidth = 0.01 # width of lines
stimLength = 0.05 # length of lines
Cradius = 0.6 # stimulus eccentricity
Tradius = 0.1  # radius of the top-down cues: circle and square
Twidth = 10 # line width for top-down cues
mask_text = '#'
mask_dur = 0.3
pre_presentation_dur = 0.2
post_presentation_dur = 0.2

### design
target_ori = [-45, 45]
color_swap = [0, 1]
n_reps = 2 # how many trial per cell?
color_1 = (255, 0, 0) # red
color_2 = (0, 0, 255) # blue
# SoAs
if TRAINING_MODE == True:
    SoAs = [0.4, 0.5]
else:
    SoAs = [0.050,0.100,0.200,0.400]


### prepare some standards ###
# the eight stimulus positions
anglesDeg = np.linspace(0, 315, nStim)
anglesRad = anglesDeg * (np.pi / 180)
xPosVector = np.sin(anglesRad) * Cradius + Ccenter[0]
yPosVector = np.cos(anglesRad) * Cradius + Ccenter[1]

# vectors for shuffling
ori_vector = target_ori * (nStim/2)
color_vector = [0] * nStim
shape_vector = [0] * nStim



### make design ###
dfs = []
cond_i = 0
for SoA in SoAs:
    for swap in color_swap:
        for ori in target_ori:
            for rep in range(n_reps):
                cond_i += 1
                # positions of the relevant stimuli
                target_pos = np.random.randint(nStim) # target position
                distract_pos = np.random.randint(nStim) # distractor position
                while distract_pos == target_pos: # they must not have the same position
                    distract_pos = np.random.randint(nStim)
                # stimuli in this trial
                trial_positions = range(nStim)
                np.random.shuffle(ori_vector)
                trial_oris = ori_vector
                trial_oris[target_pos] = ori # control for orientation of target
                trial_colors = [0] * nStim
                trial_colors[distract_pos] = 1 # distractor has to have different color
                trial_shapes = [0] * nStim
                trial_shapes[target_pos] = 1 # target has to have different shape
                # save in a pandas df
                df = pd.DataFrame({"trial_id": cond_i, 
                    "position": trial_positions, "position_x": xPosVector, "position_y": yPosVector,
                    "orientations": trial_oris, "colors": trial_colors, "shapes": trial_shapes, 
                    "target_ori": ori, "color_swap": swap, "SoA": SoA})
                dfs.append(df)
n_trials = len(dfs)
# shuffle the data
np.random.shuffle(dfs)
# add trial_nr
for trial in range(n_trials):
    df_temp = dfs[trial]
    df_temp['trial_nr'] = trial+1
    dfs[trial] = df_temp
# get trial 0
df_trial_zero = df_temp
# make one big data.frame
full_df = pd.concat(dfs) 
# save the design
if TRAINING_MODE == False:
    full_df.to_csv(path_to_result, index=False)
print("Total number of trials: " + str(trial+1))


#### the trial function ####
def runTrial(df_trial, c_1, c_2):
    trial_timer = core.Clock()
    # present fixcross
    fixcross.draw()
    myWin.flip()
    # 
    stimuli_prepared = False
    trial_timer.reset()
    trial_timer.add(pre_presentation_dur)
    # draw stimuli: loop over positions
    while trial_timer.getTime()<0:
        if stimuli_prepared==False:
            for s in range(nStim):
                df_pos = df_trial[df_trial.position==s]
                # line stimulus
                if int(df_pos.orientations) == target_ori[1]: # 45 deg, CW
                    line_stim = visual.Line(win=myWin, 
                        start = (float(df_pos.position_x)-(Tradius/2),float(df_pos.position_y)-(Tradius/2)), 
                        end = (float(df_pos.position_x)+(Tradius/2),float(df_pos.position_y)+(Tradius/2)) )
                else: # -45 deg, CCW
                    line_stim = visual.Line(win=myWin, 
                        start = (float(df_pos.position_x)+(Tradius/2),float(df_pos.position_y)-(Tradius/2)), 
                        end = (float(df_pos.position_x)-(Tradius/2),float(df_pos.position_y)+(Tradius/2)) )
                line_stim.setLineWidth(Twidth)
                line_stim.draw()
                # shape and color
                if int(df_pos.shapes) == 0: # rectangle
                    rect.setPos([float(df_pos.position_x), float(df_pos.position_y)])
                    if int(df_pos.colors) == 0: # normal stimuli
                        rect.setLineColor(c_1, 'rgb255')
                    else: # distractor
                        rect.setLineColor(c_2, 'rgb255')
                    rect.draw()
                else: # circle
                    circle.setPos([float(df_pos.position_x), float(df_pos.position_y)])
                    if int(df_pos.colors) == 0: # normal stimuli
                        circle.setLineColor(c_1, 'rgb255')
                    else: # distractor
                        circle.setLineColor(c_2, 'rgb255')
                    circle.draw()
            # fixcross
            fixcross.draw()
            # prepare next frame:
            myWin.callOnFlip(trial_timer.reset)
            myWin.callOnFlip(trial_timer.add, float(df_pos.SoA))
            # done
            stimuli_prepared = True
        else:
            pass
    # STIMULUS PRESENTATION HERE
    myWin.flip()
    print(df_trial[['target_ori', 'position', 'orientations', 'colors', 'shapes']])
#    event.waitKeys()
    stimuli_prepared = False
    while trial_timer.getTime()<0:
        if stimuli_prepared==False:
            # draw Masks
            fixcross.draw()
            for s in range(nStim):
                df_pos = df_trial[df_trial.position==s]
                mask_1.setPos([float(df_pos.position_x), float(df_pos.position_y)])
                mask_1.draw()
                mask_2.setPos([float(df_pos.position_x), float(df_pos.position_y)])
                mask_2.draw()
            # prepare next frame:
            myWin.callOnFlip(trial_timer.reset)
            myWin.callOnFlip(trial_timer.add, mask_dur)
            # done
            stimuli_prepared = True
        else:
            pass
    # MASK PRESENTATION
    myWin.flip()
    stimuli_prepared = False
    while trial_timer.getTime()<0:
        if stimuli_prepared==False:
            # post trial interval
            fixcross.draw()
            # done
            stimuli_prepared = True
        else:
            pass
    myWin.flip() # post mask interval
    core.wait(post_presentation_dur)
    event.waitKeys()


############### start exp ##################
start_exp=True
if start_exp==True:
    
    # create screen
    myWin =visual.Window(size=window_size, allowGUI=True, fullscr=fullscreen, rgb=background_rgb, winType='pyglet', units='norm')
    myWin.setRecordFrameIntervals(True)
    myWin.setMouseVisible(False)
    
    ## annouce EXP
    if TRAINING_MODE == True:
        announce_txt = visual.TextStim(win=myWin, text="Training session", color=text_rgb)
    else:
        announce_txt = visual.TextStim(win=myWin, text="Experiment session", color=text_rgb)
    announce_txt.draw()
    myWin.flip()
    event.waitKeys()
    core.wait(pre_presentation_dur)
    
    ## create standard visuals
    # the mask
    mask_1 = visual.TextStim(win=myWin, text=mask_text, color=color_1, height = Tradius*3, colorSpace = 'rgb255')
    mask_2 = visual.TextStim(win=myWin, text=mask_text, color=color_2, height = Tradius*3, colorSpace = 'rgb255', flipHoriz=True)
    # circle and square
    rect = visual.Rect(myWin, width=2*Tradius, height=2*Tradius)
    rect.setLineWidth(Twidth)
    circle = visual.Circle(myWin, radius=Tradius, edges=128)
    circle.setLineWidth(Twidth)
    # the fixation cross
    fixcross = visual.TextStim(win=myWin, text="+", color=text_rgb)
    
    # first blank screen
    myWin.flip()
    
    core.wait(0.5)
    
    ### show trial zero to establish an attentional set for color ###
    # annouce trial
    announce_txt = visual.TextStim(win=myWin, text="Trial Zero", color=text_rgb)
    announce_txt.draw()
    myWin.flip()
    event.waitKeys()
    core.wait(pre_presentation_dur)
    # select color
    distractor_color = np.random.randint(2) # randomize first color config
    if distractor_color == 0: # normal stim is now color 1 (red)
        trial_color_normal = color_1
        trial_color_distract = color_2
    else: # normal stim is now color 2 (blue)
        trial_color_normal = color_2
        trial_color_distract = color_1
    # run trial ZERO
    runTrial(df_trial_zero, trial_color_normal, trial_color_distract)
    
    ### loop over trials ###
    for trial in range(n_trials):
        # select trial data
        df_here = dfs[trial]
        print('Trial Nr. ' + str(np.unique(df_here.trial_nr)))
        print('SoA=' + str(np.unique(df_here.SoA)))
        # decide which color is which now
        do_color_swap = np.unique(df_here.color_swap)
        assert len(do_color_swap) == 1
        print('distractor_color was: ' + str(distractor_color))
        if do_color_swap == 1: # if there's a color swap happening in that trial
            print('performing color swap!')
            if distractor_color == 0: # 
                distractor_color = 1
            else:
                distractor_color = 0
        print('distractor_color is now: ' + str(distractor_color))
        if distractor_color == 0: # normal stim is now color 1 (red)
            trial_color_normal = color_1
            trial_color_distract = color_2
        else: # normal stim is now color 2 (blue)
            trial_color_normal = color_2
            trial_color_distract = color_1
        # annouce trial
        announce_txt = visual.TextStim(win=myWin, text="Trial Nr. " + str(trial+1), color=text_rgb)
        announce_txt.draw()
        myWin.flip()
        event.waitKeys()
        core.wait(pre_presentation_dur)
        # run trial
        runTrial(df_here, trial_color_normal, trial_color_distract) # color 1: normal stim, color 2: distractors
    
    ## goodbye
    announce_txt = visual.TextStim(win=myWin, text="Thanks for your participation!", color=text_rgb)
    announce_txt.draw()
    myWin.flip()
    event.waitKeys()
    core.wait(pre_presentation_dur)
    

#### close everything ####
myWin.close()
core.quit()



