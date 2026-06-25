from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import os

# ✅ Create ImageDataGenerator
datagen = ImageDataGenerator(rescale=1.0/255)

# ✅ Load training dataset (make sure this folder exists)
train_generator = datagen.flow_from_directory(
    'dataset/train',
    target_size=(128, 128),
    class_mode='categorical'
)

# ✅ Save class labels (order matters for correct fish names)
os.makedirs('model', exist_ok=True)
with open("model/class_names.json", "w") as f:
    json.dump(train_generator.class_indices, f)

print("✅ Class names saved successfully to model/class_names.json")
print(train_generator.class_indices)
