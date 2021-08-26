#!/usr/bin/python3

import math
import os
import py_midicsv
import argparse
import noteblock_music_utility

def parse_arguments():
    parser = argparse.ArgumentParser(description="convert specific .csv files to .mid files")
    parser.add_argument("input_files", nargs="*", default = [], help="csv files to convert, leave blank for all from current directory")
    parser.add_argument("-v", "--visual_percussion", action='store_true', dest="use_visual_percussion", help="uses different pitches for percussion to look good in MIDI visualizer if set, but those pitches map to different instuments and sound bad")
    parser.add_argument("-e", "--melodic_percussion", action='store_true', dest="use_melodic_percussion", help="maps percussion instruments to random drums to preserve pitch (snare: program 114, hat: program 119, basedrum: program 116)")
    parser.add_argument("-k", "--keep_newcsv", action='store_true', dest="keep_newcsv", help="keep the generated temporary file *.newcsv")
    parser.add_argument("-m", "--metronome", type=int, default = -1, help="the smallest possible miditick difference between notes, e.g. 4, can be determined automatically")
    parser.add_argument("-f", "--speed_fine_tune", type=float, default = 1, help="my solution to obscure tempo: metronome value must be integer, but if in theory it is 10/3 e.g. (meaning 40/(10/3)=12 tps in NBS) and in reality it is 3, you should set this to 3/(10/3) = 0.9 meaning the speed will be multiplied by 0.9 and it will be slower then expected")
    parser.add_argument("-l", "--note_length", type=float, default = -1, help="the number of ticks (1/40 s) for the notes to turn off, if <0 then multiplies the metronome value, default is -1, so it's the same as the metronome value")
    parser.add_argument("-s", "--can_same_note_play_twice", action='store_true', help="allows more of the same note to play at the same time, so it doesn't shut down those notes earlier than note_length says so")
    return vars(parser.parse_args())

def convert_and_add_off(data, use_visual_percussion, use_melodic_percussion, metronome, note_length, can_same_note_play_twice, speed_fine_tune):
    instruments = {  #"name": [channel, program_for_melody_instrument_or_pitch_for_percussion, pitches_to_shift]
        "harp": [0, 6, 0],
        "bass": [2, 32, -24], #MIDI visualizer matches channel 9 to channel 1 and I need bass to be separate from percussion
        "snare": [9, 38 if not use_visual_percussion else 26, 0], #sadly we can't convert pitch for percussion (channel 9) instruments,
        "hat": [9, 42 if not use_visual_percussion else 28, 0], #because it is needed for different percussion instruments
        "basedrum": [9, 35 if not use_visual_percussion else 24, 0],
#        "bell": [3, 14, 24], #uncomment these if you want to record music with these instruments too (Wynncraft doesn't have these)
#        "flute": [4, 73, 12],
#        "chime": [5, 112, 24],
#        "guitar": [6, 24, -12],
#        "xylophone": [7, 12, 24],
#        "iron_xylophone": [8, 11, 0],
#        "cow_bell": [11, 113, 12], #mapped to agogo because cowbell is a percussion instrument
#        "didgeridoo": [12, 111, -24], #mapped to shehnai because there's no didgeridoo
#        "bit": [13, 80, 0],
#        "banjo": [14, 105, 0],
#        "pling": [15, 4, 0],
    } if not use_melodic_percussion else { #this converts percussion instruments while preserving pitch information
        "harp": [0, 6, 0],
        "bass": [2, 32, -24],
        "snare": [3, 114, -49],
        "hat": [4, 119, -49],
        "basedrum": [5, 116, -49],
    }
    
    metronome = noteblock_music_utility.get_metronome_info(data, metronome, False)
    
    new_data = [
        ["0", "0", "Header", "1", "2", str(metronome * 4)], #number of clock pulses per quarter note
        ["1", "0", "Start_track"],
#        ["1", "0", "Time_signature", "4", "2", "5", "8"], #why would I provide anything if I know nothing about this
        ["1", "0", "Tempo", str(int(metronome * 100000 / speed_fine_tune + 0.5))], #The tempo is specified as the Number of microseconds per quarter note; 40 midi ticks always mean 1 second
        ["1", "0", "End_track"],
        ["2", "0", "Start_track"],
        ]
    
    for i in instruments:
        if instruments[i][0] != 9:
            new_data.append(["2", "0", "Program_c", str(instruments[i][0]), str(instruments[i][1])])
    
    current_midi_tick = 0
    delay_to_noteoff = int(-note_length * metronome + 0.5 if note_length < 0 else note_length + 0.5) #measured in (1/40)s (midi clock)
    notes_waiting_for_off = [] #[[current_tick_when_started, channel, note], [...]]
    
    for i in data:
        current_midi_tick += int(i[1])

        if notes_waiting_for_off != []:
            while notes_waiting_for_off[0][0] + delay_to_noteoff <= current_midi_tick:
                finished_note = notes_waiting_for_off.pop(0)
                new_data.append(["2", str(finished_note[0] + delay_to_noteoff), "Note_off_c", str(finished_note[1]), str(finished_note[2]), "0"])
                if len(notes_waiting_for_off) == 0:
                    break
        
#        if i[2] == "0.0": #somehow the pitch got 0.0 (it should be between 0.5 and 2) and math.log threw an error (understandably)
#            continue #this happened in Endless Climb (Tower of Ascension 1) 2 times e.g.
        
        channel = instruments[i[0]][0]
        note = int(math.log(float(i[2]), 2) * 12 + 66.5) + instruments[i[0]][2] if channel != 9 else instruments[i[0]][1]
        volume = 127 if float(i[3]) > 1.0 else int(math.sqrt(float(i[3])) * 127 + 0.5)
        
        if not can_same_note_play_twice:
            for jndex, j in enumerate(notes_waiting_for_off): #trying to see if there's the same note already playing and offing it
                if channel == j[1] and note == j[2]:
                    new_data.append(["2", str(current_midi_tick), "Note_off_c", str(channel), str(note), "0"])
                    notes_waiting_for_off.pop(jndex)
                    break
        
        new_data.append(["2", str(current_midi_tick), "Note_on_c", str(channel), str(note), str(volume)])
        notes_waiting_for_off.append([current_midi_tick, channel, note])
    
    for i in notes_waiting_for_off:
        current_midi_tick = i[0] + delay_to_noteoff
        new_data.append(["2", str(current_midi_tick), "Note_off_c", str(i[1]), str(i[2]), "0"])
        
    new_data.append(["2", str(current_midi_tick + 40), "End_track"])
    new_data.append(["0", "0", "End_of_file"])
    return new_data

def convert_to_midi_file(data, file, keep_newcsv):
    new_data = [', '.join(i) for i in data]
    csv_string = '\n'.join(new_data)

    with open(file + ".newcsv", "w") as output_csv:
        output_csv.write(csv_string)
    midi_object = py_midicsv.csv_to_midi(file + ".newcsv")
    if not keep_newcsv:
        os.remove(file + ".newcsv")

    with open(file + ".mid", "wb") as output_file:
        midi_writer = py_midicsv.FileWriter(output_file)
        midi_writer.write(midi_object)

def main():
    args = parse_arguments()
    for file in noteblock_music_utility.get_input_files(args["input_files"]):
        data = noteblock_music_utility.import_csv_file(file)
        data = convert_and_add_off(data, args["use_visual_percussion"], args["use_melodic_percussion"], args["metronome"], args["note_length"], args["can_same_note_play_twice"], args["speed_fine_tune"])
        convert_to_midi_file(data, file[:-4], args["keep_newcsv"])

if __name__ == '__main__':
    main()
