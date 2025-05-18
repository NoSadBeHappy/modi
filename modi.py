import py_midicsv as pm
import csv

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

#to csv
with open("example_converted.csv", "w") as f:
    f.writelines(csv_midi)

#to list
list_csv_midi = list(csv.reader(csv_midi, delimiter=","))


#flatten list: https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
#only used for extracting key signature
flat_list_csv_midi = [
    x
    for xs in list_csv_midi
    for x in xs
]
#subtract the key signature number from all note numbers in colum e get to C. (record this value in a var)

KeySignature = int(flat_list_csv_midi[flat_list_csv_midi.index( ' Key_signature') + 1])

pos = int(0)

mode = input("what mode do you want it in? (put the tonic in Major, so 1: ionian (Major), 2: Dorian, 3: Phrygian. 4: Lydian, 5: Mixolydian, 6: Aeolian (minor), 7: Locrian: ") #key change amount
minor = input("is the input midi file in minor? (true or false): ")#true or false is current in minor or major

print (pos)
for line in list_csv_midi:
    for pos in line: #always adds 1 to pos every time it loops, this looks for Note_on_c and WILL LOOK FOR Note_off_c
        print (pos)
        if (list_csv_midi[int(line)][int(float(pos))] == " Note_on_c"):
            #pos is now the position where the int we need to change is
            pos = pos + 2
            list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) - KeySignature #go to c temperarly to more easily change mode
        if (minor == True): #convert to major if needed
            if int(list_csv_midi[line][int(float(pos))]) in aeolian:
                #convert minor to major
                list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) + 1

        #mode == 1 is not needed, its already in major so yay!
        if (mode == 2): # lower B E
            if int(list_csv_midi[line][int(float(pos))]) in dorian:
                list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) - 1
        elif (mode == 3): # lower B E A D
            if int(list_csv_midi[line][int(float(pos))]) in phrygian:
                list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) - 1
        elif (mode == 4): #raise F
            if int(list_csv_midi[line][int(float(pos))]) in lydian:
                list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) + 1
        elif (mode == 5): #lower B
            if int(list_csv_midi[line][int(float(pos))]) in mixolydian:
                list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) - 1
        elif (mode == 6): #lower B E A
            if int(list_csv_midi[line][int(float(pos))]) in aeolian:
                list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) - 1
        elif (mode == 7): #lower B E A D G
            if int(list_csv_midi[line][int(float(pos))]) in locrian:
                list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) - 1
        list_csv_midi[line][int(float(pos))] = int(list_csv_midi[line][int(float(pos))]) + KeySignature #get back to real key at the end


#ADD A LIST TO CSV PARSER



# Parse the CSV output of the previous command back into a MIDI file
midi_object = pm.csv_to_midi(csv_string_list)

# Save the parsed MIDI file to disk
with open("example_converted.mid", "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)
