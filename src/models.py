from datetime import datetime
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class Gene:
    """
        This is the bottom layer of our abstraction. 

        The gene will be a class that contains simple numerical data on the various aspects of someones health
        we wish to capture. 

        the gene will hold data for a single day in time. 

        the gene will be linked to a unique id that is linked to a specific person

        id date nremhr rmssd spo2 stress_score sleep_points_percentage 
        exertion_points_percentage responsiveness_points_percentage 
        distance activityType bpm lightly_active_minutes moderately_active_minutes 
        very_active_minutes sedentary_minutes mindfulness_session sleep_duration 
        minutesAsleep minutesAwake sleep_efficiency gender bmi TENSE/ANXIOUS TIRED 
        GYM HOME OUTDOORS day

    """

    def __init__(self, id:int, day:int, nremhr:float, rmssd:float, spo2:float, stress_score:float,
                 sleep_points_percentage:float, exertion_points_percentage:float, 
                 responsiveness_points_percentage:float, distance:float, activityType:str,
                 bpm:float, lightly_active_minutes:float, moderately_active_minutes:float,
                 very_active_minutes:float, sedentary_minutes:float, mindfulness_session:bool,
                 sleep_duration:float, minutesAsleep:float, minutesAwake:float, sleep_efficiency:float,
                 gender:str, bmi:float, tense:bool, tired:bool, gym: bool, home: bool, outdoors:bool):
        self.id = id
        self.day = day
        self.nremhr = nremhr
        self.rmssd = rmssd
        self.spo2 = spo2
        self.stress_score = stress_score
        self.sleep_points_percentage = sleep_points_percentage
        self.exertion_points_percentage = exertion_points_percentage
        self.responsiveness_points_percentage = responsiveness_points_percentage
        self.distance = distance
        self.activityType = activityType
        self.bpm = bpm
        self.lightly_active_minutes = lightly_active_minutes
        self.moderately_active_minutes = moderately_active_minutes
        self.very_active_minutes = very_active_minutes
        self.sedentary_mintes = sedentary_minutes
        self.mindfulness_session = mindfulness_session
        self.sleep_duration = sleep_duration
        self.minutesAsleep = minutesAsleep
        self.minutesAwake = minutesAwake
        self.sleep_efficiency = sleep_efficiency
        self.gender = gender
        self.bmi = bmi
        self.tense = tense
        self.tired = tired
        self.gym = gym
        self.home = home
        self.outdoors = outdoors


class Genome:

    """
        The Chromosome is the second layer of abstraction. A chromosome will roughly compose a set of genes.

        It will be a set of days linked to a unique person.

        Also, it's going to be a list, where the index of that list is a specific day that we are looking at.
    """

    def __init__(self, geneset: list[Gene], id):
        self.geneset = geneset
        self.id = id

    def find_day(self, day:int)-> Gene:
        for g in self.geneset:
            if g.day == day:
                return self.geneset[day]
        print("Geneset does not include: ", day, ". Please request a valid day.")

    def calculate_phenotype(self):
        """
            perhaps here is where we could evaluate the genotype and calculate what the phenotype would look
            like, depending on what we deemed to be interesting enough for us to look at.

            Currently uses genes to train the model and then predicts if a day will be tense or not
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
        genes = self.geneset
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

            
        

    






    