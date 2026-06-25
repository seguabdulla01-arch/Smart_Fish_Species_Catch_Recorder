import os

dataset_dir = 'dataset'
classes = sorted(os.listdir(dataset_dir))
print("Detected class order:")
for c in classes:
    print(c)
