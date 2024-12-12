from datetime import datetime
import numpy as np
from sklearn.calibration import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder


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

        self.encoding = []

    def create_encoding(self):
        """
           1. take all fields and create a binary string 0101010101010101010100101010101110010101010101 
           2. real value numbers [] 

           sklearn.preprocessing for string mapping
           ordinal encoder, label encoder

        """
        le = LabelEncoder()

        gene_attributes = [a for a in vars(self) if not a.startswith("__")]

        g_to_list = []

        for ga in gene_attributes:
            if ga == "id" or ga == "create_encoding" or ga == "activityType":
                continue
            else:
                value = self.__getattribute__(ga)
                if ga == "bmi":
                    value = value.replace(">", "")
                    value = value.replace(">=", "")
                if ga == "gender":
                    if value == "MALE":
                        value = 1
                    else:
                        value = 0
                if type(value) == str and not value.isnumeric():
                    continue

                if type(value) == str or type(value) == int or type(value) == float:
                
                    g_to_list.append(int(value))

        le.fit(g_to_list)
        encoding = le.transform(g_to_list)
        return encoding


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


    def create_encoding(self):
        """
           1. take all fields and create a binary string 0101010101010101010100101010101110010101010101 
           2. real value numbers [] 

           sklearn.preprocessing for string mapping
           ordinal encoder, label encoder

        """
        le = LabelEncoder()

        gene_attributes = [a for a in vars(self) if not a.startswith("__")]

        g_to_list = []

        for ga in gene_attributes:
            if ga == "id" or ga == "create_encoding" or ga == "activityType":
                continue
            else:
                value = self.__getattribute__(ga)
                if ga == "bmi":
                    value = value.replace(">", "")
                    value = value.replace(">=", "")
                if ga == "gender":
                    if value == "MALE":
                        value = 1
                    else:
                        value = 0
                if type(value) == str and not value.isnumeric():
                    continue

                if type(value) == str or type(value) == int or type(value) == float:
                
                    g_to_list.append(int(value))

        le.fit(g_to_list)
        encoding = le.transform(g_to_list)
        return encoding

    def calculate_genome_phenotype(self, anxiety:list, tired:list, stress_score:list, sleep_point_percent:list, prev_phenotype=None, prev_phenotype_period=None):
        """
           entire collection of data we have on a person

           --BMI
           ANXIOUS
           TIRED


           (
           % of days ANXIOUS == 1
           % of days TIRED == 1
           change in stress_score 
           change in sleep_points_percentage )
           |
           |
           BB
           |
           |
           *
           one continuous value

           phenotype: (0,1) for one ID for the data we have now
                        1 good
                        0 bad

           |
           |
           |
           |
           *

           say we add another month of data for an ID

           then, we recalculate the phenotype


        
        """
        # Ensure the first value is greater than 0.0\
        if len(stress_score) > 0:
            stress_score_begin = stress_score[0]
            while stress_score_begin <= 0.0 and len(stress_score) != 0:
                stress_score = stress_score[1:]
                if len(stress_score) == 0:
                    break
                stress_score_begin = stress_score[0]

            # Ensure the last value is greater than 0.0
        if len(stress_score) > 0:
            stress_score_end = stress_score[-1]
            while stress_score_end <= 0.0 and len(stress_score) != 0:
                stress_score = stress_score[:-1]
                if len(stress_score) == 0:
                    break
                stress_score_end = stress_score[-1]
                
            

        if len(sleep_point_percent) > 0:
        # Ensure the first value is greater than 0.0
            sleep_point_percent_begin = sleep_point_percent[0]
            while sleep_point_percent_begin <= 0.0 and len(sleep_point_percent) != 0:
                sleep_point_percent = sleep_point_percent[1:]
                if len(sleep_point_percent) == 0:
                    break
                sleep_point_percent_begin = sleep_point_percent[0]
                
        if len(sleep_point_percent) > 0:
            # Ensure the last value is greater than 0.0
            sleep_point_percent_end = sleep_point_percent[-1]
            while sleep_point_percent_end <= 0.0 and len(sleep_point_percent) != 0:
                sleep_point_percent = sleep_point_percent[:-1]
                if len(sleep_point_percent) == 0:
                    break
                sleep_point_percent_end = sleep_point_percent[-1]
                
            

        if stress_score_begin > 0.0 and stress_score_end > 0.0:
            stress_score_change = (stress_score_end - stress_score_begin) / stress_score_begin
        else:
            stress_score_change = 0.0
        if sleep_point_percent_begin > 0.0 and sleep_point_percent_end > 0.0:
            sleep_point_change = (sleep_point_percent_end - sleep_point_percent_begin) / sleep_point_percent_begin        
        else:
            sleep_point_change = 0.0
        
        anxiety_average = np.average(anxiety)
        tired_average = np.average(tired)


        # Normalize metrics
        normalized_stress_score_change = (1 + stress_score_change) / 2  # Ensures values are between 0 and 1
        normalized_sleep_point_change = (sleep_point_change + 1) / 2   # Ensures values are between 0 and 1
        normalized_anxiety = 1 - anxiety_average  # Invert because low anxiety is good
        normalized_tired = 1 - tired_average      # Invert because low tiredness is good

        # Combine into phenotype score
        phenotype = (normalized_stress_score_change +
                    normalized_sleep_point_change +
                    normalized_anxiety +
                    normalized_tired) / 4
        
        return phenotype

    def calculate_genome_phenotype_split(self, date:list, anxiety:list, tired:list, stress_score:list, sleep_point_percent:list, prev_phenotype=None):
        def split_into_parts(data, parts=4):
            """
            Splits a list into the specified number of equal parts.
            If the list is not evenly divisible, some parts may differ slightly in size.
            
            Args:
                data (list): The list to split.
                parts (int): The number of parts to divide the list into.
            
            Returns:
                list: A list of sublists.
            """
            # Calculate the approximate size of each part
            avg_length = len(data) / parts
            month_splits = [datetime.strptime(day, "%Y-%m-%d").strftime("%B") for day in date]
            split_data = []
            last_index = 0
            ret_data = {}
            months_in_order = []
            for d in month_splits:
                if d not in ret_data.keys():
                    ret_data[d] = []
                    months_in_order.append(d)
            for i in range(len(month_splits)):
                # Calculate the start and end indices for this part
                ret_data[month_splits[i]].append(data[i])
            
            for m in months_in_order:
                split_data.append(ret_data[m])
            return split_data, months_in_order
        
        anxiety_split, months_in_order = split_into_parts(anxiety)
        tired_split, _ = split_into_parts(tired)
        stress_score_split, _ = split_into_parts(stress_score)
        sleep_point_percent_split, _ = split_into_parts(sleep_point_percent)

        phenotype_scores = []
        for i in range(len(anxiety_split)):
            phenotype_score = self.calculate_genome_phenotype(
                anxiety_split[i],
                tired_split[i],
                stress_score_split[i],
                sleep_point_percent_split[i]
            )
            phenotype_scores.append(phenotype_score)
        return (phenotype_scores, months_in_order)


    # def calculate_gene_phenotype(self):
    #     """
    #         Day to day phenotype calculation

    #         ANXIOUS
    #         TIRED

    #         % of days that you were anxious
    #         % of days that you were tired


    #     """
    #     pass
            
        

    






    