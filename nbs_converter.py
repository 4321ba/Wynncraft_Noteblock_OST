#!/usr/bin/python3

import math
import argparse
import noteblock_music_utility

def parse_arguments():
    parser = argparse.ArgumentParser(description="convert specific .csv files to the old .nbs format files")
    parser.add_argument("input_files", nargs="*", default=[], help="csv files to convert, leave blank for all from current directory")
    parser.add_argument("-m", "--metronome", type=int, default=-1, help="the smallest possible tick difference between notes, e.g. 4, can be determined automatically, 40 / metronome = tempo")
    parser.add_argument("-f", "--speed_fine_tune", type=float, default = 1, help="my solution to obscure tempo: metronome value must be integer, but if in theory it is 10/3 e.g. (meaning 40/(10/3)=12 tps in NBS) and in reality it is 3, you should set this to 3/(10/3) = 0.9 meaning the speed will be multiplied by 0.9 and it will be slower then expected")
    parser.add_argument("-o", "--original_order", action='store_true', dest="is_original_order", help="if this flag is set, the order of the noteblocks won't change (it will probably look quite messy), otherwise they will be grouped by instrument and volume")
    return vars(parser.parse_args())

#nbs instrument list
INSTRUMENTS = {
    "harp": 0,
    "bass": 1,
    "snare": 3,
    "hat": 4,
    "basedrum": 2,
    "bell": 7,
    "flute": 6,
    "chime": 8,
    "guitar": 5,
    "xylophone": 9,
}

def make_volume_int(data):
    new_data = []
    for note in data:
        note[3] = min(max(int(float(note[3]) * 100 + 0.5), 1), 100)
        new_data.append(note)
    return new_data

def get_ivc(instrument, volume):
    #ivc stands for instrument volume code
    #it is a numerical representation of the instrument and the volume together
    #that is unambiguous, and can be easily sorted for the best order
    return (INSTRUMENTS[instrument] + 1) * 100 - volume

def from_ivc(ivc):
    reverse_instruments = {value: key for key, value in INSTRUMENTS.items()}
    instrument = reverse_instruments[ivc // 100]
    volume = 100 - ivc % 100
    return instrument, volume

def get_all_layer_counts(data):
    #Here we get all the information from data, how many notes are in each instrument at the ticks, in the same group
    all_layers = [[[get_ivc(data[0][0], data[0][3]), 0]]] #e.g. [[[100, 3], [120, 4], [30, 2], ...], [[100, 1], ...], ...] 3D list, 1st D: time, 2nd D: instruments, 3rd: instrument volume code and the number of layers with it
    for i in data:
        if i[1] == "0":
            if all_layers[-1][-1][0] == get_ivc(i[0], i[3]): #if the last note's ivc is the same
                all_layers[-1][-1][1] += 1
            else:
                all_layers[-1].append([get_ivc(i[0], i[3]), 1])
        else:
            all_layers.append([[get_ivc(i[0], i[3]), 1]])
    return all_layers
    
def get_best_layers_with_preference_algorithm(all_layers):
    #Here we determine what order the layers will be in, based on the preference value
    layers = [] #e.g. [[100, 3], [120, 4], [30, 2], ...] the number of layers with that ivc
    while len(all_layers) > 0:
        preference = {} #{100: [*preference value*, *max number of notes*], 120: [*preference value*, *max number of notes*], ...}
        for tick in all_layers:
            if tick[0][0] not in preference:
                preference[tick[0][0]] = [0, 0]
            preference[tick[0][0]][0] += len(tick) ** 2 #preference value is calculated by how many different instruments are behind the particular instrument, squared; the biggest value wins
            if preference[tick[0][0]][1] < tick[0][1]:
                preference[tick[0][0]][1] = tick[0][1]
        preference = {key: value for key, value in sorted(preference.items(), key = lambda item: -item[1][0])} #this not only finds the biggest value, but organizes it descending, which we may not really want
        chosen_ivc = list(preference.keys())[0]
        layers.append([chosen_ivc, preference[chosen_ivc][1]])
#        print(preference, chosen_instrument)
        new_layers = []
        for tick in all_layers: #deleting the instruments that got chosen
            if tick[0][0] != chosen_ivc:
                new_layers.append(tick)
            elif len(tick) > 1:
                new_layers.append(tick[1:])
        all_layers = new_layers
    return layers
    
def get_jumps_and_layer_names(data, layers):
    #data is the regular data except volume is 100× and int
    #layers are [[100, 4], [140, 2], [ivc: count], ...]
    max_layer_count = 0
    layer_offsets = []
    layer_names = []
    layer_volumes = []
    #Here we populate the layer_offsets, based on the layers data
    new_layers = layers.copy()
    notes_in_current_instrument = 0
    for i in data:
        jumps = 1
        if i[1] != "0":
            new_layers = layers.copy()
            notes_in_current_instrument = 0
        if new_layers[0][0] == get_ivc(i[0], i[3]):
            notes_in_current_instrument += 1
        else:
            while new_layers[0][0] != get_ivc(i[0], i[3]):
                jumps += new_layers.pop(0)[1]
            jumps -= notes_in_current_instrument
            notes_in_current_instrument = 1
        layer_offsets.append(jumps)
    #Here we get the names for the layers
    for layer in layers:
        max_layer_count += layer[1]
        instrument, volume = from_ivc(layer[0])
        for i in range(layer[1]):
            layer_names.append(str(i + 1) + ". " + str(volume) + "% " + instrument.capitalize())
            layer_volumes.append(volume)
    return max_layer_count, layer_offsets, layer_names, layer_volumes
    
def get_smart_note_placement(data):
    all_layers = get_all_layer_counts(data)
    layers = get_best_layers_with_preference_algorithm(all_layers)
    print("Identified layers:", layers)
    return get_jumps_and_layer_names(data, layers)

def reorganizer(data):
    new_data = [[]] #e.g.: [[["harp", "0", "1.0", "1.0"], [...], ...], [[...], [...], ...]]
    delays = [data[0][1]]
    layers = {}
    data[0][1] = "0"
    for i in data:
        if i[1] == "0":
            new_data[-1].append(i)
        else:
            delays.append(i[1])
            new_data.append([[i[0], "0", i[2], i[3]]])
    
    data = []
    for index, tick in enumerate(new_data):
        tick.sort(key = lambda x: get_ivc(x[0], x[3]))
        tick[0][1] = str(delays[index])
        data += tick
        instrument_count = {}
        for note in tick:
            ivc = get_ivc(note[0], note[3])
            if not ivc in instrument_count.keys():
                instrument_count[ivc] = 0
            instrument_count[ivc] += 1
        for ivc in instrument_count:
            if ivc not in layers.keys() or layers[ivc] < instrument_count[ivc]:
                layers[ivc] = instrument_count[ivc]
    
    new_layers = [[key, value] for key, value in sorted(layers.items(), key = lambda item: item[0])]
    print("Identified layers:", new_layers)
    max_layer_count, layer_offsets, layer_names, layer_volumes = get_jumps_and_layer_names(data, new_layers)
    return max_layer_count, layer_offsets, layer_names, layer_volumes, data
    
def write_byte(file, number):
    file.write(bytearray([number]))

def write_short(file, number):
    file.write(bytearray([number % 256, number // 256]))

def write_integer(file, number):
    file.write(bytearray([number % 256, number // 256 % 256, number // 65536 % 256,  number // 16777216]))

def write_string(file, string):
    binary_string = string.encode("latin-1", "replace")
    write_integer(file, len(binary_string))
    file.write(binary_string)

def convert_to_nbs_file(data, metronome, is_original_order, filename, speed_fine_tune):
    
    metronome = noteblock_music_utility.get_metronome_info(data, metronome, False)
    tempo = int(160 * speed_fine_tune / metronome + 0.5) * 25 #rounding to multiplicate of 25 because ONBS can't be more precise and we don't trust that it can round well
    
    data = make_volume_int(data)
    
    max_layer_count = 0
    layer_offsets = [] #stores the "jumps to next layer" value for each note in the same order as data stores the notes
    layer_names = [] #smart note placement names the track based on the instrument
    layer_volumes = [] #from 1 to 100 int

    if is_original_order:
        max_layer_count, layer_offsets, layer_names, layer_volumes = get_smart_note_placement(data)
    else:
        max_layer_count, layer_offsets, layer_names, layer_volumes, data = reorganizer(data)
    
    #file format: https://www.stuffbydavid.com/mcnbs/format
    with open(filename + ".nbs", "wb") as file:
        write_short(file, 10) #it is not important, but it shouldn't be 0 because that's the new format (song length)
        write_short(file, max_layer_count) #layer count
        write_string(file, "") #song name
        write_string(file, "") #song author
        write_string(file, "") #song original author
        write_string(file, "") #song description
        write_short(file, tempo) #tempo
        write_byte(file, 0) #auto-saving, not used
        write_byte(file, 10) #auto-saving interval, not used
        write_byte(file, 4) #time signature
        write_integer(file, 0) #minutes spent
        write_integer(file, 0) #left-clicks
        write_integer(file, 0) #right-clicks
        write_integer(file, 0) #note blocks added
        write_integer(file, 0) #note blocks removed
        write_string(file, filename + ".csv") #imported file name
        
        write_short(file, 1 + int(int(data[0][1]) / metronome + 0.5))
        data[0][1] = "0"
        for i in data: #writing the notes
            if int(int(i[1]) / metronome + 0.5) > 0:
                write_short(file, 0) #close previous tick
                write_short(file, int(int(i[1]) / metronome + 0.5)) #jumps to next tick
            write_short(file, layer_offsets.pop(0)) #jumps to next layer
            write_byte(file, INSTRUMENTS[i[0]]) #instrument
            write_byte(file, int(math.log(float(i[2]), 2) * 12 + 45.5)) #pitch
        write_short(file, 0) #closing last tick
        write_short(file, 0) #closing the notes section
        
        for i in range(max_layer_count): #this part is said to be optional, except ONBS hangs when not provided
            write_string(file, layer_names[i]) #name
            write_byte(file, layer_volumes[i]) #volume
        write_byte(file, 0)

def main():
    args = parse_arguments()
    for file in noteblock_music_utility.get_input_files(args["input_files"]):
        data = noteblock_music_utility.import_csv_file(file)
        convert_to_nbs_file(data, args["metronome"], args["is_original_order"], file[:-4], args["speed_fine_tune"])

if __name__ == '__main__':
    main()
