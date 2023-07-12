from flask import Flask, redirect, request, jsonify,render_template, render_template_string,Response
from flask_cors import CORS
import psycopg2 
import db
import os
from psycopg2 import sql
import requests
from flasgger import Swagger
import mapper
import hashlib
from cryptography.fernet import Fernet
import base64
import csv
import io
from io import StringIO
from flask import Flask, request, jsonify, send_file
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Profile, Settings, Credentials, Contacts, PlaceOfResidence, PersonalInterests, \
    DeviceInformation, Cookies, WorkAndEducation, BasicData
app = Flask(__name__)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'allowed-swagger',
            "route": '/allowed-swagger/swagger.json',  # Обновленный путь к swagger.json
            "rule_filter": lambda rule: True,  
            "model_filter": lambda tag: True,  
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/allowed-swagger"  # Обновленный путь для доступа к Swagger UI
}
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "MDC-Bridge API Documentation",
        "version": "1.0"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
}, config=swagger_config)
CORS(app)


def Connect_db(): 
    try:
        conn = psycopg2.connect(
            host="db",
            port="5432",
            dbname="bridge-db",
            user="postgres",
            password="postgres"
        )
        print("#### Connection to the database successful!:)  ####")
        return conn
    except psycopg2.Error as e:
        print("#### Error connecting to the database:", e)
        raise SystemExit(1)  # Завершение программы с кодом ошибки
    


@app.route('/api/v1/set-user-privacy', methods=['POST'])
def setUserPrivacy():
    """
    Set user privacy settings.

    ---
    tags:
      - API
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User email
            category:
              type: string
              description: Privacy category
            settingsValue:
              type: string
              description: Settings value

    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            success:
              type: boolean
              description: Indicates if the operation was successful
      400:
        description: Bad Request
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      404:
        description: Not Found
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    # Проверка наличия специального токена
    auth_token = os.getenv('AUTH_TOKEN')
    
    if request.headers.get('Authorization') != auth_token:
        return jsonify({'error': 'Invalid token'}), 401

    # Получение данных из тела запроса
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415

    data = request.get_json()
    email = data.get('email')
    category = data.get('category')
    settings_value = data.get('settingsValue')

    if not email or not category or not settings_value:
        return jsonify({'error': 'Invalid request body'}), 400

    try:
        query = sql.SQL("SELECT * FROM settings WHERE %s = ANY(email)")
        result = db.execute_query(query, (email,))

        if not result:
            return jsonify({'error': 'Email not found'}), 404

        query = sql.SQL("UPDATE settings SET {} = %s WHERE %s = ANY(email)")
        query = query.format(sql.Identifier(category))
        db.execute_query(query, (settings_value, email))

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/v1/get-profile-data', methods=['GET'])
def get_profile():
    """
    Get profile data.

    ---
    tags:
      - API
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: Email address of the profile to retrieve.

    responses:
      200:
        description: Profile data retrieved successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                Data:
                  type: object
                  properties:
                    # ... (existing properties)

        examples:
          application/json:
            {
              "Data": {
                "profile": {
                  "id": 1,
                  "firstName": "John",
                  "lastName": "Doe",
                  "dateOfBirth": "1990-01-01",
                  "gender": "Male",
                  "email": "johndoe@example.com",
                  "phone": "123-456-7890",
                  "maritalStatus": "Single",
                  "income": 50000
                },
                "basicData": {
                  "interests": "Music",
                  "languages": "English, French",
                  "religionViews": "Agnostic",
                  "politicalViews": "Liberal"
                },
                "contacts": {
                  "mobilePhone": "987-654-3210",
                  "address": "123 Main St, City",
                  "linkedAccounts": "Twitter: @johndoe",
                  "website": "johndoe.com"
                },
                "workAndEducation": {
                  "placeOfWork": "ABC Company",
                  "skills": "Programming, Project Management",
                  "university": "XYZ University",
                  "faculty": "Computer Science"
                },
                "placeOfResidence": {
                  "currentCity": "City",
                  "birthPlace": "City",
                  "otherCities": "City1, City2"
                },
                "personalInterests": {
                  "briefDescription": "I love playing guitar.",
                  "hobby": "Gardening",
                  "sport": "Football"
                },
                "deviceInformation": {
                  "operatingSystem": "Windows 10",
                  "displayResolution": "1920x1080",
                  "browser": "Chrome",
                  "ISP": "Internet Provider",
                  "adBlock": true
                },
                "cookies": {
                  "sessionState": "Active",
                  "language": "English",
                  "region": "US",
                  "recentPages": "Homepage, Products",
                  "productId": "12345",
                  "productName": "Product A",
                  "productPrice": 19.99,
                  "quantity": 2,
                  "subTotal": 39.98,
                  "total": 39.98,
                  "couponCode": "DISCOUNT10",
                  "shippingInformation": "123 Main St, City",
                  "taxInformation": "1234567890"
                }
              }
            }
      400:
        description: Bad Request
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      404:
        description: Not Found
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    auth_token = os.getenv('AUTH_TOKEN')

    if request.headers.get('Authorization') != auth_token:
        return jsonify({'error': 'Invalid token'}), 401
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415


    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email parameter is missing'}), 400

    try:
        query = """
        SELECT DISTINCT p.id, p.firstname, p.lastname, p.dateofbirth, p.gender, p.email, p.phone, p.maritalstatus, p.income,
               bd.interests, bd.languages, bd.religionviews, bd.politicalviews,
               c.mobilephone, c.address, c.linkedaccounts, c.website,
               w.placeofwork, w.skills, w.university, w.faculty,
               pr.currentcity, pr.birthplace, pr.othercities,
               pi.briefdescription, pi.hobby, pi.sport,
               di.operatingsystem, di.displayresolution, di.browser, di.isp, di.adblock,
               co.sessionstate, co.language, co.region, co.recentpages, co.productid, co.productname, co.productprice,
               co.quantity, co.subtotal, co.total, co.couponcode, co.shippinginformation, co.taxinformation
        FROM profile p
        LEFT JOIN basicdata bd ON p.id = bd.profileid
        LEFT JOIN contacts c ON p.id = c.profileid
        LEFT JOIN workandeducation w ON p.id = w.profileid
        LEFT JOIN placeofresidence pr ON p.id = pr.profileid
        LEFT JOIN personalinterests pi ON p.id = pi.profileid
        LEFT JOIN deviceinformation di ON p.id = di.profileid
        LEFT JOIN cookies co ON p.id = co.profileid
        WHERE %s = ANY(p.email)
        """
        
        result = db.execute_query(query, (email,))

        if not result:
            return jsonify({'error': 'No profile found for the provided email'}), 404

        profile_data = {
            'profile': {
            'id': hash_data(result[0][0]),
            'firstName': hash_data(result[0][1]),
            'lastName': hash_data(result[0][2]),
            'dateOfBirth': hash_data(str(result[0][3])),
            'gender': hash_data(result[0][4]),
            'email': hash_data(result[0][5]),
            'phone': hash_data(result[0][6]),
            'maritalStatus': hash_data(result[0][7]),
            'income': hash_data(result[0][8]),
            },

            'basicData': {
                'interests': hash_data(result[0][9]),
                'languages': hash_data(result[0][10]),
                'religionViews': hash_data(result[0][11]),
                'politicalViews': hash_data(result[0][12])
            },
            'contacts': {
                'mobilePhone': hash_data(result[0][13]),
                'address': hash_data(result[0][14]),
                'linkedAccounts': hash_data(result[0][15]),
                'website': hash_data(result[0][16])
            },
            'workAndEducation': {
                'placeOfWork': hash_data(result[0][17]),
                'skills': hash_data(result[0][18]),
                'university': hash_data(result[0][19]),
                'faculty': hash_data(result[0][20])
            },
            'placeOfResidence': {
                'currentCity': hash_data(result[0][21]),
                'birthPlace': hash_data(result[0][22]),
                'otherCities': hash_data(result[0][23])
            },
            'personalInterests': {
                'briefDescription': hash_data(result[0][24]),
                'hobby': hash_data(result[0][25]),
                'sport': hash_data(result[0][26])
            },
            'deviceInformation': {
                'operatingSystem': hash_data(result[0][27]),
                'displayResolution': hash_data(result[0][28]),
                'browser': hash_data(result[0][29]),
                'ISP': hash_data(result[0][30]),
                'adBlock': hash_data(bool(result[0][31]))
            },
            'cookies': {
                'sessionState': hash_data(result[0][32]),
                'language': hash_data(result[0][33]),
                'region': hash_data(result[0][34]),
                'recentPages': hash_data(result[0][35]),
                'productId': hash_data(result[0][36]),
                'productName': hash_data(result[0][37]),
                'productPrice': hash_data(result[0][38]),
                'quantity': hash_data(result[0][39]),
                'subTotal': hash_data(result[0][40]),
                'total': hash_data(result[0][41]),
                'couponCode': hash_data(result[0][42]),
                'shippingInformation': hash_data(result[0][43]),
                'taxInformation': hash_data(result[0][44])
            }
        }
        return jsonify({'Data': profile_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def decrypt_dict_values(data):
    decrypted_data = {}

    for key, value in data.items():
        if isinstance(value, dict):
            decrypted_data[key] = decrypt_dict_values(value)
        else:
            decrypted_data[key] = decrypt_data(value)

    return decrypted_data

def decrypt_data(encrypted_data):
    if encrypted_data is None:
      return None
    try:
        salt = os.getenv('AUTH_TOKEN')
        decrypted_values = []

        if isinstance(encrypted_data, list):
            for item in encrypted_data:
                key = base64.urlsafe_b64encode(hashlib.sha256(salt.encode()).digest())
                cipher = Fernet(key)
                decrypted_data = cipher.decrypt(item.encode('utf-8')).decode('utf-8')
                decrypted_data = decrypted_data[len(salt):]

                decrypted_values.append(decrypted_data)
        else:
            key = base64.urlsafe_b64encode(hashlib.sha256(salt.encode()).digest())
            cipher = Fernet(key)
            decrypted_data = cipher.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
            decrypted_data = decrypted_data[len(salt):]
            return decrypted_data

        return decrypted_values

    except Exception as e:
        print("Ошибка при отхэшировании данных:", str(e))
        return None



def hash_data(data):
    if data is None:
      return None
    try:
        salt = os.getenv('AUTH_TOKEN')
        hashed_values = []

        if isinstance(data, int):
            data = str(data)
        if isinstance(data, list):
            for item in data:
                item = str(item)
                salted_data = salt + item
                key = base64.urlsafe_b64encode(hashlib.sha256(salt.encode()).digest())
                cipher = Fernet(key)
                encrypted_data = cipher.encrypt(salted_data.encode('utf-8'))
                hashed_values.append(encrypted_data.decode('utf-8'))
        else:
            data = str(data)
            salted_data = salt + data
            key = base64.urlsafe_b64encode(hashlib.sha256(salt.encode()).digest())
            cipher = Fernet(key)
            encrypted_data = cipher.encrypt(salted_data.encode('utf-8'))
            return encrypted_data.decode('utf-8')

        return hashed_values

    except Exception as e:
        print("Ошибка при хэшировании данных:", str(e))
        return None
    
@app.route('/swagger',methods=['GET','POST'])
def show_swagger():
    if request.method == 'POST':
      auth_token = os.getenv('AUTH_TOKEN')
      if request.form.get('token') != auth_token:
        return redirect('/unauthorized')
      return redirect('/allowed-swagger')
    
    return render_template('verify.html')

@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')


@app.route('/upload', methods=['POST', 'GET'])
def update_csv():
    """
    Update CSV data.
    ---
    tags:
      - API
    parameters:
      - name: csv
        in: formData
        type: file
        required: true
        description: CSV file to update
      - name: datasetName
        in: formData
        type: string
        required: true
        description: Dataset name

    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
      400:
        description: Bad Request
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """

    if request.method == 'POST':
        auth_token = os.getenv('AUTH_TOKEN')

        if request.form.get('token') != auth_token:
            return render_template('unauthorized.html')

        dataset_name = request.form.get('datasetName')
        csv_file_f = request.files.get('csv')

        if csv_file_f is None:
            return 'No file uploaded', 400
        csv_dataframe = mapper.process_csv_files(csv_file_f)
        csv_dataframe.to_csv("data.csv", index=False)

        print("file saved")
        updatepostgres("data.csv", dataset_name)
        SendPostRequest(dataset_name)

        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Success Message</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
                <style>
                    body {
                        font-family: Arial, sans-serif;
                    }
                    .success-message {
                        text-align: center;
                        margin-top: 50px;
                    }
                    .success-message h2 {
                        color: #28a745;
                    }
                    .success-message p {
                        margin-bottom: 20px;
                    }
                    .emoji {
                        font-size: 60px;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success-message">
                        <h2>Request completed successfully</h2>
                        <p>Your dataset has been successfully uploaded to MDC.</p>
                        <div class="emoji">😻</div>
                    </div>
                </div>
            </body>
            </html>
        ''')

    return render_template('upload.html')

def get_row_count(conn, table_name):
    cursor = conn.cursor()
    query = f"SELECT COUNT(*) FROM {table_name};"
    cursor.execute(query)
    row_count = cursor.fetchone()[0]
    cursor.close()
    return row_count

def SendPostRequest(dataset_name):
    auth_token = os.getenv('AUTH_TOKEN')
    conn = Connect_db()
    uuid = db.get_dataset_id(dataset_name,conn)
    rows_count = get_row_count(conn,'profile')




    url = 'https://bridge.mydatacoin.io/api/v1/DataSets/create-dataset'
    data = {
        'token': auth_token,
        'id': str(uuid),
        'name': dataset_name,
        'rows': rows_count
    }
    response = requests.post(url, json=data)
    
    return response.text, response.status_code 

    

@app.route('/api/v1/credentials', methods=['GET'])
def get_credentials():
    """
    Get credentials.

    ---
    tags:
      - API

    responses:
      200:
        description: Success
        schema:
          type: object
          properties:
            credentials:
              type: array
              items:
                type: object
                properties:
                  profileId:
                    type: string
                    description: Profile ID
                  emails:
                    type: array
                    items:
                      type: string
                    description: List of emails
                  phones:
                    type: array
                    items:
                      type: string
                    description: List of phones
      401:
        description: Unauthorized
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Internal Server Error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    auth_token = os.getenv('AUTH_TOKEN')

    if request.headers.get('Authorization') != auth_token:
        return jsonify({'error': 'Invalid token'}), 401 

    
    conn = Connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM credentials"
    
    try:
        cursor.execute(query)
        credentials = cursor.fetchall()
        credentials_json = []
        for credential in credentials:
            credential_data = {
                'profileId': credential[1],
                'emails': credential[2],
                'phones': credential[3]
            }
            credentials_json.append(credential_data)
        
        return jsonify({'credentials': credentials_json})
    except psycopg2.Error as e:
        print("Error retrieving credentials:", e)
        return 'Error retrieving credentials', 500
    
    finally:
        cursor.close()
        conn.close()



@app.route('/api/v1/get-count-settings', methods=['POST'])
def process_request():
    """
    Получение счетчиков настроек по идентификатору набора данных.

    ---
    tags:
      - API
    parameters:
      - name: datasetid
        in: body
        description: Идентификатор набора данных
        required: true
        schema:
          type: object
          properties:
            datasetid:
              type: integer
        example:
          datasetid: 1
    responses:
      200:
        description: Успешный запрос. Возвращает счетчики настроек.
        schema:
          type: object
          properties:
            data:
              $ref: '#/definitions/SettingsCount'
      500:
        description: Внутренняя ошибка сервера. Возвращает сообщение об ошибке.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        auth_token = os.getenv('AUTH_TOKEN')

        if request.headers.get('Authorization') != auth_token:
          return jsonify({'error': 'Invalid token'}), 401 
        conn = Connect_db()
        cursor = conn.cursor()
        dataset_id = request.json.get('datasetid')
        query = """
        SELECT * FROM profile WHERE datasetsid = %s;
        """
        cursor.execute(query, (dataset_id,))
        profiles = cursor.fetchall()
    
        result = {'datasetid': dataset_id,
                  'profileids': {
                      'collection': 0,
                      'proccessing':0,
                      'monetize':0
                  },
                  'basicdataids': {
                      'collection': 0,
                      'proccessing':0,
                      'monetize':0
                  },
                  'contactsids': {
                      'collection': 0,
                      'proccessing':0,
                      'monetize':0
                  },
                  'workandeducationids': {
                      'collection': 0,
                      'proccessing':0,
                      'monetize':0
                  },
                  'placeofresidenceids': {
                      'collection': 0,
                      'proccessing':0,
                      'monetize':0
                  },
                  'personalinterestsids': {
                      'collection': 0,
                      'proccessing':0,
                      'monetize':0
                  },                  
                  }
    
        for profile in profiles:
            profile_id = profile[0]

            # Запрос для получения связанных настроек для заданного профиля
            query = """
            SELECT * FROM settings WHERE profileid = %s;
            """
            cursor.execute(query, (profile_id,))
            settings = cursor.fetchone()
            if settings:
                # Извлечение значений из массивов полей
                profileids = settings[3]
                basicdataids = settings[4]
                contactsids = settings[5]
                workandeducationids = settings[6]
                placeofresidenceids = settings[7]
                personalinterestsids = settings[8]

                # Суммирование первых значений
                profileids_sum = sum(profileids[:1]) if profileids else 0
                result['profileids']['collection'] += profileids_sum 
                profileids_second_sum = sum(profileids[1:2]) if len(profileids) >= 2 else 0
                result['profileids']['proccessing'] += profileids_second_sum 
                profileids_third_sum = sum(profileids[2:3]) if len(profileids) >= 3 else 0
                result['profileids']['monetize'] += profileids_third_sum

                basicdataids_sum = sum(basicdataids[:1]) if basicdataids else 0
                result['basicdataids']['collection'] += basicdataids_sum
                basicdataids_second_sum = sum(basicdataids[1:2]) if len(basicdataids) >= 2 else 0
                result['basicdataids']['proccessing'] += basicdataids_second_sum
                basicdataids_third_sum = sum(basicdataids[2:3]) if len(basicdataids) >= 3 else 0
                result['basicdataids']['monetize'] += basicdataids_third_sum

                contactsids_sum = sum(contactsids[:1]) if contactsids else 0
                result['contactsids']['collection'] += contactsids_sum
                contactsids_second_sum = sum(contactsids[1:2]) if len(contactsids) >= 2 else 0
                result['contactsids']['proccessing'] += contactsids_second_sum
                contactsids_third_sum = sum(contactsids[2:3]) if len(contactsids) >= 3 else 0         
                result['contactsids']['monetize'] += contactsids_third_sum
                
                workandeducationids_sum = sum(workandeducationids[:1]) if workandeducationids else 0
                result['workandeducationids']['collection'] += workandeducationids_sum
                workandeducationids_second_sum = sum(workandeducationids[1:2]) if len(workandeducationids) >= 2 else 0
                result['workandeducationids']['proccessing'] += workandeducationids_second_sum
                workandeducationids_third_sum = sum(workandeducationids[2:3]) if len(workandeducationids) >= 3 else 0
                result['workandeducationids']['monetize'] += workandeducationids_third_sum
                
                placeofresidenceids_sum = sum(placeofresidenceids[:1]) if placeofresidenceids else 0
                result['placeofresidenceids']['collection'] += placeofresidenceids_sum
                placeofresidenceids_second_sum = sum(placeofresidenceids[1:2]) if placeofresidenceids else 0
                result['placeofresidenceids']['proccessing'] += placeofresidenceids_second_sum
                placeofresidenceids_third_sum = sum(placeofresidenceids[2:3]) if placeofresidenceids else 0
                result['placeofresidenceids']['monetize'] += placeofresidenceids_third_sum

                personalinterestsids_sum = sum(personalinterestsids[:1]) if personalinterestsids else 0
                result['personalinterestsids']['collection'] += personalinterestsids_sum
                personalinterestsids_second_sum = sum(personalinterestsids[1:2]) if personalinterestsids else 0
                result['personalinterestsids']['proccessing'] += personalinterestsids_second_sum
                personalinterestsids_third_sum = sum(personalinterestsids[2:3]) if personalinterestsids else 0
                result['personalinterestsids']['monetize'] += personalinterestsids_third_sum


        cursor.close()
        conn.close()

        return jsonify({'data': result}), 200

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500

def updatepostgres(filenamecsv,dataset_name):
    connect_db = Connect_db()
    print(connect_db)
    db.SaveDataInCsv(connect_db,filenamecsv,dataset_name)

#ОТПРАВИТЬ НА ПОЧТУ
@app.route('/api/v1/generate-csv', methods=['POST'])
def generate_csv():
    try:
        DB_HOST = 'localhost'
        DB_PORT = 5858
        DB_NAME = 'bridge-db'
        DB_USER = 'postgres'
        DB_PASSWORD = 'postgres'

        # Создание подключения к базе данных
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        Session = sessionmaker(bind=engine)
        dataset_id = request.json.get('datasetid')

        # Создание сессии базы данных
        session = Session()

        # Получение профилей на основе datasetid
        profiles = session.query(Profile).filter_by(datasetsid=dataset_id).all()

        # Список для хранения данных для CSV-файла
        csv_data = []
        for profile in profiles:
          profile_id = profile.id
          settings = session.query(Settings).filter_by(profileid=profile_id).first()
          if settings:
            row_data = []  # Временный список для хранения данных из всех таблиц

            if settings.profileids and len(settings.profileids) >= 3 and settings.profileids[2] == 1:
              profile_data = session.query(Profile).filter_by(id=profile_id).first()
              row_data.extend([
                profile_data.firstname or 'null',
                profile_data.lastname or 'null',
                str(profile_data.dateofbirth) if profile_data.dateofbirth else 'null',
                profile_data.gender or 'null',
                '; '.join(profile_data.email) if profile_data.email and any(e.strip() != '' for e in profile_data.email) else 'null',
                '; '.join(profile_data.phone) if profile_data.phone and any(e.strip() != '' for e in profile_data.phone) else 'null',
                str(profile_data.maritalstatus) if profile_data.maritalstatus else 'null',
                str(profile_data.income) if profile_data.income else 'null'
              ])

            if settings.basicdataids and len(settings.basicdataids) >= 3 and settings.basicdataids[2] == 1:
              basic_data = session.query(BasicData).filter_by(profileid=profile_id).first()
              row_data.extend([
                '; '.join(basic_data.interests) if basic_data.interests and any(e.strip() != '' for e in basic_data.interests) else 'null',
                '; '.join(basic_data.languages) if basic_data.languages and any(e.strip() != '' for e in basic_data.languages) else 'null',
                 '; '.join(basic_data.religionviews) if basic_data.religionviews and any(e.strip() != '' for e in basic_data.religionviews) else 'null',
                 '; '.join(basic_data.politicalviews) if basic_data.politicalviews and any(e.strip() != '' for e in basic_data.politicalviews) else 'null',
              ])

            if settings.contactsids and len(settings.contactsids) >= 3 and settings.contactsids[2] == 1:
              contacts_data = session.query(Contacts).filter_by(profileid=profile_id).first()
              row_data.extend([
                contacts_data.mobilephone or 'null',
                contacts_data.address or 'null',
                '; '.join(contacts_data.linkedaccounts) if contacts_data.linkedaccounts and any(e.strip() != '' for e in contacts_data.linkedaccounts) else 'null',
                contacts_data.website or 'null'
              ])

            if settings.workandeducationids and len(settings.workandeducationids) >= 3 and settings.workandeducationids[2] == 1:
              work_education_data = session.query(WorkAndEducation).filter_by(profileid=profile_id).first()
              row_data.extend([
                work_education_data.placeofwork or 'null',
                '; '.join(work_education_data.skills) if work_education_data.skills and any(e.strip() != '' for e in work_education_data.skills) else 'null',
                work_education_data.university or 'null',
                work_education_data.faculty or 'null'
              ])

            if settings.placeofresidenceids and len(settings.placeofresidenceids) >= 3 and settings.placeofresidenceids[2] == 1:
              place_residence_data = session.query(PlaceOfResidence).filter_by(profileid=profile_id).first()
              row_data.extend([
                place_residence_data.currentcity or 'null',
                place_residence_data.birthplace or 'null',
                '; '.join(place_residence_data.othercities) if place_residence_data.othercities and any(e.strip() != '' for e in place_residence_data.othercities) else 'null'
             ])

            if settings.personalinterestsids and len(settings.personalinterestsids) >= 3 and settings.personalinterestsids[2] == 1:
              personal_interests_data = session.query(PersonalInterests).filter_by(profileid=profile_id).first()
              row_data.extend([
                personal_interests_data.briefdescription or 'null',
                '; '.join(personal_interests_data.hobby) if personal_interests_data.hobby and any(e.strip() != '' for e in personal_interests_data.hobby) else 'null',
                '; '.join(personal_interests_data.sport) if personal_interests_data.sport and any(e.strip() != '' for e in personal_interests_data.sport) else 'null',
              ])

            csv_data.append(row_data)  # Добавляем все данные из таблиц в одну строку

        # Сохранение CSV-файла на локальном диске

        #ДОБАВИТЬ ОСТАЛЬНЫЕ ТАБЛИЦЫ 
 # Сохранение CSV-файла на локальном диске
        save_path = '/home/maksat/golang/new/bridge'  # Замените на путь к желаемой папке сохранения
        file_name = 'generated_data.csv'
        file_path = os.path.join(save_path, file_name)
        #ДОБАВИТЬ ОСТАЛЬНЫЕ ТАБЛИЦЫ 
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'firstName', 'lastName', 'dateOfBirth', 'gender', 'email', 'phone', 'maritalStatus', 'income',
                'interests', 'languages', 'religionViews', 'politicalViews', 'mobilePhone', 'address', 'linkedAccounts',
                'website', 'placeOfWork', 'skills', 'university', 'faculty', 'currentCity', 'birthPlace', 'otherCities',
                'breifDescription', 'hobby', 'sport'
            ])
            writer.writerows(csv_data)

        return jsonify({'message': 'Файл сохранен успешно.'}), 200

    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

