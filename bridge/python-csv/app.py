from flask import Flask, request
from flask_cors import CORS
import os
import csv
import psycopg2

app = Flask(__name__)
CORS(app)

@app.route('/get', methods=['GET'])
def my_endpoint():
    return 'Hello, World!'

@app.route('/updatecsv', methods=['POST'])
def update_csv():
    if 'csv' not in request.files:
        return 'No file uploaded', 400

    csv_file = request.files['csv']
    csv_file.save(os.path.join(os.getcwd(), 'data.csv'))
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
    print("file saved")
    return 'File saved', 200

def connect_db(): 
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="bridge-db",
            user="postgres",
            password="postgres"
        )
        print("#### Connection to the database successful!:)  ####  ")
        return conn
    except psycopg2.Error as e:
        print("#### Error connecting to the database:", e)
        raise SystemExit(1)  # Завершение программы с кодом ошибки

db = connect_db()
print(db)

def Create_Table_Profile(conn):
    cursor = conn.cursor()
    Profile_table = '''CREATE TABLE IF NOT EXISTS profile (    
        id SERIAL PRIMARY KEY,         
        firstName TEXT,
        lastName TEXT,
        dateOfBirth TIMESTAMP,
        gender TEXT,
        email TEXT[],
        phone TEXT[],
        maritalStatus INTEGER,
        income INTEGER
    );'''

    try:
        cursor.execute(Profile_table)
        print("Table 'profile' created successfully!")
    except psycopg2.Error as e:
        print("Error creating table:", e)

    conn.commit()
    cursor.close()

def Create_Table_Contacts(conn):
    cursor = conn.cursor()
    Contacts_Table ='''CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        profileId INTEGER REFERENCES profile(id),
        mobilePhone TEXT,
        address TEXT,
        linkedAccounts TEXT[],
        website TEXT
    );'''
    try:
        cursor.execute(Contacts_Table)
        print("Table 'Contacts' created successfully")
    except psycopg2.Error as e:
        print("Error creating table:", e)
    conn.commit()
    cursor.close()

def Create_Table_PlaceOfResidence(conn):
    cursor = conn.cursor()
    PlaceOfResidence_Table = '''CREATE TABLE IF NOT EXISTS placeOfResidence (
        id SERIAL PRIMARY KEY,
        profileId INTEGER REFERENCES profile(id),
        currentCity TEXT,
        birthPlace TEXT,
        otherCities TEXT[]
    );'''
    try:
        cursor.execute(PlaceOfResidence_Table)
        print("table 'PlaceOfResidence' created successfully")
    except psycopg2.Error as e: 
        print("Error creating table:", e)
    conn.commit()
    cursor.close()

def Create_Table_PersonalInterested(conn):
    cursor = conn.cursor()
    Personal_Interests_Table = '''CREATE TABLE IF NOT EXISTS personalInterests (
        id SERIAL PRIMARY KEY,
        profileId INTEGER REFERENCES profile(id),
        briefDescription TEXT,
        hobby TEXT,
        sport TEXT
    );'''
    try:
        cursor.execute(Personal_Interests_Table)
        print("table 'personalInterests' Created Successfully")
    except psycopg2.Error as e:
        print("Error creating table: ", e)
    conn.commit()
    cursor.close()

def Create_Table_DeviceInformation(conn):
    cursor = conn.cursor()
    Device_Information_Table = '''CREATE TABLE IF NOT EXISTS deviceInformation (
        id SERIAL PRIMARY KEY,
        profileId INTEGER REFERENCES profile(id),
        operatingSystem TEXT,
        displayResolution TEXT,
        browser TEXT,
        ISP TEXT,
        adBlock BOOLEAN
    );'''
    try:
        cursor.execute(Device_Information_Table)
        print("table 'Device Information' Created Successfully")
    except psycopg2.Error as e:
        print("Error creating table: ", e)
    conn.commit()
    cursor.close()

def Create_Table_Cookies(conn):
    cursor = conn.cursor()
    Cookies_Table = '''CREATE TABLE IF NOT EXISTS cookies (
        id SERIAL PRIMARY KEY,
        profileId INTEGER REFERENCES profile(id),
        sessionState TEXT,
        language TEXT,
        region TEXT,
        recentPages TEXT[],
        productId INTEGER,
        productName TEXT,
        productPrice INTEGER,
        quantity INTEGER,
        subTotal INTEGER,
        total INTEGER,
        couponCode TEXT,
        shippingInformation TEXT,
        taxInformation TEXT
    );'''
    try:
        cursor.execute(Cookies_Table)
        print("table 'Cookies' Created Successfully")
    except psycopg2.Error as e:
        print("Error creating table: ", e)
    conn.commit()
    cursor.close()

def Create_Table_Settings(conn):
    cursor = conn.cursor()
    Settings_Table = '''CREATE TABLE IF NOT EXISTS settings (                                                              
        id SERIAL PRIMARY KEY,
        email TEXT,                                                                       
        profileId INTEGER REFERENCES profile(id),
        profileIds INTEGER[],
        basicDataIds INTEGER[],
        contactsIds INTEGER[],
        workAndEducationIds INTEGER[],
        placeOfResidenceIds INTEGER[],
        personalInterestsIds INTEGER[]
    );'''
    try:
        cursor.execute(Settings_Table)
        print("table 'Settings' Created Successfully")
    except psycopg2.Error as e:
        print("Error creating table: ", e)
    conn.commit()
    cursor.close()

def Create_Table_WorkdAndEducation(conn):
    cursor = conn.cursor()
    WorkAndEducation_Table = '''CREATE TABLE IF NOT EXISTS workAndEducation (
        id SERIAL PRIMARY KEY,
        profileId INTEGER REFERENCES profile(id),
        placeOfWork TEXT,
        skills TEXT[],
        university TEXT,
        faculty TEXT
    );'''
    try:
        cursor.execute(WorkAndEducation_Table)
        print('Table "Work and Education" created successfully') 
    except psycopg2.Error as e: 
        print("Error creating table:", e)
    conn.commit()
    cursor.close()


def Create_Table_BasicData(conn):
    cursor = conn.cursor()
    Basic_Data = ''' 
    CREATE TABLE IF NOT EXISTS basicData (
        id SERIAL PRIMARY KEY,
        profileId INTEGER REFERENCES profile(id),
        interests TEXT,
        languages TEXT[],
        religionViews TEXT,
        politicalViews TEXT
    );'''

    try:
        cursor.execute(Basic_Data)
        print("### TABLE BASICDATA created succesfully ###")
    except psycopg2.Error as e:
        print("ERROR Creating Database: ",e)

    conn.commit()
    cursor.close()
db = connect_db()


print(Create_Table_Profile(db))
print(Create_Table_BasicData(db))
print(Create_Table_Contacts(db))
print(Create_Table_WorkdAndEducation(db))
print(Create_Table_PlaceOfResidence(db))
print(Create_Table_PersonalInterested(db))
print(Create_Table_DeviceInformation(db))
print(Create_Table_Cookies(db))
print(Create_Table_Settings(db))
# Функция для вставки данных в таблицу

def insert_data(table_name, data,conn):
    cursor = conn.cursor()
    columns = ', '.join(data.keys())
    values = tuple(data.values())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)
    if table_name == 'profile':
        0
    conn.commit()
    cursor.close()

# Функция для получения идентификатора профиля
def get_profile_id(first_name, last_name,conn):
    cursor = conn.cursor()
    query = "SELECT id FROM profile WHERE email = %s OR phone = %s"
    cursor.execute(query, (first_name, last_name))
    profile_id = cursor.fetchone()
    cursor.close()
    return profile_id[0] if profile_id else None

# Чтение CSV файла и вставка данных в таблицы
def SaveDataInCsv(conn):
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Вставка данных в таблицу profile
        
            profile_data = {
                'firstName': row['firstname'] if 'firstname' in row else None,
                'lastName': row['lastname'] if 'lastname' in row else None,
                'dateOfBirth': row['datebirth'] if 'datebirth' in row else None,
                'gender': row['gender'] if 'gender' in row else None,
                'email': row['email'].split(';') if 'email'in row else None,   # Разделение множественных значений через ;
                'phone': row['phone'].split(';') if 'phone' in row else None,  # Разделение множественных значений через ;
                'maritalStatus': int(row['maritalstatus']) if 'maritalstatus' in row else None,
                'income': int(row['income']) if 'income' in row else None
            }
            insert_data('profile', profile_data,conn)

            # Получение идентификатора профиля
            profile_id = get_profile_id(profile_data['email'], profile_data['phone'],conn)
            # Вставка данных в таблицу basicData
            basic_data = {
                'profileId': profile_id,
                'interests': row['interests'] if 'interests' in row else None,
                'languages': row['languages'].split(';') if 'languages' in row else None,  # Разделение множественных значений через ;
                'religionViews': row['religionviews'] if 'religionviews' in row else None,
                'politicalViews': row['politicalviews'] if 'politicalviews' in row else None,
            }
            insert_data('basicData', basic_data,conn)

            # Вставка данных в таблицу contacts
            contacts_data = {
                'profileId': profile_id,
                'mobilePhone': row['mobilephone'] if 'mobilephone' in row else None,
                'address': row['address'] if 'address' in row else None,
                'linkedAccounts': row['linkedaccounts'].split(';') if 'linkedaccounts' in row else None,  # Разделение множественных значений через ;
                'website': row['website'] if 'website' in row else None
            }
            insert_data('contacts', contacts_data,conn)
            workAndEducation = {
                'profileId':profile_id,
                'placeOfWork':row['placeofwork'] if 'placeofwork' in row else None,
                'skills': row['skills'].split(';') if 'skills' in row else None,
                'university':row['university'] if 'university' in row else None,
                'faculty': row['faculty'] if 'faculty' in row else None,
            }
            insert_data('workAndEducation', workAndEducation,conn)
            placeOfResidence = {
                'profileId': profile_id,
                'currentCity':row['currentcity'] if 'currentcity' in row else None,
                'birthPlace': row['birthplace'] if 'birthplace' in row else None,
                'otherCities':row['othercities'].split(';') if 'othercities' in row else None
            }
            insert_data('placeOfResidence', placeOfResidence,conn)
            personalInterested = {
                'profileId': profile_id,
                'briefDescription':row['briefdescription'] if 'briefdescription' in row else None,
                'hobby':row['hobby'] if 'hobby' in row else None,
                'sport': row['sport'] if 'sport' in row else None,
            }
            insert_data('personalInterests',personalInterested,conn)
            deviceInformation = {
                'profileId':profile_id,
                'operatingsystem':row['operatingsystem'] if 'operatingsystem' in row else None,
                'displayResolution':row['displayresolution'] if 'displayresolution' in row else None,
                'browser': row['browser'] if 'browser' in row else None,
                'ISP': row['isp'] if 'isp' in row else None,
                'adBlock': row['adblock'] if 'adblock' in row else None,
            }
            insert_data('deviceInformation', deviceInformation,conn)
            cookies = {
                'profileId': profile_id,
                'sessionState':row['sessionstate'] if 'sessionstate' in row else None,
                'language': row['language'] if 'language' in row else None,
                'region': row['region'] if 'region' in row else None,
                'recentPages':row['recentpages'].split(';') if 'recentpages' in row else None,
                'productName':row['productname'] if 'productname' in row else None,
                'productPrice':row['productprice'] if 'productprice' in row else None,
                'quantity': row['quantity'] if 'quantity' in row else None,
                'subTotal': row['subtotal'] if 'subtotal' in row else None,
                'total': row['total'] if 'total' in row else None,
                'couponCode': row['couponcode'] if 'couponcode' in row else None,
                'shippingInformation': row['shippinginformation'] if 'shippinginformation' in row else None,
                'taxInformation': row['taxinformation'] if 'taxinformation' in row else None
            }
            insert_data('cookies', cookies,conn)
            settings = {
                'email': row['email'] if 'email' in row else None,
                'profileId':profile_id,
                'profileIds':[0,0,0],
                'basicDataIds':[0,0,0],
                'contactsIds':[0,0,0],
                'workAndEducationIds':[0,0,0],
                'placeOfResidenceIds':[0,0,0],
                'personalInterestsIds':[0,0,0],
            }
            insert_data('settings',settings,conn)

            #Продолжите аналогичным образом для остальных таблиц

    #Закрытие соединения с базой данных PostgreSQL

    conn.close()
    return "DONE 200 (-_-)"

print(SaveDataInCsv(db))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)