import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from models import Gene

class Phenotype:
    def __init__(self):
        self.model = None
        self.individuals = None
    
    def create_and_train_nn_model(self, genes:list[Gene]):
        """
            Creates the neural network for predicting if a day is tense or not
            Returns a 0.0 or 1.0 for False/True for each gene in list genes
            TODO: May want to change it to take in multiple days and have a sum/percent of days person is anxious in week/month
        """
        def preprocess_data(genes):
            # Convert Gene objects to numerical data
            features = []
            labels = []
            for gene in genes:
                feature = [
                    gene.nremhr,
                    gene.rmssd,
                    gene.spo2,
                    gene.stress_score,
                    gene.sleep_points_percentage,
                    gene.exertion_points_percentage,
                    gene.responsiveness_points_percentage,
                    gene.distance,
                    gene.bpm,
                    gene.lightly_active_minutes,
                    gene.moderately_active_minutes,
                    gene.very_active_minutes,
                    gene.sedentary_mintes,
                    gene.mindfulness_session,
                    gene.sleep_duration,
                    gene.minutesAsleep,
                    gene.minutesAwake,
                    gene.sleep_efficiency,
                    gene.gender,
                    gene.bmi,
                    gene.tired,
                    gene.gym,
                    gene.home,
                    gene.outdoors
                ]
                features.append(feature)
                labels.append(gene.tense)
            
            return np.array(features), np.array(labels)

        # Example: Assuming `genes` is your list of Gene objects
        features, labels = preprocess_data(genes)

        # Normalize the features
        scaler = StandardScaler()
        features = scaler.fit_transform(features)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

        # Build the neural network
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        # Train the model
        model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

        # Evaluate the model
        loss, accuracy = model.evaluate(X_test, y_test)
        print(f"Test Accuracy: {accuracy:.2f}")

        predictions = model.predict(features)

        # Interpret the predictions
        # Since the model outputs probabilities for binary classification, round them to 0 or 1
        predicted_tense = (predictions > 0.5).astype(int)  # 0.5 is the threshold
        self.model = model
        return predicted_tense