# train_model.py
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os, json

# --- Dataset path ---
data_dir = "dataset/train"
model_dir = "model"
os.makedirs(model_dir, exist_ok=True)

# --- Prepare data ---
datagen = ImageDataGenerator(rescale=1./255)
train_gen = datagen.flow_from_directory(
    data_dir,
    target_size=(128, 128),
    batch_size=16,
    class_mode='categorical'
)

# --- Build CNN model ---
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(len(train_gen.class_indices), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("🚀 Training started...")
model.fit(train_gen, epochs=10)
print("✅ Training completed successfully!")

# --- Save model and class labels ---
model.save(os.path.join(model_dir, "fish_species_cnn.h5"))
print("✅ Model saved to model/fish_species_cnn.h5")

with open(os.path.join(model_dir, "class_names.json"), "w") as f:
    json.dump(train_gen.class_indices, f)
print("✅ Class names saved successfully to model/class_names.json")
