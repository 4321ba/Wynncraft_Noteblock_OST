# Wynncraft Noteblock OST
Note-by-note Wynncraft music in NBS and MIDI formats.  
Written by the talented people at Wynncraft, more specifically see here: https://wynncraft.gamepedia.com/Music .  
Lincense copied from XavierEXE's playlist: https://www.youtube.com/playlist?list=PLyqkjDCr8kbI3CjNZimiri8shU1GbfJ6E . You should listen to that too if you aren't interested in different instruments / MIDI.  
My piano tutorial playlist using these: https://www.youtube.com/playlist?list=PLDa4Vj43E2e-mCukFLGM5xTLILNZ_daaI .  
For the GitHub repo with the mp3 files look here: https://github.com/Wynntils/WynncraftOST .  
For Scores and MIDI files see also Xeoran's work: https://musescore.com/user/7400466/sets/5090208 .

The source csv files found in `cut_csv` were recorded with https://github.com/4321ba/noteblock_music_yoinker and antilagged, so there is no lag. Sadly, there's a bug https://forums.wynncraft.com/threads/music-note-volume-is-messed-up.281761/ that the NBS player plays the wrong volume sometimes, so this is reflected here as well. You can find some pieces that consist of more than one part, you can also find the source in `cut_csv` for them.

NBS files are in the `nbs` folder. They use the old format, so you can open them with NBS and also ONBS. Please do NOT copy these to play on your Minecraft server without the Wynncraft team's approval. (I think it's fine if you play it to your friend e.g. just don't compete with Wynncraft, I'm no lawyer though.) Also, see `Sounds.zip` for the Wynncraft noteblock sounds for NBStudio from the 1.19 resource pack, cut shorter (no silence at the end) so all notes can be played back even with the crazier pieces (khmm CtC).

In the `musescore_midi` folder you can find the MIDI files that are best opened in MuseScore (and maybe other score creation software) to create a score / sheet music from them. This is achieved by making the notes really short (2/20 sec or 3/20 sec) so they don't overlap with each other. MuseScore can then lengthen it if it is needed. This is pretty much identical to this Google Drive folder: https://drive.google.com/drive/folders/1ga9nTBblcy4ssXA5m4E2PEmXRmAXh4zF .

In the `general_midi` folder you can find the MIDI files that can best be played back with a General MIDI compatible soundfont / player. This is the one you can listen to the best if you want to. Here the notes are 1/4 second long.

In the `melodic_percussion_midi` folder you can find the MIDI files that are best suited to be played back with `wynncraft_soundfont.sf2`. The notes are pretty long here (2 seconds) and the percussion is not GM MIDI compatible, but preserves pitch. You can also use this if you want to create a custom soundfont to play them back with melodic percussion.

The Wynncraft soundfont (`wynncraft_soundfont.sf2`) has 5 melodic instruments:  
harp mapped to harpsichord,  
bass mapped to acoustic bass (2 octave lower than harp),  
snare mapped to steel drums (4 octave and 1 half-note lower),  
hat mapped to reverse cymbal (4 octave and 1 half-note lower) and  
basedrum mapped to taiko drum (4 octave and 1 half-note lower)  
and 3 percussion instruments:  
snare mapped to acoustic snare,  
hat mapped to closed hi-hat and  
basedrum mapped to acoustic bass drum,  
good for playing all the midi files (with normal or with melodic percussion) found here.

You can also try to generate the midi files and the nbs files from the csv files, using `convert.sh`.

There are alternative midi files in `Wynncraft_Noteblock_OST_layered_volumed_midis.zip`, there, the notes are on separate channels based on the volume. Though not all volumes are on different channels, because there are not enough channels (max 16).  
The midis in `Wynncraft_Noteblock_OST_separated_instruments_midis.zip` are for every instrument in a completely separate file, and in every file every volume level (max 10) is on separate channel too. (iirc)

If something feels wrong, be sure to open an issue!
