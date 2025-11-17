# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import os

# # Dataset Path
# dataset_path = "dataset/"

# # Data Augmentation
# train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
# train_generator = train_datagen.flow_from_directory(
#     dataset_path + "train", target_size=(48, 48), batch_size=64, color_mode="grayscale", class_mode="categorical", subset="training")
# val_generator = train_datagen.flow_from_directory(
#     dataset_path + "train", target_size=(48, 48), batch_size=64, color_mode="grayscale", class_mode="categorical", subset="validation")

# # CNN Model
# model = Sequential([
#     Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
#     MaxPooling2D(2, 2),
#     Conv2D(64, (3, 3), activation='relu'),
#     MaxPooling2D(2, 2),
#     Flatten(),
#     Dense(128, activation='relu'),
#     Dropout(0.5),
#     Dense(7, activation='softmax')  # 7 Emotions
# ])

# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# # Train Model
# model.fit(train_generator, validation_data=val_generator, epochs=20)

# # Save Model
# model.save("model/emotion_model.h5")
# print("Model trained and saved as emotion_model.h5")


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Dataset Path
dataset_path = "dataset/train"

# Ensure model directory exists
os.makedirs("model", exist_ok=True)

# Data Augmentation
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode="categorical",
    subset="training"
)

val_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(48, 48),
    batch_size=64,
    color_mode="grayscale",
    class_mode="categorical",
    subset="validation"
)

# CNN Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    
    Conv2D(128, (3, 3), activation='relu'),  # Extra layer added
    MaxPooling2D(2, 2),
    
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')  # 7 Emotion categories
])

# Compile Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train Model
model.fit(train_generator, validation_data=val_generator, epochs=20)

# Save Model
model.save("model/emotion_model.h5")
print("Model trained and saved as model/emotion_model.h5")
