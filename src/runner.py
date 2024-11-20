"""
    Source file to run all of the code from the other two files. 
"""


#######################
# COMMON FUNCTIONS #
#######################

def get_data():
    data = None
    return data

def encode_data(data, **kwargs):
    print("Encoding health metrics...")
    encoded_data = None
    return encoded_data

def decode_data(encodings, **kwargs):
    print("Decoding predictions into human-readable format...")
    ti = kwargs['ti']
    predictions = ti.xcom_pull(task_ids='predict_phenotype')
    decoded_results = None
    return decoded_results


#######################
# TRAINING FUNCTIONS #
#######################


def store_trained_model():
    print("Storing the pre-trained CBM model...")
    model = None
    return model


#######################
# INFERENCE FUNCTIONS #
#######################

def load_trained_model(**kwargs):
    print("Loading the pre-trained CBM model...")
    model = None
    return model

def predict_phenotype(**kwargs):
    print("Running predictions using the model...")
    ti = kwargs['ti']
    model = ti.xcom_pull(task_ids='load_trained_model')
    encoded_data = ti.xcom_pull(task_ids='encode_gene')
    predictions = f"Predictions_based_on_{model}_and_{encoded_data}"
    return predictions

def update_database(**kwargs):
    print("Updating the database with predictions...")
    ti = kwargs['ti']
    decoded_results = ti.xcom_pull(task_ids='decode_phenotype')
    print(f"Updated database with: {decoded_results}")

def display_results(**kwargs):
    print("Triggering UI update with results...")
    ti = kwargs['ti']
    decoded_results = ti.xcom_pull(task_ids='decode_phenotype')
    print(f"Displayed results on UI: {decoded_results}")