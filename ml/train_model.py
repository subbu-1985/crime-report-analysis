"""import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GlobalAveragePooling1D, Dense
from tensorflow.keras.utils import to_categorical

# Example: Load your labeled data (replace with your real dataset)
# DataFrame should have columns: 'text', 'label'
data = pd.DataFrame({
    "text": [
        "Stolen bike reported in Guntur",
        "Domestic violence in Vijayawada",
        "Land dispute in Nellore",
        "ATM fraud in Krishna",
        "Assault near railway station"
    ],
    "label": [
        "Theft",
        "Domestic Violence",
        "Land Dispute",
        "Financial Crime",
        "Assault"
    ]
})

# Encode labels
le = LabelEncoder()
data['label_enc'] = le.fit_transform(data['label'])
num_classes = len(le.classes_)

# Tokenize text
tokenizer = Tokenizer(num_words=1000, oov_token="<OOV>")
tokenizer.fit_on_texts(data['text'])
sequences = tokenizer.texts_to_sequences(data['text'])
X = pad_sequences(sequences, maxlen=20)
y = to_categorical(data['label_enc'], num_classes=num_classes)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build model
model = Sequential([
    Embedding(input_dim=1000, output_dim=16, input_length=20),
    GlobalAveragePooling1D(),
    Dense(32, activation='relu'),
    Dense(num_classes, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# Train
model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))

# Save model
model.save("crime_classifier.h5")

# Save tokenizer and label encoder for inference (optional)
import pickle
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)"""
    
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import logging
from datetime import datetime
from utils.data_loader import load_crime_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrimeClassifierTrainer:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.feature_columns = [
            'hour_of_day', 'day_of_week', 'district_encoded',
            'latitude', 'longitude', 'population_density'          

        ]
        self.target_column = 'crime_type'
        
    def load_and_preprocess_data(self):
        """Load and preprocess crime data"""
        logger.info("Loading and preprocessing data...")
        df = load_crime_data()
        
        # Encode categorical features
        df['district_encoded'] = self.label_encoder.fit_transform(df['district'])
        df['hour_of_day'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Handle missing values
        df['population_density'] = df['population_density'].fillna(df['population_density'].median())
        
        return df

    def create_model(self, num_classes):
        """Create neural network model"""
        model = Sequential([
            Dense(128, activation='relu', input_shape=(len(self.feature_columns),)),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dropout(0.2),
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def train(self):
        """Train the crime classification model"""
        try:
            df = self.load_and_preprocess_data()
            
            # Split data
            X = df[self.feature_columns]
            y = self.label_encoder.transform(df[self.target_column])
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Create and train model
            self.model = self.create_model(len(self.label_encoder.classes_))
            
            early_stop = EarlyStopping(monitor='val_loss', patience=5)
            
            logger.info("Training model...")
            history = self.model.fit(
                X_train, y_train,
                validation_data=(X_test, y_test),
                epochs=50,
                batch_size=32,
                callbacks=[early_stop],
                verbose=1
            )
            
            # Save model and artifacts
            self.save_model()
            logger.info("Training completed successfully")
            
            return history
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise

    def save_model(self):
        """Save model and preprocessing artifacts"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = f"ml/crime_classifier_{timestamp}.h5"
        encoder_path = "ml/label_encoder.pkl"
        
        self.model.save(model_path)
        joblib.dump(self.label_encoder, encoder_path)
        
        # Update symlink to latest model
        import os
        if os.path.exists("ml/crime_classifier.h5"):
            os.remove("ml/crime_classifier.h5")
        os.symlink(f"crime_classifier_{timestamp}.h5", "ml/crime_classifier.h5")

if __name__ == "__main__":
    trainer = CrimeClassifierTrainer()
    trainer.train()