import csv
import psycopg2 
import uuid


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
def get_profile_id(email, phone, conn):
    cursor = conn.cursor()
    query = "SELECT id FROM profile WHERE email[1] = ANY (%s::varchar[]) OR phone[1] = ANY (%s::varchar[])"
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

def generate_uuid():

    return str(uuid.uuid4())
# Чтение CSV файла и вставка данных в таблицы
def SaveDataInCsv(conn,filenamecsv,dataset_name):
    with open(filenamecsv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset_data = {
            'id': generate_uuid(),
            'name': dataset_name,
            'filename': filenamecsv
        }
        insert_data('datasets', dataset_data,conn)
        # dataset_id = get_dataset_id(dataset_data['name'],conn)
        for row in reader:
            profile_data = {
                'datasetsid': dataset_data.get('id'),
                'firstname': process_empty_string(row.get('firstName')),
                'lastname': process_empty_string(row.get('lastName')),
                'dateofbirth': process_empty_string(row.get('dateOfBirth')),
                'gender': process_empty_string(row.get('gender')),
                'email': row.get('email').split(';') if row.get('email') is not None else None,
                'phone': row.get('phone').split(';') if row.get('phone') is not None else None,
                'maritalstatus': process_empty_string(row.get('maritalStatus')),
                'income': process_empty_string(row.get('income')) 
            }

            insert_data('profile', profile_data,conn)

            # Получение идентификатора профиля
            profile_id = get_profile_id(profile_data['email'], profile_data['phone'],conn)
            # Вставка данных в таблицу basicData
            credentials_data = {
                'profileid': profile_id,
                'emails': process_empty_string(profile_data['email']),
                'phones': process_empty_string(profile_data['phone'])
            }
            insert_data('credentials',credentials_data,conn)

            basic_data = {
                'profileid': profile_id,
                'interests': process_empty_string(row.get('interests')),
                'languages': row.get('languages').split(';') if row.get('languages') is not None else None,  # Разделение множественных значений через ;
                'religionviews': process_empty_string(row.get('religionViews')),
                'politicalviews': process_empty_string(row.get('politicalViews')),
            }
            insert_data('basicdata', basic_data,conn)

            # Вставка данных в таблицу contacts
            contacts_data = {
                'profileid': profile_id,
                'mobilephone': process_empty_string(row.get('mobilePhone')),
                'address': process_empty_string(row.get('address')),
                'linkedaccounts': row.get('linkedAccounts').split(';') if row.get('linkedAccounts') is not None else None,
                'website': process_empty_string(row.get('website'))
            }
            insert_data('contacts', contacts_data,conn)
            workAndEducation = {
                'profileid':profile_id,
                'placeofwork':process_empty_string(row.get('placeOfWork')),
                'skills': row.get('skills').split(';') if row.get('skills') is not None else None,
                'university':process_empty_string(row.get('university')),
                'faculty': process_empty_string(row.get('faculty')),
            }
            insert_data('workAndEducation', workAndEducation,conn)
            placeOfResidence = {
                'profileid': profile_id,
                'currentcity':process_empty_string(row.get('currentCity')),
                'birthplace': process_empty_string(row.get('birthPlace')),
                'othercities':row.get('otherCities').split(';') if row.get('otherCities') is not None else None
            }
            insert_data('placeofresidence', placeOfResidence,conn)
            personalInterested = {
                'profileid': profile_id,
                'briefdescription':process_empty_string(row.get('briefDescription')),
                'hobby':process_empty_string(row.get('hobby')),
                'sport': process_empty_string(row.get('sport')),
            }
            insert_data('personalinterests',personalInterested,conn)
            deviceInformation = {
                'profileid':profile_id,
                'operatingsystem':process_empty_string(row.get('operatingSystem')),
                'displayresolution':process_empty_string(row.get('displayResolution')),
                'browser': process_empty_string(row.get('browser')),
                'isp': process_empty_string(row.get('iSP')),
                'adblock': process_empty_string(row.get('adBlock')),
            }
            insert_data('deviceinformation', deviceInformation,conn)
            cookies = {
                'profileid': profile_id,
                'sessionstate':process_empty_string(row.get('sessionState')),
                'language': process_empty_string(row.get('language')),
                'region': process_empty_string(row.get('region')),
                'recentpages':row.get('recentPages').split(';') if row.get('recentPages') is not None else None,
                'productname':process_empty_string(row.get('productName')),
                'productprice':process_empty_string(row.get('productPrice')),
                'quantity': process_empty_string(row.get('quantity')),
                'subtotal': process_empty_string(row.get('subtotal')),
                'total': process_empty_string(row.get('total')),
                'couponcode': process_empty_string(row.get('couponCode')),
                'shippinginformation': process_empty_string(row.get('shippingInformation')),
                'taxinformation': process_empty_string(row.get('taxInformation'))
            }
            insert_data('cookies', cookies,conn)
            settings = {
                'email': row['email'] if 'email' in row else None,
                'profileid':profile_id,
                'profileids':[0,0,0],
                'basicdataids':[0,0,0],
                'contactsids':[0,0,0],
                'workandeducationids':[0,0,0],
                'placeofresidenceids':[0,0,0],
                'personalinterestsids':[0,0,0],
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

