import py_midicsv as pm
import csv
import io

# Note sets for modes
A = [9, 21, 33, 45, 57, 69, 81, 93, 105, 117]
B = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119]
D = [2, 14, 26, 38, 50, 62, 74, 86, 98, 110, 122]
E = [4, 16, 28, 40, 52, 64, 76, 88, 100, 112, 124]
F = [5, 17, 29, 41, 53, 65, 77, 89, 101, 113, 125]
G = [7, 19, 31, 43, 55, 67, 79, 91, 103, 115, 127]

# Mode definitions
dorian = [note for scale in [B, E] for note in scale]
phrygian = [note for scale in [B, E, A, D] for note in scale]
lydian = [note for scale in [F] for note in scale]
mixolydian = [note for scale in [B] for note in scale]
aeolian = [note for scale in [B, E, A] for note in scale]
locrian = [note for scale in [B, E, A, D, G] for note in scale]

# Load the MIDI file and parse it into CSV format
csv_midi = pm.midi_to_csv("example.mid")

# Convert csv_midi list of strings to list of lists
list_csv_midi = list(csv.reader(io.StringIO(''.join(csv_midi))))

# Save the CSV (optional)
csv_string_list = [",".join(line) + "\n" for line in list_csv_midi]
with open("example.csv", "w") as f:
    f.writelines(csv_string_list)

# Convert back to MIDI and save
midi_object = pm.csv_to_midi(csv_string_list)
with open("example_output.mid", "wb") as output_file:
    pm.FileWriter(output_file).write(midi_object)

# Parse all key signature changes
key_changes = []  # List of (tick, key_signature)

for line in list_csv_midi:
    if len(line) > 4 and line[2].strip() == "Key_signature":
        try:
            tick = int(line[1].strip())
            key = int(line[4].strip())
            key_changes.append((tick, key))
        except:
            pass

# Sort key changes by time
key_changes.sort()

# Default to C if no key signatures found
if not key_changes:
    key_changes = [(0, 0)]

# Function to get key signature at a given tick
def get_key_signature_at_tick(tick):
    active_key = 0
    for change_tick, key in key_changes:
        if tick >= change_tick:
            active_key = key
        else:
            break
    return active_key

# Get user input
mode = int(input("Select mode (1: Ionian, 2: Dorian, 3: Phrygian, 4: Lydian, 5: Mixolydian, 6: Aeolian, 7: Locrian): ").strip())
minor = input("Is the input MIDI in minor? (true or false): ").strip().lower() == "true"

# Helper to apply mode transformation
def apply_mode(note, key):
    # Transpose to C
    note -= key

    # Minor to major
    if minor and note in aeolian:
        note += 1

    # Mode alterations
    if mode == 2 and note in dorian:
        note -= 1
    elif mode == 3 and note in phrygian:
        note -= 1
    elif mode == 4 and note in lydian:
        note += 1
    elif mode == 5 and note in mixolydian:
        note -= 1
    elif mode == 6 and note in aeolian:
        note -= 1
    elif mode == 7 and note in locrian:
        note -= 1

    # Transpose back to original key
    return note + key

# Process all note events
for i, line in enumerate(list_csv_midi):
    if len(line) > 4 and line[2].strip() in ("Note_on_c", "Note_off_c"):
        try:
            tick = int(line[1].strip())
            key = get_key_signature_at_tick(tick)
            original_note = int(line[4])
            new_note = apply_mode(original_note, key)
            list_csv_midi[i][4] = str(new_note)
        except Exception as e:
            print(f"Error processing line {i}: {e}")

# Save the CSV (optional)
csv_string_list = [",".join(line) + "\n" for line in list_csv_midi]
with open("example_converted.csv", "w") as f:
    f.writelines(csv_string_list)


# Convert back to MIDI and save
midi_object = pm.csv_to_midi(csv_string_list)
with open("example_converted.mid", "wb") as output_file:
    pm.FileWriter(output_file).write(midi_object)

print("Output saved to example_converted.mid")
