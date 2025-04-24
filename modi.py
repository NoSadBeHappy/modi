import py_midicsv as pm

A = [9, 21, 33, 45, 57, 69, 81, 93, 105, 117]
B = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119]
D = [2, 14, 26, 38, 50, 62, 74, 86, 98, 110, 122]
E = [4, 16, 28, 40, 52, 64, 76, 88, 100, 112, 124]
F = [5, 17, 29, 41, 53, 65, 77, 89, 101, 113, 125]
G = [7, 19, 31, 43, 55, 67, 79, 91, 103, 115, 127]

dorian = [B, E]
phrygian = [B, E, A, D]
lydian = [F]
mixolydian = [B]
aeolian = [B, E, A]
locrian = [B, E, A, D, G]

#midi info: https://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html
#modes: https://en.wikipedia.org/wiki/Mode_(music)

# Load the MIDI file and parse it into CSV format
csv_midi = pm.midi_to_csv("example.mid")

with open("example_converted.csv", "w") as f:
    f.writelines(csv_midi)

#subtract the key signature number from all note numbers in colum e get to C. (record this value in a var)

KeySignature = csv_midi.index("Key_signature") + 1

pos = 0

mode = input("what mode do you want it in? (put the tonic in Major, so 1: ionian (Major), 2: Dorian, 3: Phrygian. 4: Lydian, 5: Mixolydian, 6: Aeolian (minor), 7: Locrian") #key change amount
minor = input("is the input midi file in minor?")#true or false is current in minor or major

pos = index("Notes_on_c", pos) #skip to the first one
for pos in csv_midi: #always adds 1 to pos every time it loops, this looks for Note_on_c and WILL LOOK FOR Note_off_c
    if (pos == "Note_on_c"):
        #pos is now the position where the int we need to change is
        pos = pos + 2
    csv_midi[pos] = csv_midi[pos] - KeySignature #go to c temperarly to more easily change mode
    if (minor == true): #convert to major if needed
        if csv_midi[pos] in aeolian:
            #convert minor to major
            csv_midi[pos] = csv_midi + 1

    #mode == 1 is not needed, its already in major so yay!
    if (mode == 2): # lower B E
        if csv_midi[pos] in dorian:
            csv_midi[pos] = csv_midi[pos] - 1
    elif (mode == 3): # lower B E A D
        if csv_midi[pos] in phrygian:
            csv_midi[pos] = csv_midi[pos] - 1
    elif (mode == 4): #raise F
        if csv_midi[pos] in lydian:
            csv_midi[pos] = csv_midi[pos] + 1
    elif (mode == 5): #lower B
        if csv_midi[pos] in mixolydian:
            csv_midi[pos] = csv_midi[pos] - 1
    elif (mode == 6): #lower B E A
        if csv_midi[pos] in aeolian:
            csv_midi[pos] = csv_midi[pos] - 1
    elif (mode == 7): #lower B E A D G
        if csv_midi[pos] in locrian:
            csv_midi[pos] = csv_midi[pos] - 1

    csv_midi[pos] = csv_midi[pos] + KeySignature #get back to real key at the end

# Parse the CSV output of the previous command back into a MIDI file
midi_object = pm.csv_to_midi(csv_string_list)

# Save the parsed MIDI file to disk
with open("example_converted.mid", "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)
