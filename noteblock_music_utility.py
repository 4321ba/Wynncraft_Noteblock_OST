#!/usr/bin/python3

from csv import reader as csvreader
from sys import exit as sysexit
from os import listdir as oslistdir

def get_input_files(files):
    if len(files) == 0:
        return [i for i in oslistdir() if i[-4:] == ".csv"]
    else:
        return files

def import_csv_file(file):
    print("Importing file", file)
    with open(file, newline='') as csv_file:
        csv_data = csvreader(csv_file, delimiter=',', quotechar='|')
        return [row for row in csv_data]

def create_csv_file(data, file):
    new_data = [','.join(i) for i in data]
    csv_string = '\n'.join(new_data) + '\n'
    with open(file, "w") as output_csv:
        output_csv.write(csv_string)

def get_metronome_info(data, metronome, return_timings): #metronome is the value defined by the user, -1 if nothing is defined
    
    if metronome != -1 and not return_timings: #metronome is provided by the user and the script doesn't want timing info
        print("Metronome value is", metronome)
        return metronome
    
    #get timing info from data
    timings = {}
    for i in data:
        if not int(i[1]) in timings.keys():
            timings[int(i[1])] = 0
        timings[int(i[1])] += 1
    timings = {key: value for key, value in sorted(timings.items(), key = lambda item: -item[1])}
    
    #determine metronome value (the smallest timing used, without the lag)
    if metronome == -1:
        
        possible_metronome_ticks = list(timings.keys())
        if 0 in possible_metronome_ticks:
            possible_metronome_ticks.remove(0)
        
        greatest_common_divisor = 0
        for i in range(1, min(possible_metronome_ticks) + 1):
            if all(j % i == 0 for j in possible_metronome_ticks):
                greatest_common_divisor = i
        
        if greatest_common_divisor > 2: #this means that it's probably lag-free so we should use the GCD as metronome value
            metronome = greatest_common_divisor
        else:
            possible_metronome_ticks = possible_metronome_ticks[0:2] #get 2 most frequent delays, those are the best bet if it's laggy
            if len(possible_metronome_ticks) == 1:
                metronome = possible_metronome_ticks[0]
            elif (possible_metronome_ticks[0] / possible_metronome_ticks[1]).is_integer(): #one is the multiplicate of the other
                metronome = possible_metronome_ticks[1]
            elif (possible_metronome_ticks[1] / possible_metronome_ticks[0]).is_integer():
                metronome = possible_metronome_ticks[0]
            elif 1 <= abs(possible_metronome_ticks[0] - possible_metronome_ticks[1]) <= 2: #they're the same just one is with lag (1 difference in 1.15, 2 in 1.12)
                metronome = possible_metronome_ticks[0] #hopefully the real value appears more times than the laggy one
            else:
                sysexit("Couldn't find metronome value in " + str(possible_metronome_ticks) + " from " + str(timings))
        
        #if it seems to be 12 or 8, it should be in reality 6 or 4 most probably
        if metronome == 8 or metronome == 12:
            print("Identified a metronome value of", metronome, "but we think it should be", metronome // 2, "instead")
            metronome = metronome // 2

    print("Metronome value is", metronome)
    if return_timings:
        return metronome, timings
    return metronome
