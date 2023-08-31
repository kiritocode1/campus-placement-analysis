import pandas as pd
import os
import pickle
from uuid import uuid4
import traceback
# Prepared data in the format required by deployed model


def transform_placed_prediction(df):
    transformed_data = []
    placed = ['tier', 'cgpa', 'inter_gpa', 'ssc_gpa', 'internships', 'no_of_projects', 'is_participate_hackathon', 'is_participated_extracurricular',
              'no_of_programming_languages', 'dsa', 'mobile_dev', 'web_dev', 'Machine Learning', 'cloud', 'CSE', 'ECE', 'IT', 'MECH']
    for index, row in df.iterrows():
        row_values = []
        for column in placed:
            if(column != 'CSE' and column != 'IT' and column != 'MECH' and column != 'ECE'):
                row_values.append(float(row[column]))

        # Check the branch value and fill the corresponding columns
        if row[4] == "CSE":
            row_values.insert(14, 1)
            row_values.insert(15, 0)
            row_values.insert(16, 0)
            row_values.insert(17, 0)
        elif row[4] == 'ECE':
            row_values.insert(14, 0)
            row_values.insert(15, 1)
            row_values.insert(16, 0)
            row_values.insert(17, 0)
        elif row[4] == 'IT':
            row_values.insert(14, 0)
            row_values.insert(15, 0)
            row_values.insert(16, 1)
            row_values.insert(17, 0)
        elif row[4] == 'MECH':
            row_values.insert(14, 0)
            row_values.insert(15, 0)
            row_values.insert(16, 0)
            row_values.insert(17, 1)
        else:
            row_values.insert(14, 0)
            row_values.insert(15, 0)
            row_values.insert(16, 0)
            row_values.insert(17, 0)
        transformed_data.append(row_values)
    return transformed_data


# Prepared data in the format required by deployed model
def transform_salary_prediction(df):
    transformed_data = []
    salary = ['tier', 'cgpa', 'internships', 'no_of_projects', 'is_participate_hackathon', 'is_participated_extracurricular',
              'no_of_programming_languages', 'dsa', 'mobile_dev', 'web_dev', 'Machine Learning', 'cloud', 'CSE', 'ECE', 'IT', 'MECH']
    for index, row in df.iterrows():
        row_values = []
        for column in salary:
            if(column != 'CSE' and column != 'IT' and column != 'MECH' and column != 'ECE'):
                row_values.append(float(row[column]))

        # Check the branch value and fill the corresponding columns
        if row[4] == "CSE":
            row_values.insert(14, 1)
            row_values.insert(15, 0)
            row_values.insert(16, 0)
            row_values.insert(17, 0)
        elif row[4] == 'ECE':
            row_values.insert(14, 0)
            row_values.insert(15, 1)
            row_values.insert(16, 0)
            row_values.insert(17, 0)
        elif row[4] == 'IT':
            row_values.insert(14, 0)
            row_values.insert(15, 0)
            row_values.insert(16, 1)
            row_values.insert(17, 0)
        elif row[4] == 'MECH':
            row_values.insert(14, 0)
            row_values.insert(15, 0)
            row_values.insert(16, 0)
            row_values.insert(17, 1)
        else:
            row_values.insert(14, 0)
            row_values.insert(15, 0)
            row_values.insert(16, 0)
            row_values.insert(17, 0)
        transformed_data.append(row_values)
    return transformed_data


def load_pickle_models():
    salary_model_path = os.path.join(
        os.path.dirname(__file__), 'models', 'sal_model.pkl')
    placed_model_path = os.path.join(os.path.dirname(
        __file__), 'models', 'Placed_model.pkl')

    salary_model = pickle.load(open(salary_model_path, 'rb'))
    is_placed_model = pickle.load(open(placed_model_path, 'rb'))

    return is_placed_model, salary_model


def save_df_to_temp(df):
    unique_id = str(uuid4())
    temp_file_url_path = os.path.join(
        os.path.dirname(__file__), '..', 'static', 'temp', unique_id+'.csv')

    df.to_csv(temp_file_url_path, index=True)

    return '/temp/'+unique_id+'.csv'


def convert_is_placed_to_zero_ifnot_placed(is_placed, salary):

    for i in range(len(is_placed)):
        if is_placed[i] == 0:
            salary[i] = 0

    return salary


def check_columns_and_datatypes(excel_file):
    expected_columns = [
        "s_id", "name", "tier", "gender", "branch", "cgpa", "inter_gpa",
        "ssc_gpa", "internships", "no_of_projects", "is_participate_hackathon",
        "is_participated_extracurricular", "no_of_programming_languages",
        "dsa", "mobile_dev", "web_dev", "Machine Learning", "cloud", "other_skills"
    ]
    expected_datatypes = {
        "s_id": int, "name": str, "tier": int, "gender": str, "branch": str,
        "cgpa": float, "inter_gpa": float, "ssc_gpa": float, "internships": int,
        "no_of_projects": int, "is_participate_hackathon": int,
        "is_participated_extracurricular": int, "no_of_programming_languages": int,
        "dsa": int, "mobile_dev": int, "web_dev": int, "Machine Learning": int,
        "cloud": int, "other_skills": str
    }
    try:
        if excel_file.filename.endswith(".xlsx"):
            df = pd.read_excel(excel_file)
        elif excel_file.filename.endswith(".csv"):
            df = pd.read_csv(excel_file)
        else:
            return False
        if set(expected_columns) != set(df.columns):
            return False

        for column, datatype in expected_datatypes.items():
            if column in df.columns and df[column].dtype != datatype:
                df[column] = df[column].astype(datatype)

        return True
    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return False
