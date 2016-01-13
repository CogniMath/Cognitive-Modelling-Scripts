#Matthia Cognitive Model Python Version


import numpy as np
import random
import math
import csv

actr_a = 1.1
actr_b = 0.015
actr_t0 = 11

num_subjects = 18 #According to the .csv file
num_sessions = 5
num_trials = 120


def plot_existing_data():
	
	with open ('#name.csv', 'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=' ', quotechar='|') #FIXME when you have the data
		for row in in data:
			print(', '.join(row))



def create_declarative_memory(chunks, encounters):

	Declarative_Memory = np.zeros(())	#FIXME check how big the DM should be

	return dm


def update_declarative_memory(dm):



def uniform_condition(a):

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

	conc_vector = np.concatenate(vec_a,vec_b,vec_c,vec_d)
	uniform_vector = np.random.shuffle(conc_vector)



def exponential_condition(a,b,c,d):

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

	conc_vector = np.concatenate(vec_a,vec_b,vec_c,vec_d)
	expo_vector = np.random.shuffle(conc_vector)

	


def anti_exponential_condition(a,b,c,d):

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

	conc_vector = np.concatenate(vec_a,vec_b,vec_c,vec_d)
	anti_expo_vector = np.random.shuffle(conc_vector)



def actr_b(encounters, current_time):




def actr_noise(s):

	n_random = random.uniform(0.0001, 0.9999)
	s*math.log((1-n_random)/n_random)

	return s

def pulse_into_time(num_pulses):

	interval_estimation = actr_t0
	global_time = actr_t0

	for i in range (1,num_pulses):
		interval_estimation = interval_estimation * actr_a + actr_noise(actr_a * actr_b * interval_estimation)
		global_time = global_time + interval_estimation

	return global_time


def time_into_pulse(time):

	interval_estimation = actr_t0
	num_pulses = 0
	time_tracker = actr_t0

	while time_tracker < time:
		interval_estimation = interval_estimation * actr_a + actr_noise(actr_a * actr_b * interval_estimation)
		time_tracker = time_tracker + interval_estimation
		num_pulses = num_pulses + 1

	return num_pulses


def run_model(num_subjects, num_sessions):

	for i in range(1,num_subjects):

		subject_clock = 0
		subject_DM = create_declarative_memory() #FIXME add number of chunks and encounters 

		for j in range(1, num_sessions):

			if(j=1 or j=3 or j=5):

				uniform_foreperiod = uniform_condition(30)

				for time in uniform_foreperiod:
					subject_clock = subject_clock + random.uniform(250,850) + time
					pulse_estimation = time_into_pulse(subject_clock)
					#FIXME add the pulse_estimation and time to the DM
				#run the uniform condition
			
			elif(j=2):

				exponential_foreperiod = exponential_condition(64,32,16,8)
				
				for time in exponential_foreperiod:
					subject_clock = subject_clock + random.uniform(250,850) + time
					pulse_estimation = time_into_pulse(subject_clock)
				#run the exponential condition
			
			elif(j=4):
				
				antiexponential_foreperiod = anti_exponential_condition(8,16,32,64)
				
				for time in antiexponential_foreperiod:
					subject_clock = subject_clock + random.uniform(250,850) + time
					pulse_estimation = time_into_pulse(subject_clock)


				#run the antiexponential condition 


if __name__ == "__main__":





"""FIXME the results aren't perfectly matching with the R function
But the code still seems correct
"""