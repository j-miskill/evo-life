from datetime import datetime


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
        """
        pass
            
        

    






    