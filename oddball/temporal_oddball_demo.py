# -*- coding: utf-8 -*-

# Temporal Oddball Effect Demo
# by richard 11/2015

#### packages ####
import pylab
import numpy as np
from psychopy import logging, prefs
from psychopy import event, sound, core, visual
from psychopy import gui
from psychopy.iohub import launchHubServer, EventConstants  # needs: msgpack , psutil, xlib, 


def trial_instruction(win, kb, text):
    core.wait(0.5)
    kb.clearEvents()
    text_on_screen = visual.TextStim(win=win, text=text, pos=(0,0), height=fixcross_height, color=text_rgb)
    text_on_screen.draw()
    myWin.flip()
    while not kb.getEvents():
        pass


#####################                                   this is the real trial                            ##############################
def oddball_trial(win, kb, oddball_filename, standard_filename, oddball_pos, comparison_dur): 
    trial_timer = core.Clock()
    stimuli_prepared = False
    trial_timer.reset()
    trial_timer.add(isi_dur)
    ###################### isi before first stimulus, stimuli are prepared here #################
    while trial_timer.getTime()<0:
        if stimuli_prepared==False:
            # set variables
            rt = 0.0
            key = "timeout"
            correct = 0
            # create list of presentations (standards and oddball)
            presentations = np.zeros(stim_presentations)
            presentations[oddball_pos-1] = 1 # set the position of the oddball to 1
            # prepare the stimuli to be shown
            standard = visual.ImageStim(win, image=standard_filename, size=(pic_size,pic_size), pos=(0,0))
            oddball = visual.ImageStim(win, image=oddball_filename, size=(pic_size,pic_size), pos=(0,0))
            # prepare the answer screen
            fixcross = visual.TextStim(win=win, text="+", pos=(0,0), height=fixcross_height, color=text_rgb)
            Or = visual.TextStim(win=win, text="or", pos=(0,0), height=fixcross_height, color=text_rgb)
            right_option = visual.TextStim(win=win, text=answer_right,  pos=(0.4,0), height=fixcross_height, color=text_rgb) # [::-1] for hebrew
            left_option = visual.TextStim(win=win, text=answer_left,  pos=(-0.4,0), height=fixcross_height, color=text_rgb)
            # prepare next window: the presentation of a standard
            standard.draw()
            win.callOnFlip(trial_timer.reset)
            win.callOnFlip(trial_timer.add, standard_dur)
            stimuli_prepared = True
        else:
            pass
    ########################### loop over all presentations ######################
    for p in range(len(presentations)):
        ##### picture is presented #####
        win.flip() 
        isi_prepared = False
        while trial_timer.getTime()<0:
            if isi_prepared==False:
                win.callOnFlip(trial_timer.add, isi_dur)
                isi_prepared = True
            else:
                pass
        #### isi after picture #####
        win.flip()
        pic_prepared = False
        while trial_timer.getTime()<0: # wait and prepare the next stimulus in the meantime
            if pic_prepared==False:
                if p+1<len(presentations): # there an upcoming stimulus, namely a standard or an oddball
                    if presentations[p+1]==0: # the upcoming stimulus is a standard
                        standard.draw()
                        win.callOnFlip(trial_timer.add, standard_dur)
                    else: # the upcoming stimulus is an oddball
                        oddball.draw()
                        win.callOnFlip(trial_timer.add, comparison_dur)
                else: # there is no next stimulus, only the answer screen
                    Or.draw()
                    right_option.draw()
                    left_option.draw()
                pic_prepared = True
            else:
                pass
    ######################### answer screen ##############3
    answer_screen_time = win.flip()
    trial_timer.reset()
    trial_timer.add(time_for_answer)
    # prepare next window
    win.callOnFlip(trial_timer.reset) 
    win.callOnFlip(trial_timer.add, after_answer_dur) # wait while the answer is shown
    # expect answer
    kb.clearEvents()
    while rt == 0.0 and trial_timer.getTime()<0: 
        for kb_event in keyboard.getEvents(): #check for RT
            if kb_event.key == answer_key_left or kb_event.key == answer_key_right: # or kb_event.key == missed_key
                key = kb_event.key
                rt = round(kb_event.time - answer_screen_time, 5)
                if key == answer_key_left:
                    left_option.draw()
                elif key == answer_key_right:
                    right_option.draw()
#                else: # key = missed_key
#                    pass # draw nothing
            elif kb_event.key == escape_key:
                print("aborting experiment...")
                win.saveFrameIntervals(fileName=None, clear=True)
                win.close()
                io.quit()
                core.quit()
    ############## after answer screen (shows the answer and a fixcross) #############
    win.flip()
    prepared = False
    while trial_timer.getTime()<0:
        if prepared==False:
            win.callOnFlip(trial_timer.add, after_answer_dur) # wait with fixcross before next trial begins
            # was the answer correct?
            if rt > 0.0: # was there a response?
                if comparison_dur-standard_dur==0: # if comparison_dur is equal to the standard_dur, then any answer is okay
                    correct = 1
                elif comparison_dur-standard_dur>0: # the comparison_dur was longer than the standard, then right key is correct
                    if key == answer_key_left:
                        correct = 0
                    elif key == answer_key_right:
                        correct = 1
                elif comparison_dur-standard_dur<0: # the comparison_dur was shorter than the standard, then left key is correct
                    if key == answer_key_left:
                        correct = 1
                    elif key == answer_key_right:
                        correct = 0
            # end: was answer correct
            prepared = True
        else:
            pass
    ############ wait until end of trial ##########
    win.flip()
    while trial_timer.getTime()<0:
        pass
    ##### end of trial #####
    return key, correct, rt



#### parameters ####
# general
window_size = (1000,900)   # resolution: 1920, 1080, 
# The HP Pavilion 2311x is a 58.4 cm (23 inch) monitor with a WLED (white light emitting diode) backlit screen
# Panel active area (width x height): 50.9 cm x 28.6 cm (20 inches x 11.2 inches)
fullscreen = False
background_rgb = [1,1,1]
text_rgb = [-1,-1,-1]
answer_key_right = '.' #'RIGHT'
answer_right = 'longer' #u'ארוך'  # long
answer_key_left = ',' #'LEFT'
answer_left = 'shorter' #u'קצר' # short
missed_key = ' '
escape_key = 'q'
continue_key = 'c'
# trial
pic_size = 0.6
text_height = 0.15
fixcross_height = 0.15
after_answer_dur = 0.5
standard_dur = 0.5 # duration of standard
isi_dur = 0.3 
time_for_answer = 5
wait_time = 1 # wait for this duration after the block instruction screen
stim_presentations = 9



start_exp=True
############### start demo ##################
if start_exp==True:
    #### initialize hardware #####
    # io
    io=launchHubServer(experiment_code='contextual_oddball',psychopy_monitor_name='default')
    # keyboard
    keyboard = io.devices.keyboard
    # create screen
    myWin =visual.Window(size=window_size, allowGUI=True, fullscr=fullscreen, rgb=background_rgb, winType='pyglet')
    myWin.setRecordFrameIntervals(True)
    myWin.setMouseVisible(False)
    # create standard visuals
    fixcross = visual.TextStim(win=myWin, text="+", color=text_rgb)
    fixcross.draw()
    myWin.flip()
    # show instruction wait until keyboard is pressed
    instructional_pic = visual.ImageStim(myWin, image="instruction_pic.png", size=(900,371), pos=(0,0), units='pix') # 1280x800 is lenovo screen. 1200x445 is picture
    instructional_pic.draw()
    myWin.flip()
    while not keyboard.getEvents():
        pass
    
    # trials
    trial_instruction(myWin, keyboard, 'Test Trial')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "0_o.jpg", "0_s.jpg", 7, 0.7)
    trial_instruction(myWin, keyboard, 'Trial 1')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "2_o.jpg", "2_s.jpg", 6, 0.7)
    trial_instruction(myWin, keyboard, 'Trial 2')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "1_o.jpg", "1_s.jpg", 7, 0.3)
    trial_instruction(myWin, keyboard, 'Trial 3')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "3_o.jpg", "3_s.jpg", 5, 0.5)
    trial_instruction(myWin, keyboard, 'Trial 4')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "4_o.jpg", "4_s.jpg", 8, 0.35)
    trial_instruction(myWin, keyboard, 'Trial 5')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "5_o.jpg", "5_s.jpg", 5, 0.45)
    trial_instruction(myWin, keyboard, 'Trial 6')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "8_o.jpg", "8_s.jpg", 7, 0.6)
    trial_instruction(myWin, keyboard, 'Trial 7')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "7_o.jpg", "7_s.jpg", 8, 0.55)
    trial_instruction(myWin, keyboard, 'Trial 8')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "6_o.jpg", "6_s.jpg", 6, 0.40)
    trial_instruction(myWin, keyboard, 'Trial 9')
    response, response_correct, response_rt = oddball_trial(myWin, keyboard, "9_o.jpg", "9_s.jpg", 8, 0.65)
    
    #### close everything ####
    myWin.saveFrameIntervals(fileName="frametime.log", clear=True)
    myWin.close()
    io.quit()
    core.quit()