"""
Cognitive Modelling Course: Final Assignment
Matthia Sabatelli: S2847485
MSc. Artificial Intelligence

It's possible to run the code by launching python CognitiveModelling_S2847485.py from terminal, the python version that is required is 2.7.
The code shows what is happening while the experiment is running by giving information about the Block and about the participant,
In fact it shows which stimulous is presented and also which one the participant was expecting according to the blending process (which might be unprecise).
At the end some statistics about the experiment are shown.

It's possible to adjust the number of participants but for unknown reasons the code might be a little bit unstable and sometimes it
crashes while increasing this variable, however if this happens just relaunch the program it's very rare that it happens 2 times in a row.
The results of a 18 participant simulation are presented in the paper.
"""

import random       #Libraries used in the code 
import math
import numpy as np
import csv

actr_a = 1.11       #Definition of various parameters used in order to use the different ActR functions
actr_b = 0.015
actr_t0 = 11
actr_decay_rate = 0.5
actr_weighted_s = 1


class participant():  #Initialization of the class participant in order to keep track of every participant's data of the experiment

    def __init__(self, block, foreperiod, rt):

        self.block = block
        self.foreperiod = foreperiod
        self.rt = rt


def create_the_dm(pulses_dict, pulse, time):    #Creation of the Declarative Memory for every participant, the DM is represented by a dictionary
                                                #that has 'pulse' and 'time' as keys since these are the variables that need to be saved 

    if pulse in pulses_dict.keys():
        tmp = pulses_dict[pulse]
        tmp.append(time)
        pulses_dict[pulse] = tmp
    else:
        pulses_dict[pulse] = [time]


def comp_abs_diff(new_dict_with_diff, dictionary_of_pulses):  
    
    for k in dictionary_of_pulses.keys():
        tmp_list = dictionary_of_pulses[k]
        for time in range(len(tmp_list)):
            tmp_list[time] = tmp_list[time] + subject_clock
        new_dict_with_diff[k] = tmp_list


def calcu_activations(pulses_diff_dictionary, conv_act_pulses_dicionary):   
    
    i = 0.0
    
    for k in pulses_diff_dictionary.keys():
        tmp_list = pulses_diff_dictionary[k]
        for x in range(len(tmp_list)):
            if tmp_list[x] == 0:
                tmp_list[x] = 1
            tmp_list[x] = math.log(len(tmp_list) / (1 - 0.5)) - 0.5 * math.log(abs(tmp_list[x]))
        conv_act_pulses_dicionary[k] = tmp_list


def small_act(conv_act_pulses_dicionary, small_act_dict):   #Function that calculates the total activation for every single pulse by summing over all the single activations
    
    small_activation = 0
    
    for k in conv_act_pulses_dicionary.keys():
        tmp_list = conv_act_pulses_dicionary[k]
        small_act_dict[k] = sum(tmp_list)


def total_act(conv_act_pulses_dicionary):   #Function that calculates the total sum of the activations, by summing over the previous activation sum 
    
    total_activation = 0
    
    for k in conv_act_pulses_dicionary.keys():
        tmp_list = conv_act_pulses_dicionary[k]
        for x in tmp_list:
            total_activation += x
    return total_activation


def total_and_small_to_blend(total_activation, small_act_dict): #Function that is the final step in order to get the blended value according to how the blended value is computed
    
    tmp_val = 0.0
    total = 0.0
    
    for k in small_act_dict.keys():
        tmp_val = k * (small_act_dict[k] / total_activation)
        total += tmp_val

    return total


def calculate_reaction_time(b, basic_reaction_time,time, expected_time):   #Function that estimates the reaction time for every participant and according to how they are 
                                                                           #performing, if they're yet ready to respond to the stimulous or not, it adds some penalties to the RT
                                                                           #Different RT penalties according to different blocks are given + some random ms are added 

    print "****************** EXPERIMENT IS RUNNING ********************"
    print "We are in Block: ", b
    print "This is the time presentation: ", time
    print "This is the time that I expect ", expected_time
    print "-------------------------------------------------------------"
    
    
    if b == 1 or b == 3 or b == 5:
        if time-expected_time <0:
            basic_reaction_time += 35 + random.randint(1,11) #Penalty added 
    
    if b == 2:
        if time-expected_time <0:
            basic_reaction_time += 65 + random.randint(1,11) #Penalty added
    
    if b == 4:
        if time-expected_time <0:
            basic_reaction_time += 100 + random.randint(1,11) #Penalty added

    return basic_reaction_time


def repeat():   #Main function that governs all the previous ones and according to how the blended process works returns
                #an interval estimation value that corresponds to when the participant thinks the next stimulous will appear

    comp_abs_diff(pulses_diff_dictionary, pulses_dictionary)
    calcu_activations(pulses_diff_dictionary, conv_act_pulses_dicionary)

    total_activation = total_act(conv_act_pulses_dicionary)

    small_act(conv_act_pulses_dicionary, small_act_dict)

    blending_val = total_and_small_to_blend(total_activation, small_act_dict)

    interval_estimation = pulse_into_time(blending_val) #In order to get a value in ms the pulse needs to be converted into time
    
    return interval_estimation


def uniform_condition(a):   #Function that creates a vector of stimuli for Block 1,3,5
    
    conc_vector = []

    vec_a = []
    vec_b = []
    vec_c = []
    vec_d = []

    for i in range(a):
        vec_a.append(400)
        vec_b.append(800)
        vec_c.append(1200)
        vec_d.append(1600)

    conc_vector = vec_a + vec_b + vec_c + vec_d
    uniform_vector = sorted(conc_vector, key=lambda k: random.random())

    return uniform_vector


def exponential_condition(a, b, c, d): #Function that creates a vector of stimuli for Block 2
    
    conc_vector = []

    vec_a = []
    vec_b = []
    vec_c = []
    vec_d = []

    for i in range(a):
        vec_a.append(400)

    for j in range(b):
        vec_b.append(800)

    for k in range(c):
        vec_c.append(1200)

    for m in range(d):
        vec_d.append(1600)

    conc_vector = vec_a + vec_b + vec_c + vec_d
    expo_vector = sorted(conc_vector, key=lambda k: random.random())

    return expo_vector


def anti_exponential_condition(a, b, c, d): #Function that creates a vector of stimuli for Block 4
    
    conc_vector = []

    vec_a = []
    vec_b = []
    vec_c = []
    vec_d = []

    for i in range(a):
        vec_a.append(400)

    for j in range(b):
        vec_b.append(800)

    for k in range(c):
        vec_c.append(1200)

    for m in range(d):
        vec_d.append(1600)

    conc_vector = vec_a + vec_b + vec_c + vec_d
    anti_expo_vector = sorted(conc_vector, key=lambda k: random.random())

    return anti_expo_vector


def time_into_pulse(time):  #Function that converts time intervals into pulses

    interval_estimation = actr_t0
    num_pulses = 0
    time_tracker = actr_t0

    while time_tracker < time:
        interval_estimation = interval_estimation * actr_a + actr_noise(actr_a * actr_b * interval_estimation)
        time_tracker = time_tracker + interval_estimation
        num_pulses = num_pulses + 1

    return num_pulses


def actr_noise(s):  #Noise function that produces some randomness while running the experiment

    n_random = random.uniform(0.0001, 0.9999)
    noise = s * math.log((1 - n_random) / n_random)
    return noise


def pulse_into_time(num_pulses):  #Function that converts a pulse into time

    interval_estimation = actr_t0
    global_time = actr_t0

    for i in range(1, int(num_pulses)):
        interval_estimation = interval_estimation * actr_a + actr_noise(actr_a * actr_b * interval_estimation)
        global_time = global_time + interval_estimation

    return global_time


reaction_time = 0.0     #Initialization of the variables used in the experiment 
total_activation = 0.0
blending_val = 0.0
subject_clock = 0
pulses_dictionary = {}
pulses_diff_dictionary = {}
conv_act_pulses_dicionary = {}
small_act_dict = {}

num_subjects = 1        
num_sessions = 6


data_set_dictionary = {'Block': [], 'foraperiod': [], 'RT': []} 
participants = []

for i in xrange(0,num_subjects):    #Main Experiment Simulation function

    subject_clock = 0
    
    for i in range(1, num_sessions):

        if (i == 1 or i == 3 or i == 5):
            times_vector = uniform_condition(10)
        elif (i == 2):
            times_vector = exponential_condition(64, 32, 16, 8)
        elif (i == 4):
            times_vector = anti_exponential_condition(8, 16, 32, 64)

        for time in times_vector:  
            subject_clock += time
            create_the_dm(pulses_dictionary, time_into_pulse(time), subject_clock)
            subject_clock += 50 #50 milliseconds are needed to update the dm
            expectation_time = repeat()
            
            subject_clock += expectation_time 
            subject_clock += 150 #150 milliseconds pass between one foreperiod and another one

            rt = calculate_reaction_time(i, 300+random.randint(1,11), time, expectation_time) #300 milliseconds is the base reaction time + random ms noise

            data_set_dictionary['Block'].append(i)
            data_set_dictionary['foraperiod'].append(time)
            data_set_dictionary['RT'].append(rt)

    participants.append(participant(data_set_dictionary['Block'], data_set_dictionary['foraperiod'],data_set_dictionary['RT']))
    data_set_dictionary = {'Block': [], 'foraperiod': [], 'RT': []}

list400 = []
list800 = []
list1200 = []
list1600 = []


with open('DataSimulation.csv', 'wb') as csvfile:   #Everything is saved to a .csv file in order to plot the results with R after a short preprocessing 
    
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    spamwriter.writerow(['Block', 'ForePeriod', 'ResponseTime'])

    for p in participants:

        block = p.block    
        foreperiod=p.foreperiod
        RT = p.rt

        for i in range(1,6):

            for f in range(len(foreperiod)):

                if block[f] == i: 

                    if foreperiod[f] == 400:
                        list400.append(RT[f])
                    elif foreperiod[f] == 800:
                        list800.append(RT[f])
                    elif foreperiod[f] == 1200:
                        list1200.append(RT[f])
                    elif foreperiod[f] == 1600:
                        list1600.append(RT[f])

            
            print "-------------------------------------------------------------"
    
            print "Stats Block: ", i
            print "Average Response Time for Block 400:",np.mean(list400)
            print "Average Response Time for Block 800:",np.mean(list800)
            print "Average Response Time for Block 1200:",np.mean(list1200)
            print "Average Response Time for Block 1600:",np.mean(list1600)
            
            spamwriter.writerow([i, 400, np.mean(list400)])
            spamwriter.writerow([i, 800, np.mean(list800)])
            spamwriter.writerow([i, 1200, np.mean(list1200)])
            spamwriter.writerow([i, 1600, np.mean(list1600)])
            
        list400 = []
        list800 = []
        list1200 = []
        list1600 = []
