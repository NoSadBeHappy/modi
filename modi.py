import py_midicsv as pm

#midi info: https://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html

# Load the MIDI file and parse it into CSV format
csv_string_list = pm.midi_to_csv("example.mid")

with open("example_converted.csv", "w") as f:
    f.writelines(csv_string_list)

#subtract the key signature number from all note numbers in colum e get to C. (record this value in a var)
#convert to major if in minor by +1 from all the E, A, and B numbers.
#convert to desired mode
#add key signature to get back to the right key




# Parse the CSV output of the previous command back into a MIDI file
midi_object = pm.csv_to_midi(csv_string_list)

# Save the parsed MIDI file to disk
with open("example_converted.mid", "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)
