import pandas as pd
import glob
import os
from difflib import get_close_matches

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

def process_csv_files(csv_files):
    # Получаем список CSV-файлов в указанной директории
    # csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    for csv_file in csv_files:
        # Считываем входной CSV-файл
        df = pd.read_csv(csv_file)

        # Создаем новую таблицу с образцовыми названиями столбцов
        output_df = pd.DataFrame(columns=sample_columns.keys())

        for column in sample_columns:
            if column == "faculty":
                output_df[column] = "null"
            elif column == "address":
                # Создаем столбец "address" путем объединения значений столбцов "city", "county", "state" и "zip"
                address_parts = ['city', 'county', 'state', 'zip']
                if all(part in df.columns for part in address_parts):
                    output_df[column] = df[address_parts].apply(lambda x: '; '.join(x.dropna().astype(str)), axis=1)
                else:
                    output_df[column] = "null"
            elif column == "phone":
                if "phone1" in df.columns and "phone2" in df.columns:
                    # Объединяем значения столбцов "phone1" и "phone2" через запятую
                    output_df[column] = df[["phone1", "phone2"]].apply(lambda x: '; '.join(x.dropna().astype(str)), axis=1)
                else:
                    output_df[column] = "null"
            elif column in df.columns:
                # Если столбец есть в CSV-файле, копируем его значения
                output_df[column] = df[column]
            else:
                # Если столбец отсутствует в CSV-файле, ищем наиболее похожее название столбца и копируем его значения
                matching_column = find_matching_column(column, df.columns)
                if matching_column:
                    output_df[column] = df[matching_column]
                else:
                    # Если не найдено похожих названий столбцов, добавляем столбец со значением null
                    if column == "placeOfWork" and "company_name" in df.columns:
                        output_df[column] = df["company_name"]
                    else:
                        output_df[column] = "null"

        # Формируем имя выходного файла на основе имени входного файла
        # output_file = os.path.basename(csv_file).replace(".csv", "_corrected.csv")
        # output_path = os.path.join(output_dir, output_file)

        # Сохраняем output_df в выходной файл
        # output_df.to_csv(output_path, index=False)

        print(f"Обработка файла {csv_file} завершена.")
        return output_df

# Пример использования
input_directory = "/Users/arsen/Desktop/MDC/csvmaker/NOT_corrected"
output_directory = "/Users/arsen/Desktop/MDC/csvmaker/corrected"
process_csv_files(input_directory, output_directory)
