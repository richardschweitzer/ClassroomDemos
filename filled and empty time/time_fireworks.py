# filled vs empty time

# fireworks! 
# by richard 11/2014
from psychopy import visual, core, sound, event
import numpy as np
import pylab
from psychopy.iohub import launchHubServer, EventConstants  # needs: msgpack , psutil, xlib, 

########################################## FIREWORKS procedure #################################################
def fireworks_task(win, win_size, visual, core, trial_duration):
    ############ procedures ###############
    def initiate_start(pos, start_positions): # input are numbers from 1 to 5 and an array of 5 positions
        x_pos = start_positions[pos-1]
        y_pos = -1
        return x_pos, y_pos
    
    # a function to define the firework. input: the mean speed and variation, the colours, the signed/unsigned array
    def initiate_fireworks(np, mean_vertical_speed, var_vertical_speed, mean_horizontal_speed, var_horizontal_speed, def_colours, signed):
        np.random.shuffle(signed)
        # here we produce the speed and the color of the firework
        speed_y = mean_vertical_speed + signed[0] * np.random.rand() / var_vertical_speed
        speed_x = mean_horizontal_speed + signed[1] * np.random.rand() / var_horizontal_speed
        dot_rgb255_col = def_colours[np.random.randint(0,len(def_colours))] 
        return speed_x, speed_y, dot_rgb255_col
    
    # a function 
    def update_fireworks(x, y, speed_x, speed_y, slowing, gravity):
        # compute position of the dot on this frame
        slowing += gravity 
        y += speed_y / float(slowing) 
        x += speed_x / float(slowing) 
        return x, y, slowing
    
    def initiate_particles(np, pos_explosion, num_particles, particle_speed_factor, signed): # this function creates position, direction and individual speed of particles
        pos_particles = np.reshape(np.tile(pos_explosion,num_particles), [num_particles,2])
        # each particle gets a speed and slowing assigned
        speed_particles = []
        ind_slowing_particles = []
        for n in range(num_particles): # here we randomize values for each particle
            np.random.shuffle(signed)
            # the speed
            v = [signed[0] * particle_speed_factor * np.random.rand(), signed[1] * particle_speed_factor * np.random.rand()]
            speed_particles.append(v)
            # the slowing independently from the speed
            s = [signed[2]*np.random.rand(), signed[3]*np.random.rand()]
            ind_slowing_particles.append(s)
        return pos_particles, speed_particles, ind_slowing_particles
    
    def update_particles(np, pos_particles, speed_particles, slowing_p, num_particles, gravity, particle_gravity_factor):
        slowing_p += gravity
        slowing_particles = np.reshape(np.tile([slowing_p,slowing_p], num_particles), [num_particles,2]) # the slowing for all particles
        gravity_particles = np.reshape(np.tile([0, -gravity*particle_gravity_factor], num_particles), [num_particles,2]) # the gravity effect on all particles
        speed_particles = speed_particles / slowing_particles + gravity_particles
        pos_particles += speed_particles
        return pos_particles, speed_particles, slowing_p
    
    ############# START EXPERIMENT HERE #############
    ### first, prepare parameters and so on ###
    trial_timer = core.MonotonicClock()
    start_trial_time = trial_timer.getTime()
    prepare_timer = core.CountdownTimer(0.1) # give the computer 100ms timer to prepare the stimuli. this should suffice
    i = 0
    nr_explosions = 0
    while prepare_timer.getTime()>0:
        i+=1
        if i==1: 
            import numpy as np
            ## parameters ##
            def_colours = [[255,255,255], #White
                      [255,64,0],    #Red
                      [255,128,0],   #Orange
                      [255,204,0],   #Yellow-orange
                      [192,255,0],   #Yellow-green
                      [64,255,0],    #Bright green
                      [0,255,128],   #Sea green
                      [0,255,255],   #Aqua
                      [0,128,255],   #Turquoise
                      [0,48,255],    #Bright blue
                      [128,0,255],   #Indigo
                      [255,0,255]]   #Magenta
            # for fireworks
            mean_vertical_speed = 0.04 # mean value of relative vertical position change per frame
            var_vertical_speed = 100  # this value represents how strong the random effect on speed should be. BUT: higher values mean less random effect 
            mean_horizontal_speed = 0 # mean value of relative horizontal position change per frame (constant wind from the sides)
            var_horizontal_speed = 100
            firework_decel = 1
            firework_size = (0.05, 0.05)
            frames_firework = 75 # how many frames of flight time
            start_positions_firework = [-0.5,-0.25,0,0.25,0.5]
            np.random.shuffle(start_positions_firework)
            # for particles
            particle_speed_factor = [0.02, 0.022, 0.024, 0.026, 0.028]
            particle_decel = [0.7, 0.75, 0.8, 0.85, 0.90]
            particle_gravity_factor = 0.04
            num_particles = [30, 35, 40, 45, 50]
            particle_size = (0.03, 0.03)
            frames_particles = 25 # for how many frames are particles shown?
            np.random.shuffle(particle_speed_factor)
            np.random.shuffle(particle_decel)
            np.random.shuffle(num_particles)
            # for both
            signed = [-1,1,-1,1]
            gravity = 0.05  # how fast the velocity of the ball is reduced
            resp_time_window = 0.0005 # this is 0.5ms but it doesn't matter since while the frame is loading the participant can already press a button
            position_of_timer = (-0.9,-0.9)
            position_of_press_count = (0.9, -0.9)
            ## initialise important parameters for trial ##
            active_1 = False
            active_2 = False
            active_3 = False
            active_4 = False
            active_5 = False
            firework_timer = core.CountdownTimer(trial_duration) # create a timer for the participant to see how long he/she still has to last
            frameN = 0
            # create the dots and the element arrays
            fixcross = visual.TextStim(win, text="+")
            dot_1 = visual.GratingStim(win, tex=None, mask="gauss", size=firework_size, colorSpace='rgb255')
            dots_1 = visual.ElementArrayStim(win, elementTex=None, elementMask='gauss', colorSpace='rgb255', nElements=num_particles[1-1], sizes=particle_size)
            dot_2 = visual.GratingStim(win, tex=None, mask="gauss", size=firework_size, colorSpace='rgb255')
            dots_2 = visual.ElementArrayStim(win, elementTex=None, elementMask='gauss', colorSpace='rgb255', nElements=num_particles[2-1], sizes=particle_size)
            dot_3 = visual.GratingStim(win, tex=None, mask="gauss", size=firework_size, colorSpace='rgb255')
            dots_3 = visual.ElementArrayStim(win, elementTex=None, elementMask='gauss', colorSpace='rgb255', nElements=num_particles[3-1], sizes=particle_size)
            dot_4 = visual.GratingStim(win, tex=None, mask="gauss", size=firework_size, colorSpace='rgb255')
            dots_4 = visual.ElementArrayStim(win, elementTex=None, elementMask='gauss', colorSpace='rgb255', nElements=num_particles[4-1], sizes=particle_size)
            dot_5 = visual.GratingStim(win, tex=None, mask="gauss", size=firework_size, colorSpace='rgb255')
            dots_5 = visual.ElementArrayStim(win, elementTex=None, elementMask='gauss', colorSpace='rgb255', nElements=num_particles[5-1], sizes=particle_size)
        else:
            pass
    ### start loop over frames here ###
    time_lag = 0.3 # time lag between activations
    while firework_timer.getTime()>0:
        i = 0
        if active_1==False:
            active_time = firework_timer.getTime()
            active_1 = True
            frame_start_1 = frameN
        if active_2==False and active_time-firework_timer.getTime()>time_lag:
            active_time = firework_timer.getTime()
            active_2 = True
            frame_start_2 = frameN
        if active_3==False and active_time-firework_timer.getTime()>time_lag:
            active_time = firework_timer.getTime()
            active_3 = True
            frame_start_3 = frameN
        if active_4==False and active_time-firework_timer.getTime()>time_lag:
            active_time = firework_timer.getTime()
            active_4 = True
            frame_start_4 = frameN
        if active_5==False and active_time-firework_timer.getTime()>time_lag:
            active_time = firework_timer.getTime()
            active_5 = True
            frame_start_5 = frameN
                
        ## here comes firework nr. 1
        if active_1==True:
            if frameN==frame_start_1:
                # start position of the firework
                x_1, y_1 = initiate_start(1, start_positions_firework)
                # randomize the launching speed (speed_y), direction at launch (speed_x) and color of firework (dot_rgb255_col)
                speed_x_1, speed_y_1, dot_rgb255_col_1 = initiate_fireworks(np, mean_vertical_speed, var_vertical_speed, mean_horizontal_speed, var_horizontal_speed, def_colours, signed)
                # set dot colors and position
                dot_1.setColor(dot_rgb255_col_1)
                dot_1.pos = (x_1, y_1)
                dot_1.draw()
                slowing_1 = firework_decel
            if frameN > frame_start_1 and frameN <= frame_start_1+frames_firework: # here the fireworks are shot
                # compute position of the dot on this frame
                x_1, y_1, slowing_1 = update_fireworks(x_1, y_1, speed_x_1, speed_y_1, slowing_1, gravity)
                # show dot
                dot_1.pos = [x_1,y_1]
                dot_1.draw() 
            if frameN==frame_start_1+frames_firework: 
                # starting position of particles is where the firework was shown last
                pos_particles_1, speed_particles_1, ind_slowing_particles_1 = initiate_particles(np, dot_1.pos, num_particles[1-1], particle_speed_factor[1-1], signed)
                # set elementArrayStim colors and positions, since it is way faster
                dots_1.setColors(dot_rgb255_col_1)
                dots_1.setXYs(pos_particles_1)
                slowing_p_1 = particle_decel[1-1]
            if frameN == frame_start_1+frames_firework+1: # draw the particles into buffer
                dots_1.draw()
            if frameN > frame_start_1+frames_firework+1 and frameN <= frame_start_1+frames_firework+frames_particles: # here come the particles
                pos_particles_1, speed_particles_1, slowing_p_1 = update_particles(np, pos_particles_1, speed_particles_1, slowing_p_1, num_particles[1-1], gravity, particle_gravity_factor)
                dots_1.setXYs(pos_particles_1)
                dots_1.draw()
            if frameN == frame_start_1+frames_firework+frames_particles: 
                active_1 = False 
                nr_explosions += 1
            ## firework nr. 1 has finished
        #
        ## here comes firework nr. 2
        if active_2==True:
            if frameN==frame_start_2:
                # start position of the firework
                x_2, y_2 = initiate_start(2, start_positions_firework)
                # randomize the launching speed (speed_y), direction at launch (speed_x) and color of firework (dot_rgb255_col)
                speed_x_2, speed_y_2, dot_rgb255_col_2 = initiate_fireworks(np, mean_vertical_speed, var_vertical_speed, mean_horizontal_speed, var_horizontal_speed, def_colours, signed)
                # create dot
                dot_2.setColor(dot_rgb255_col_2)
                dot_2.pos = (x_2, y_2)
                dot_2.draw()
                slowing_2 = firework_decel
            if frameN > frame_start_2 and frameN <= frame_start_2+frames_firework: # here the fireworks are shot
                # compute position of the dot on this frame
                x_2, y_2, slowing_2 = update_fireworks(x_2, y_2, speed_x_2, speed_y_2, slowing_2, gravity)
                # show dot
                dot_2.pos = [x_2,y_2]
                dot_2.draw() 
            if frameN==frame_start_2+frames_firework: 
                # starting position of particles is where the firework was shown last
                pos_particles_2, speed_particles_2, ind_slowing_particles_2 = initiate_particles(np, dot_2.pos, num_particles[2-1], particle_speed_factor[2-1], signed)
                # set elementArrayStim colors and positions, since it is way faster
                dots_2.setColors(dot_rgb255_col_2)
                dots_2.setXYs(pos_particles_2)
                slowing_p_2 = particle_decel[2-1]
            if frameN == frame_start_2+frames_firework+1: # draw the particles into buffer
                dots_2.draw()
            if frameN > frame_start_2+frames_firework+1 and frameN <= frame_start_2+frames_firework+frames_particles: # here come the particles
                pos_particles_2, speed_particles_2, slowing_p_2 = update_particles(np, pos_particles_2, speed_particles_2, slowing_p_2, num_particles[2-1], gravity, particle_gravity_factor)
                dots_2.setXYs(pos_particles_2)
                dots_2.draw()
            if frameN == frame_start_2+frames_firework+frames_particles: 
                active_2 = False
                nr_explosions += 1
            ## firework nr. 2 has finished
        #
        ## here comes firework nr. 3
        if active_3==True:
            if frameN==frame_start_3:
                # start position of the firework
                x_3, y_3 = initiate_start(3, start_positions_firework)
                # randomize the launching speed (speed_y), direction at launch (speed_x) and color of firework (dot_rgb255_col)
                speed_x_3, speed_y_3, dot_rgb255_col_3 = initiate_fireworks(np, mean_vertical_speed, var_vertical_speed, mean_horizontal_speed, var_horizontal_speed, def_colours, signed)
                # create dot
                dot_3.setColor(dot_rgb255_col_3)
                dot_3.pos = (x_3, y_3)
                dot_3.draw()
                slowing_3 = firework_decel
            if frameN > frame_start_3 and frameN <= frame_start_3+frames_firework: # here the fireworks are shot
                # compute position of the dot on this frame
                x_3, y_3, slowing_3 = update_fireworks(x_3, y_3, speed_x_3, speed_y_3, slowing_3, gravity)
                # show dot
                dot_3.pos = [x_3,y_3]
                dot_3.draw() 
            if frameN==frame_start_3+frames_firework: 
                # starting position of particles is where the firework was shown last
                pos_particles_3, speed_particles_3, ind_slowing_particles_3 = initiate_particles(np, dot_3.pos, num_particles[3-1], particle_speed_factor[3-1], signed)
                # set elementArrayStim colors and positions, since it is way faster
                dots_3.setColors(dot_rgb255_col_3)
                dots_3.setXYs(pos_particles_3)
                slowing_p_3 = particle_decel[3-1]
            if frameN == frame_start_3+frames_firework+1: # draw the particles into buffer
                dots_3.draw()
            if frameN > frame_start_3+frames_firework+1 and frameN <= frame_start_3+frames_firework+frames_particles: # here come the particles
                pos_particles_3, speed_particles_3, slowing_p_3 = update_particles(np, pos_particles_3, speed_particles_3, slowing_p_3, num_particles[3-1], gravity, particle_gravity_factor)
                dots_3.setXYs(pos_particles_3)
                dots_3.draw()
            if frameN == frame_start_3+frames_firework+frames_particles: 
                active_3 = False
                nr_explosions += 1
            ## firework nr. 3 has finished
        #
        ## here comes firework nr. 4
        if active_4==True:
            if frameN==frame_start_4:
                # start position of the firework
                x_4, y_4 = initiate_start(4, start_positions_firework)
                # randomize the launching speed (speed_y), direction at launch (speed_x) and color of firework (dot_rgb255_col)
                speed_x_4, speed_y_4, dot_rgb255_col_4 = initiate_fireworks(np, mean_vertical_speed, var_vertical_speed, mean_horizontal_speed, var_horizontal_speed, def_colours, signed)
                # create dot
                dot_4.setColor(dot_rgb255_col_4)
                dot_4.pos = (x_4, y_4)
                dot_4.draw()
                slowing_4 = firework_decel
            if frameN > frame_start_4 and frameN <= frame_start_4+frames_firework: # here the fireworks are shot
                # compute position of the dot on this frame
                x_4, y_4, slowing_4 = update_fireworks(x_4, y_4, speed_x_4, speed_y_4, slowing_4, gravity)
                # show dot
                dot_4.pos = [x_4,y_4]
                dot_4.draw() 
            if frameN==frame_start_4+frames_firework: 
                # starting position of particles is where the firework was shown last
                pos_particles_4, speed_particles_4, ind_slowing_particles_4 = initiate_particles(np, dot_4.pos, num_particles[4-1], particle_speed_factor[4-1], signed)
                # set elementArrayStim colors and positions, since it is way faster
                dots_4.setColors(dot_rgb255_col_4)
                dots_4.setXYs(pos_particles_4)
                slowing_p_4 = particle_decel[4-1]
            if frameN == frame_start_4+frames_firework+1: # draw the particles into buffer
                dots_4.draw()
            if frameN > frame_start_4+frames_firework+1 and frameN <= frame_start_4+frames_firework+frames_particles: # here come the particles
                pos_particles_4, speed_particles_4, slowing_p_4 = update_particles(np, pos_particles_4, speed_particles_4, slowing_p_4, num_particles[4-1], gravity, particle_gravity_factor)
                dots_4.setXYs(pos_particles_4)
                dots_4.draw()
            if frameN == frame_start_4+frames_firework+frames_particles: 
                active_4 = False
                nr_explosions += 1
            ## firework nr. 4 has finished
        ## here comes firework nr. 5
        if active_5==True:
            if frameN==frame_start_5:
                # start position of the firework
                x_5, y_5 = initiate_start(5, start_positions_firework)
                # randomize the launching speed (speed_y), direction at launch (speed_x) and color of firework (dot_rgb255_col)
                speed_x_5, speed_y_5, dot_rgb255_col_5 = initiate_fireworks(np, mean_vertical_speed, var_vertical_speed, mean_horizontal_speed, var_horizontal_speed, def_colours, signed)
                # set dot colors and position
                dot_5.setColor(dot_rgb255_col_5)
                dot_5.pos = (x_5, y_5)
                dot_5.draw()
                slowing_5 = firework_decel
            if frameN > frame_start_5 and frameN <= frame_start_5+frames_firework: # here the fireworks are shot
                # compute position of the dot on this frame
                x_5, y_5, slowing_5 = update_fireworks(x_5, y_5, speed_x_5, speed_y_5, slowing_5, gravity)
                # show dot
                dot_5.pos = [x_5,y_5]
                dot_5.draw() 
            if frameN==frame_start_5+frames_firework: 
                # starting position of particles is where the firework was shown last
                pos_particles_5, speed_particles_5, ind_slowing_particles_5 = initiate_particles(np, dot_5.pos, num_particles[5-1], particle_speed_factor[5-1], signed)
                # set elementArrayStim colors and positions, since it is way faster
                dots_5.setColors(dot_rgb255_col_5)
                dots_5.setXYs(pos_particles_5)
                slowing_p_5 = particle_decel[5-1]
            if frameN == frame_start_5+frames_firework+1: # draw the particles into buffer
                dots_5.draw()
            if frameN > frame_start_5+frames_firework+1 and frameN <= frame_start_5+frames_firework+frames_particles: # here come the particles
                pos_particles_5, speed_particles_5, slowing_p_5 = update_particles(np, pos_particles_5, speed_particles_5, slowing_p_5, num_particles[5-1], gravity, particle_gravity_factor)
                dots_5.setXYs(pos_particles_5)
                dots_5.draw()
            if frameN == frame_start_5+frames_firework+frames_particles: 
                active_5 = False 
                nr_explosions += 1
            ## firework nr. 5 has finished
        fixcross.draw()
        win.flip()
        frameN +=1
    return frameN, trial_timer.getTime()-start_trial_time, nr_explosions


def play_sound(sound, dur):
    sound_time_blocking = core.CountdownTimer(dur)
    sound.play()
    while sound_time_blocking.getTime()>0:
        pass

def wait_time(dur):
    wait_timer = core.CountdownTimer(dur)
    while wait_timer.getTime()>0:
        pass
    return wait_timer.getTime()


################### here starts the exp #####################
window_size = (1024,768)
fullscreen = False

# create screen
myWin =visual.Window(size=window_size, fullscr=fullscreen, rgb=[-1,-1,-1], winType='pyglet')
myWin.setRecordFrameIntervals(True)
myWin.setMouseVisible(False)


# make time intervals
interval_duration = 10
marker_dur = 0.400
marker_hz = 500
marker_sound = sound.Sound(marker_hz, marker_dur)
marker_stimulus = visual.GratingStim(myWin, tex=None, mask="gauss", size=0.5)
marker_stimulus.setPos([0,-0.3])

## start empty interval
fixcross = visual.TextStim(win=myWin, text="+")
trial_announce = visual.TextStim(win=myWin, text='Interval ' + str(1) + ' - Ready?', pos=(0,0))
trial_announce.draw()
myWin.flip() # show interval 1 screen
# wait for keys
event.clearEvents() 
event.waitKeys()
fixcross.draw()
marker_stimulus.draw()
myWin.flip() # first marker stimulus
# play sequence
play_sound(marker_sound, marker_dur)
core.wait(marker_dur)
fixcross.draw()
myWin.flip()
empty_time = wait_time(interval_duration)
fixcross.draw()
marker_stimulus.draw()
myWin.flip() # second marker stimulus
play_sound(marker_sound, marker_dur)
core.wait(marker_dur)
fixcross.draw()
myWin.flip()

## start firework interval
trial_announce = visual.TextStim(win=myWin, text='Interval ' + str(2) + ' - Ready?', pos=(0,0))
trial_announce.draw()
myWin.flip() # show interval 1 screen
# wait for keys
event.clearEvents() 
event.waitKeys()
fixcross.draw()
marker_stimulus.draw()
myWin.flip() # first marker stimulus
# play sequence
play_sound(marker_sound, marker_dur)
core.wait(marker_dur)
frames_count, firework_time, nr_explosions = fireworks_task(myWin, window_size, visual, core, interval_duration)
#print(nr_explosions)
#print(firework_time)
fixcross.draw()
marker_stimulus.draw()
myWin.flip()
play_sound(marker_sound, marker_dur)
core.wait(marker_dur)
fixcross.draw()
myWin.flip()


## which interval was longer
core.wait(1)
#question = visual.TextStim(win=myWin, text='Which interval felt longer to you?', pos=(0,0))
#question.draw()
myWin.flip()
# wait for key to end
event.clearEvents() 
event.waitKeys()

myWin.saveFrameIntervals(fileName=None, clear=True)
myWin.close()
core.quit()
print('fireworks took: ' + str(firework_time))
