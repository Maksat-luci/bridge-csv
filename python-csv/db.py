import csv
import psycopg2 



def Create_Table_Profile(conn):
    cursor = conn.cursor()
    Profile_table = '''CREATE TABLE IF NOT EXISTS profile (
        id SERIAL PRIMARY KEY,
        datasetsId UUID REFERENCES datasets (id),
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

def Create_Table_Datasets(conn):
    cursor = conn.cursor()
    datasets_table = '''CREATE TABLE IF NOT EXISTS datasets (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name TEXT,
        filename TEXT
    );'''
    try:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        print("function added successfully")
    except psycopg2.Error as e:
        print("Error Added function for uuid (uuid_generate_v4())")
    try:
        cursor.execute(datasets_table)
        print("Table 'Datasets' created successfully!")
    except psycopg2.Error as e:
        print("Error creating table:", e)
    conn.commit()
    cursor.close()

def Create_Table_Credentials(conn):
    cursor = conn.cursor()
    Profile_table = '''CREATE TABLE IF NOT EXISTS credentials (    
        id SERIAL PRIMARY KEY,
        profileId INTEGER REFERENCES profile(id),
        emails TEXT[],
        phones TEXT[]
    );'''

    try:
        cursor.execute(Profile_table)
        print("Table 'Credentials' created successfully!")
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

# Функция для вставки данных в таблицу
def insert_data(table_name, data, conn):
    try:
        cursor = conn.cursor()
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
    except Exception as e:
        # Обработка исключения
        print(f"An error occurred during data insertion: {e}")
        conn.rollback()



# Функция для получения идентификатора профиля
def get_profile_id(email, phone,conn):
    cursor = conn.cursor()
    query = "SELECT id FROM profile WHERE email = %s OR phone = %s"
    cursor.execute(query, (email, phone))
    profile_id = cursor.fetchone()
    cursor.close()
    return profile_id[0] if profile_id else None

def get_dataset_id(name,conn):
    cursor = conn.cursor()
    query = "SELECT id FROM datasets WHERE name = %s"
    cursor.execute(query, (name,))
    dataset_id = cursor.fetchone()
    cursor.close()
    return dataset_id[0] if dataset_id else None

def process_empty_string(value):
    return None if value == '' else value

# Чтение CSV файла и вставка данных в таблицы
def SaveDataInCsv(conn,filenamecsv,dataset_name):
    with open(filenamecsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset_data = {
            'name': dataset_name,
            'filename': filenamecsv
        }
        insert_data('datasets', dataset_data,conn)
        dataset_id = get_dataset_id(dataset_data['name'],conn)
        for row in reader:
            profile_data = {
                'datasetsId': dataset_id,
                'firstName': process_empty_string(row.get('firstName')),
                'lastName': process_empty_string(row.get('lastName')),
                'dateOfBirth': process_empty_string(row.get('dateOfBirth')),
                'gender': process_empty_string(row.get('gender')),
                'email': row.get('email').split(';') if row.get('email') is not None else None,
                'phone': row.get('phone').split(';') if row.get('phone') is not None else None,
                'maritalStatus': process_empty_string(row.get('maritalStatus')),
                'income': process_empty_string(row.get('income')) 
            }

            insert_data('profile', profile_data,conn)

            # Получение идентификатора профиля
            profile_id = get_profile_id(profile_data['email'], profile_data['phone'],conn)
            # Вставка данных в таблицу basicData
            credentials_data = {
                'profileId': profile_id,
                'emails': process_empty_string(profile_data['email']),
                'phones': process_empty_string(profile_data['phone'])
            }
            insert_data('credentials',credentials_data,conn)

            basic_data = {
                'profileId': profile_id,
                'interests': process_empty_string(row.get('interests')),
                'languages': row.get('languages').split(';') if row.get('languages') is not None else None,  # Разделение множественных значений через ;
                'religionViews': process_empty_string(row.get('religionViews')),
                'politicalViews': process_empty_string(row.get('politicalViews')),
            }
            insert_data('basicData', basic_data,conn)

            # Вставка данных в таблицу contacts
            contacts_data = {
                'profileId': profile_id,
                'mobilePhone': process_empty_string(row.get('mobilePhone')),
                'address': process_empty_string(row.get('address')),
                'linkedAccounts': row.get('linkedAccounts').split(';') if row.get('linkedAccounts') is not None else None,
                'website': process_empty_string(row.get('website'))
            }
            insert_data('contacts', contacts_data,conn)
            workAndEducation = {
                'profileId':profile_id,
                'placeOfWork':process_empty_string(row.get('placeOfWork')),
                'skills': row.get('skills').split(';') if row.get('skills') is not None else None,
                'university':process_empty_string(row.get('university')),
                'faculty': process_empty_string(row.get('faculty')),
            }
            insert_data('workAndEducation', workAndEducation,conn)
            placeOfResidence = {
                'profileId': profile_id,
                'currentCity':process_empty_string(row.get('currentCity')),
                'birthPlace': process_empty_string(row.get('birthPlace')),
                'otherCities':row.get('otherCities').split(';') if row.get('otherCities') is not None else None
            }
            insert_data('placeOfResidence', placeOfResidence,conn)
            personalInterested = {
                'profileId': profile_id,
                'briefDescription':process_empty_string(row.get('briefDescription')),
                'hobby':process_empty_string(row.get('hobby')),
                'sport': process_empty_string(row.get('sport')),
            }
            insert_data('personalInterests',personalInterested,conn)
            deviceInformation = {
                'profileId':profile_id,
                'operatingsystem':process_empty_string(row.get('operatingSystem')),
                'displayResolution':process_empty_string(row.get('displayResolution')),
                'browser': process_empty_string(row.get('browser')),
                'ISP': process_empty_string(row.get('iSP')),
                'adBlock': process_empty_string(row.get('adBlock')),
            }
            insert_data('deviceInformation', deviceInformation,conn)
            cookies = {
                'profileId': profile_id,
                'sessionState':process_empty_string(row.get('sessionState')),
                'language': process_empty_string(row.get('language')),
                'region': process_empty_string(row.get('region')),
                'recentPages':row.get('recentPages').split(';') if row.get('recentPages') is not None else None,
                'productName':process_empty_string(row.get('productName')),
                'productPrice':process_empty_string(row.get('productPrice')),
                'quantity': process_empty_string(row.get('quantity')),
                'subTotal': process_empty_string(row.get('subtotal')),
                'total': process_empty_string(row.get('total')),
                'couponCode': process_empty_string(row.get('couponCode')),
                'shippingInformation': process_empty_string(row.get('shippingInformation')),
                'taxInformation': process_empty_string(row.get('taxInformation'))
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

    conn.close()


def execute_query(query, data=None):
    conn = psycopg2.connect(
        host="db",
        port="5432",
        dbname="bridge-db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    if data:
        cur.execute(query, data)
    else:
        cur.execute(query)
    conn.commit()
    if cur.description is not None:
        result = cur.fetchall()
    else:
        result = True
    cur.close()
    conn.close()
    return result

