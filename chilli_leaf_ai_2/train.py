import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def main():
    print("=========================================")
    print("Chilli Leaf Disease Model Training")
    print("=========================================")

    # Configuration
    IMG_SIZE = (224, 224)
    BATCH_SIZE = 32
    EPOCHS = 20
    DATA_DIR = 'data/train'
    MODEL_DIR = 'models'
    MODEL_PATH = os.path.join(MODEL_DIR, 'chilli_model.h5')

    # Ensure directories exist
    os.makedirs(MODEL_DIR, exist_ok=True)
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Data directory '{DATA_DIR}' not found. Please add images per category.")
        return

    # 1. Data Handling with validation split 80/20
    print("[INFO] Loading and augmenting data...")
    datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=0.2,
        rotation_range=30,
        zoom_range=0.3,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2]
    )

    train_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    valid_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    if train_generator.samples == 0:
        print("[ERROR] No training images found in 'data/train/*'. Please add images first.")
        return

    # 2. Model Architecture (Transfer Learning)
    print("[INFO] Building model (MobileNetV2)...")
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze base model layers initially
    base_model.trainable = False
    
    # Unfreeze top layers for fine-tuning
    for layer in base_model.layers[-30:]:
        layer.trainable = True

    # Add custom classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(5, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    # 3. Compile Model with lower learning rate for fine-tuning
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    print(model.summary())

    # 4. Callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1),
        ModelCheckpoint(filepath=MODEL_PATH, monitor='val_accuracy', save_best_only=True, verbose=1)
    ]

    # 5. Training
    print("[INFO] Starting training...")
    history = model.fit(
        train_generator,
        validation_data=valid_generator,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    print(f"\n[INFO] Training complete. Best model saved to {MODEL_PATH}")

if __name__ == '__main__':
    main()
