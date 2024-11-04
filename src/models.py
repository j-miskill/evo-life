from datetime import datetime


class Gene:
    """
        This is the bottom layer of our abstraction. 

        The gene will be a class that contains simple numerical data on the various aspects of someones health
        we wish to capture. 

        the gene will hold data for a single day in time. 

        the gene will be linked to a unique id that is linked to a specific person
    
    """

    def __init__(self, steps: int, avg_intensity: int, sleep:int, heart_rate:float, met:float, date:datetime, id):
        self.steps = steps
        self.avg_intensity = avg_intensity
        self.sleep = sleep
        self.heart_rate = heart_rate
        self.met = met
        self.date = date
        self.id = id



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
        try:
            return self.geneset[day]
        except Exception as e:
            print("Geneset does not include: ", day, ". Please request a valid day.")

    def evaluate_phenotype(self):
        """
            perhaps here is where we could evaluate the genotype and calculate what the phenotype would look
            like, depending on what we deemed to be interesting enough for us to look at.
        """
        pass
            
        

    






    