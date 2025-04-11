import py_midicsv as pm

# Load the MIDI file and parse it into CSV format
csv_string_list = pm.midi_to_csv("example.mid")

with open("example_converted.csv", "w") as f:
    f.writelines(csv_string_list)

#subtract the key signature number from all note numbers in colum E to get to C. (record this value in a var)














# Parse the CSV output of the previous command back into a MIDI file
midi_object = pm.csv_to_midi(csv_string_list)

# Save the parsed MIDI file to disk
with open("example_converted.mid", "wb") as output_file:
    midi_writer = pm.FileWriter(output_file)
    midi_writer.write(midi_object)
