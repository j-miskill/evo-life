from models import Genome, Gene
import pandas as pd
import numpy as np
import os

"""
    File of helper functions
"""

class GenomeCreator:

    def __init__(self):
        self.instance = True
        self.df = None
        self.num_columns = None
        self.ids = []

    def load_data_from_csv(self, path=None):
        """
            Input: string path to csv file

            Output: a dataframe instantiated from that csv file
        """
        if not path:
            current_script_path = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_script_path)
            path = os.path.join(current_dir, '../prepped/daily.csv')
            path = os.path.normpath(path)


        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            print("Please pass in the correct path for the data to be read in from")
            print("You passed in:", path)
            raise FileNotFoundError
        
        df = df.drop("Unnamed: 0", axis=1)
        cs = self.check_schema(df)
        if not cs:
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
        
        for c in cols:
            if c not in valid_cols:
                print("failed on", c)
                return False
            
        if len(cols) != len(valid_cols):
            print(cols)
            return False

        return True

    def load_data_from_table(self):
        pass

    def create_genes_for_individual(self, id_records:pd.DataFrame):
        """
            Purpose: create a Gene for this individual's day

            Input: dataframe of records for a specific ID

            Output: a list of genes!

            Fields for Gene model:
                id day nremhr rmssd spo2 stress_score sleep_points_percentage 
                exertion_points_percentage responsiveness_points_percentage 
                distance activityType bpm lightly_active_minutes moderately_active_minutes 
                very_active_minutes sedentary_minutes mindfulness_session sleep_duration 
                minutesAsleep minutesAwake sleep_efficiency gender bmi TENSE/ANXIOUS TIRED 
                GYM HOME OUTDOORS
        """

        id_records = id_records.sort_values(by='day')
        geneset = []

        for i, r in id_records.iterrows():
            tmp_g = Gene(id=r['id'], day=r['day'], nremhr = r['nremhr'], rmssd = r['rmssd'],
                         spo2 = r['spo2'], stress_score = r['stress_score'], sleep_points_percentage = r['sleep_points_percentage'],
                         exertion_points_percentage = r['exertion_points_percentage'], responsiveness_points_percentage = r['responsiveness_points_percentage'],
                         distance = r['distance'], activityType = r['activityType'], bpm = r['bpm'], lightly_active_minutes = r['lightly_active_minutes'],
                         moderately_active_minutes = r['moderately_active_minutes'], very_active_minutes = r['very_active_minutes'],
                         sedentary_minutes = r['sedentary_minutes'], mindfulness_session = r['mindfulness_session'], sleep_duration = r['sleep_duration'],
                         minutesAsleep = r['minutesAsleep'], minutesAwake = r['minutesAwake'], sleep_efficiency = r['sleep_efficiency'],
                         gender = r['gender'], bmi = r['bmi'], tense = r['TENSE/ANXIOUS'], tired = r['TIRED'],
                          gym = r['GYM'], home = r['HOME'], outdoors = r['OUTDOORS'])
            
            geneset.append(tmp_g)

    def create_genome_for_individual(self, id):
        if self.determine_quality_individual(id=id, quality=0.3):
            id_records = self.df.loc[self.df['id'] == f'{id}']
            genes = self.create_genes_for_individual(id_records)
            g = Genome(geneset=genes, id=id)
            return g

    def create_all_genomes(self):
        genomes = {}
        for id in self.ids:
            if self.determine_quality_individual(id=id, quality=0.3):
                g = self.create_genome_for_individual(id=id)
                genomes['id'] = g
           


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


