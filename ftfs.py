import os, shutil, pathlib
import time
from tqdm import tqdm  # Add tqdm for progress bar

# This is a script created for formatting the "cats vs dogs" 
# training data to more suitable folder hierarchy for importing into keras
# It can be used to format data where the label is found in the filename
# to change it to a folder based labelling system

# Author: Markus Vallin

# We will also perform a test train split for the data here
# If split is set to 0 we will only make a training folder
test_train_split = 0.2

#Wheter to delete or copy existing data
delete_original_data = False

# The folder containing the data to be formatted
data_dir = r"" # A full path

# Function for finding label from filename
find_label = lambda x: x.split('.')[0]

parent_dir = pathlib.Path(data_dir).parent

# Labels and amount
labels = {}
data = {}

# If we are to make a split create 2 folders
if test_train_split > 0:
    train_dir = parent_dir / 'train_data'
    test_dir = parent_dir / 'test_data'
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
else:
    train_dir = parent_dir / 'train_data'
    os.makedirs(train_dir, exist_ok=True)
    
# Get the list of all files in the original dataset directory
data_files = os.listdir(data_dir)

# First count labels and make folders for data_separation and split
for file in os.listdir(data_dir):
    filename = os.fsdecode(file)
    label = find_label(filename)
    
    # Check if label exists and increment amount of labels
    if label not in labels:
        labels[label] = 1
        os.makedirs(os.path.join(train_dir, label), exist_ok=True)
        if test_train_split > 0:
            os.makedirs(os.path.join(test_dir, label), exist_ok=True)
    else:
        labels[label] += 1

    # Add file to data dict
    if label not in data:
        data[label] = [filename]
    else:
        data[label].append(filename)
    
# Print information about data
print("\nData distribution:")
for label, files in data.items():
    print(f"{label}: {len(files)} files")

# Calculate testing and training split
num_train = {}
num_test = {}

for label, files in data.items():
    num_files = len(files)
    num_test[label] = int(num_files * test_train_split)
    num_train[label] = num_files - num_test[label]

print("\nTraining and Testing split:")
for label in data.keys():
    print(f"{label}: {num_train[label]} training files, {num_test[label]} testing files")

# Start operation
print("\nStarting operation...")
start_time = time.time()

# Separate data
total_files = sum(len(files) for files in data.values())
processed_files = 0

for label, files in data.items():
    # Shuffle files to ensure random distribution
    shuffled_files = sorted(files, key=lambda k: os.urandom(16))
    
    # Split files into training and testing sets
    train_files = shuffled_files[:num_train[label]]
    test_files = shuffled_files[num_train[label]:num_train[label] + num_test[label]]
    
    print(f"\nProcessing label: {label}")
    print(f"Training files for {label}: {len(train_files)}")
    print(f"Testing files for {label}: {len(test_files)}")
    
    # Move or copy files to the respective directories
    for file in tqdm(train_files, desc=f"Processing {label} training files", leave=False):
        src = os.path.join(data_dir, file)
        dst = os.path.join(train_dir, label, file)
        if delete_original_data:
            shutil.move(src, dst)
        else:
            shutil.copy(src, dst)
        processed_files += 1
    
    for file in tqdm(test_files, desc=f"Processing {label} testing files", leave=False):
        src = os.path.join(data_dir, file)
        dst = os.path.join(test_dir, label, file)
        if delete_original_data:
            shutil.move(src, dst)
        else:
            shutil.copy(src, dst)
        processed_files += 1

# Clear the progress bar
print("\nOperation completed.")

end_time = time.time()
print(f"Operation completed in {end_time - start_time:.2f} seconds")