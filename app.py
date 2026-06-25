from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import sqlite3
import os
from datetime import datetime
import json

# --- CONFIGURATION ---
DB_PATH = 'catch_records.db'
MODEL_PATH = os.path.join('model', 'fish_species_cnn.h5')
CLASS_NAMES_PATH = os.path.join('model', 'class_names.json')

# --- LOAD CLASS NAMES SAFELY ---
import os, json

with open(os.path.join('model', 'class_names.json')) as f:
    class_dict = json.load(f)
    CLASS_NAMES = [k for k, v in sorted(class_dict.items(), key=lambda item: item[1])]

print("✅ Loaded class names:", CLASS_NAMES)



# ✅ Ensure class names are in correct order (sorted by index)
CLASS_NAMES = [name for name, idx in sorted(class_dict.items(), key=lambda x: x[1])]

# --- FISH INFORMATION ---
FISH_INFO = {
    'Catla': {'scientific_name': 'Labeo catla', 'habitat': 'Freshwater rivers and lakes', 'description': 'Popular food fish with high nutrition.'},
    'Rohu': {'scientific_name': 'Labeo rohita', 'habitat': 'Freshwater ponds and rivers', 'description': 'Important aquaculture fish species.'},
    'Tilapia': {'scientific_name': 'Oreochromis niloticus', 'habitat': 'Freshwater & brackish', 'description': 'Second most farmed fish globally.'},
    'Tuna': {'scientific_name': 'Thunnus', 'habitat': 'Open ocean', 'description': 'Fast-swimming predator fish.'},
    'Pomfret': {'scientific_name': 'Pampus argenteus', 'habitat': 'Coastal waters', 'description': 'Flat-bodied and delicate in taste.'},
    'Mackerel': {'scientific_name': 'Scomber', 'habitat': 'Coastal waters', 'description': 'Rich in omega-3 fatty acids.'},
    'Sardine': {'scientific_name': 'Sardina pilchardus', 'habitat': 'Coastal waters', 'description': 'Small, oily schooling fish.'},
    'King Fish': {'scientific_name': 'Scomberomorus', 'habitat': 'Tropical coastal', 'description': 'Firm meat, prized for sport fishing.'},
    'Snapper': {'scientific_name': 'Lutjanus', 'habitat': 'Reef areas', 'description': 'Red-colored and firm texture.'},
    'Barracuda': {'scientific_name': 'Sphyraena', 'habitat': 'Tropical oceans', 'description': 'Predatory fish with sharp teeth.'},
    'Anchovy': {'scientific_name': 'Engraulis', 'habitat': 'Coastal waters', 'description': 'Used in sauces & flavoring.'},
    'Cod': {'scientific_name': 'Gadus', 'habitat': 'Cold deep waters', 'description': 'Mild white fish, commercially important.'},
    'Salmon': {'scientific_name': 'Salmo salar', 'habitat': 'Fresh & marine', 'description': 'Rich in omega-3, pink flesh.'}
}

# --- DATABASE INITIALIZATION ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    species TEXT,
                    quantity INTEGER,
                    kilogram REAL,
                    date TEXT,
                    image TEXT
                )''')
    conn.commit()
    conn.close()

# --- FLASK APP ---
app = Flask(__name__)

# --- LOAD MODEL ---
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

model = load_model(MODEL_PATH)

# --- HOME PAGE ---
@app.route('/')
def home():
    return render_template('index.html')

# --- PREDICT PAGE ---
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    img_file = request.files['image']
    if img_file.filename == '':
        return 'No image selected', 400

    quantity = request.form.get('quantity', '1')
    kilogram = request.form.get('kilogram', '0')

    os.makedirs('static', exist_ok=True)
    filename = os.path.basename(img_file.filename)
    save_path = os.path.join('static', filename)
    img_file.save(save_path)

    # --- Image Preprocessing ---
    img = image.load_img(save_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # --- Prediction ---
    predictions = model.predict(img_array)
    pred_index = int(np.argmax(predictions, axis=1)[0])

    # --- Correct Mapping from Class Index ---
    predicted_class = CLASS_NAMES[pred_index] if 0 <= pred_index < len(CLASS_NAMES) else "Unknown"

    # --- Normalize name (safety) ---
    predicted_class = predicted_class.strip().title()

    # --- Fetch Fish Info ---
    fish_info = FISH_INFO.get(predicted_class, {
        'scientific_name': 'Not available',
        'habitat': 'Not available',
        'description': 'Information not available.'
    })

    # --- Save Record ---
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO records (species, quantity, kilogram, date, image) VALUES (?, ?, ?, ?, ?)",
              (predicted_class, quantity, kilogram, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename))
    conn.commit()
    conn.close()

    return render_template('result.html',
                           species=predicted_class,
                           image_name=filename,
                           quantity=quantity,
                           kilogram=kilogram,
                           scientific_name=fish_info['scientific_name'],
                           habitat=fish_info['habitat'],
                           description=fish_info['description'])

# --- RECORDS PAGE ---
@app.route('/records')
def records():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM records ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template('records.html', records=rows)

# --- MAIN ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
