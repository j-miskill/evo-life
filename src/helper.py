from models import Genome, Gene
import pandas as pd
import numpy as np
"""
    File of helper functions

    was thinking:
    - read in the data
    - create instances of genes
    - create instances of genomes
    - evaluate more than one person
    - data cleaning and handling
"""

class GenomeCreator:

    def __init__(self):
        self.instance = True
        self.df = None
        self.num_columns = None
        self.ids = []

    def load_data_from_csv(self, path):
        """
            Input: string path to csv file

            Output: a dataframe instantiated from that csv file
        """
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            print("Please pass in the correct path for the data to be read in from")
            print("You passed in:", path)
            raise FileNotFoundError
        
        if not self.check_schema(df):
            raise Exception("please ensure the schema of the table is correct")
        
        self.num_columns = len(df.columns)
        self.df = df
        ids = list(df['id'].unique())
        self.ids = ids
    
    def check_schema(self, df):
        valid_cols = ['id','date', 'nremhr', 'rmssd','spo2', 'stress_score', 'sleep_points_percentage', 'exertion_points_percentage',
                      'responsiveness_points_percentage', 'distance', 'activityType', 'bpm', 'lightly_active_minutes', 'moderately_active_minutes',
                      'very_active_minutes', 'sedentary_minutes', 'mindfulness_session', 'sleep_duration', 'minutesAsleep', 'minutesAwake', 'sleep_efficiency',
                      'gender', 'bmi', 'TENSE/ANXIOUS', 'TIRED', 'GYM', 'HOME', 'OUTDOORS', 'day']
        
        cols = df.columns
        if len(cols) != len(valid_cols):
            return False

        for c in cols:
            if c not in valid_cols:
                return False

        return True

    def load_data_from_table(self):
        pass

    def create_genes_for_individual(self, id):
        pass

    def create_genome_for_individual(self, id):
        
        id_records = self.df.loc[self.df['id'] == f'{id}']


        pass

    def create_all_genomes(self):
        for id in self.ids:
            if self.determine_quality_individual(id=id, quality=0.3):
                self.create_genome_for_individual(id=id)
           


    def determine_quality_individual(self, id, quality: float):
        """
            Purpose: determine whether or not an ID has enough quality data associated with it

            Input: a single ID

            Output: true or false

            Notes: 
                - quality is when they have > 60% of their columns not 0
                - zeroes could be valid, like it could be a boolean value
                - typically try to have the quality around 30% (?)
                 

        """
        if quality > 1.0:
            raise Exception("quality parameter should be a number from 0 to 1.0")

        valid_columns = ['nremhr', "rmssd", "spo2", "stress_score", "sleep_points_percentage", "exertion_points_percentage",
                         "responsiveness_points_percentage","distance", "bpm", "lightly_active_minutes", "moderately_active_minutes",
                         "very_active_minutes", "sedentary_minutes", "sleep_duration", 	"minutesAsleep", "minutesAwake",
                         "sleep_efficiency", "bmi"]
        id_records = self.df.loc[self.df['id'] == "621e32e667b776a2406d2f1c"].reset_index()
        total_cols = len(valid_columns)
        df_subset = id_records[["id", "date"] + valid_columns]
        total_num_records = df_subset['id'].count()
        base = total_cols * total_num_records
        total_zero_count = df_subset.apply(lambda row: (row == 0).sum(), axis=1)
        num_zeros_across_all_cols_for_id = total_zero_count.sum()

        validity_pct =  num_zeros_across_all_cols_for_id / base

        # we want the percentage of zeros to be less than the quality check percentage
        # ie, if we want the number of 0s to be less than 60% of total cols
        if validity_pct < quality:
            return True
        else:
            return False







        


class TableInteractor:

    def __init__(self):
        pass

    def read_to_table(self):
        pass

    def write_to_table(self):
        pass


