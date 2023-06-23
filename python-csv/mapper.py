import pandas as pd
from difflib import get_close_matches
import numpy as np

# Словарь с образцовыми названиями столбцов
sample_columns = {
    "firstName": None,
    "lastName": None,
    "dateOfBirth": None,
    "gender": None,
    "email": None,
    "phone": None,
    "maritalStatus": None,
    "income": None,
    "interests": None,
    "languages": None,
    "religionViews": None,
    "politicalViews": None,
    "mobilePhone": None,
    "address": None,
    "linkedAccounts": None,
    "website": None,
    "placeOfWork": None,
    "skills": None,
    "university": None,
    "faculty": None,
    "currentCity": None,
    "birthPlace": None,
    "otherCities": None,
    "breifDescription": None,
    "hobby": None,
    "sport": None,
    "operatingSystem": None,
    "displayResolution": None,
    "browser": None,
    "iSP": None,
    "adBlock": None,
    "sessionState": None,
    "language": None,
    "region": None,
    "recentPages": None,
    "productId": None,
    "productName": None,
    "productPrice": None,
    "quantity": None,
    "subTotal": None,
    "total": None,
    "couponCode": None,
    "shippingInformation": None,
    "taxInformation": None
}

def find_matching_column(column, df_columns):
    # Ищем наиболее похожее название столбца в df_columns с использованием get_close_matches
    matches = get_close_matches(column, df_columns)
    if matches:
        return matches[0]
    return None

def process_csv_files(csv_file):
    df = pd.read_csv(csv_file)
    df.replace('', None, inplace=True)
    df.replace(np.nan, None, inplace=True)
    output_df = pd.DataFrame(columns=sample_columns.keys())

    for column in sample_columns:
        if column == "faculty":
            output_df[column] = None
        elif column == "address":
            address_parts = ['city', 'county', 'state', 'zip']
            if all(part in df.columns for part in address_parts):
                output_df[column] = df[address_parts].apply(lambda x: '; '.join(x.dropna().astype(str)), axis=1)
            else:
                output_df[column] = None
        elif column == "phone":
            if "phone1" in df.columns and "phone2" in df.columns:
                output_df[column] = df[["phone1", "phone2"]].apply(lambda x: '; '.join(x.dropna().astype(str)), axis=1)
            else:
                output_df[column] = None
        elif column in df.columns:
            output_df[column] = df[column]
        else:
            matching_column = find_matching_column(column, df.columns)
            if matching_column:
                output_df[column] = df[matching_column]

    print(f"Обработка файла завершена.")
    return output_df