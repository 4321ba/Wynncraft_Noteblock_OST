#!/bin/sh

#the midi_converter.py, nbs_converter.py and noteblock_music_utility.py scripts are from https://github.com/4321ba/noteblock_music_yoinker
#but I copied them here too, so I for sure won't screw up compatibility

#creating the midis for scores, using the default settings (every note is 1/16th note long, without melodic percussion)
./midi_converter.py cut_csv/*.csv
#we need special attention for these pieces, as they have strange tps, and we need fine tuning (-f) to play them at the right speed
./midi_converter.py cut_csv/027_Modified_Black_Road_Nostalgia_Black_Road.csv -f 0.9625
./midi_converter.py cut_csv/060_Wings_of_Distrust_Avos_Theme.csv -f 0.9625
./midi_converter.py cut_csv/069_Lament_of_the_Decay_Gelibord.csv -f 0.9625
./midi_converter.py cut_csv/160_Earthquake_Boss_Battle_14.csv -f 0.9
./midi_converter.py cut_csv/164_Face_of_Extinction_Boss_Battle_17.csv -f 0.9
./midi_converter.py cut_csv/167_Burning_Encounter_Boss_Battle_16.csv -f 0.9
./midi_converter.py cut_csv/169_Enter_the_Hero_Siegfried_Fanfare.csv -f 0.9
./midi_converter.py cut_csv/152_Part_1_A_Family_Fractured_570_AP.csv -f 0.96875
./midi_converter.py cut_csv/152_Part_4_A_Family_Fractured_570_AP.csv -f 0.96875
mv cut_csv/*.mid musescore_midi/

#creating the midis to listen with a regular soundfont (General Midi, GM), this is with 1/4 second long notes (much longer than the ~1/10 of the musescore midis), and without melodic percussion
./midi_converter.py cut_csv/*.csv -l10
#we need special attention for these pieces, as they have strange tps, and we need fine tuning (-f) to play them at the right speed
./midi_converter.py cut_csv/027_Modified_Black_Road_Nostalgia_Black_Road.csv -f 0.9625 -l10
./midi_converter.py cut_csv/060_Wings_of_Distrust_Avos_Theme.csv -f 0.9625 -l10
./midi_converter.py cut_csv/069_Lament_of_the_Decay_Gelibord.csv -f 0.9625 -l10
./midi_converter.py cut_csv/160_Earthquake_Boss_Battle_14.csv -f 0.9 -l10
./midi_converter.py cut_csv/164_Face_of_Extinction_Boss_Battle_17.csv -f 0.9 -l10
./midi_converter.py cut_csv/167_Burning_Encounter_Boss_Battle_16.csv -f 0.9 -l10
./midi_converter.py cut_csv/169_Enter_the_Hero_Siegfried_Fanfare.csv -f 0.9 -l10
./midi_converter.py cut_csv/152_Part_1_A_Family_Fractured_570_AP.csv -f 0.96875 -l10
./midi_converter.py cut_csv/152_Part_4_A_Family_Fractured_570_AP.csv -f 0.96875 -l10
mv cut_csv/*.mid general_midi/

#creating the midis to listen with the special wynncraft_soundfont.sf2, this is with 2 second long notes (so it can fade out on its own), and with (GM-incompatible) melodic percussion
./midi_converter.py cut_csv/*.csv -l80 -e
#we need special attention for these pieces, as they have strange tps, and we need fine tuning (-f) to play them at the right speed
./midi_converter.py cut_csv/027_Modified_Black_Road_Nostalgia_Black_Road.csv -f 0.9625 -l80 -e
./midi_converter.py cut_csv/060_Wings_of_Distrust_Avos_Theme.csv -f 0.9625 -l80 -e
./midi_converter.py cut_csv/069_Lament_of_the_Decay_Gelibord.csv -f 0.9625 -l80 -e
./midi_converter.py cut_csv/160_Earthquake_Boss_Battle_14.csv -f 0.9 -l80 -e
./midi_converter.py cut_csv/164_Face_of_Extinction_Boss_Battle_17.csv -f 0.9 -l80 -e
./midi_converter.py cut_csv/167_Burning_Encounter_Boss_Battle_16.csv -f 0.9 -l80 -e
./midi_converter.py cut_csv/169_Enter_the_Hero_Siegfried_Fanfare.csv -f 0.9 -l80 -e
./midi_converter.py cut_csv/152_Part_1_A_Family_Fractured_570_AP.csv -f 0.96875 -l80 -e
./midi_converter.py cut_csv/152_Part_4_A_Family_Fractured_570_AP.csv -f 0.96875 -l80 -e
mv cut_csv/*.mid melodic_percussion_midi/

#creating the nbs files, to be opened with any NBS software, using the old format
./nbs_converter.py cut_csv/*.csv
#we need special attention for these pieces, as they have strange tps, and we need fine tuning (-f) to play them at the right speed
./nbs_converter.py cut_csv/027_Modified_Black_Road_Nostalgia_Black_Road.csv -f 0.9625
./nbs_converter.py cut_csv/060_Wings_of_Distrust_Avos_Theme.csv -f 0.9625
./nbs_converter.py cut_csv/069_Lament_of_the_Decay_Gelibord.csv -f 0.9625
./nbs_converter.py cut_csv/160_Earthquake_Boss_Battle_14.csv -f 0.9
./nbs_converter.py cut_csv/164_Face_of_Extinction_Boss_Battle_17.csv -f 0.9
./nbs_converter.py cut_csv/167_Burning_Encounter_Boss_Battle_16.csv -f 0.9
./nbs_converter.py cut_csv/169_Enter_the_Hero_Siegfried_Fanfare.csv -f 0.9
./nbs_converter.py cut_csv/152_Part_1_A_Family_Fractured_570_AP.csv -f 0.96875
./nbs_converter.py cut_csv/152_Part_4_A_Family_Fractured_570_AP.csv -f 0.96875
mv cut_csv/*.nbs nbs/

node rename.js