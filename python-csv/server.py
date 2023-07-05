from flask import Flask, redirect, request, jsonify,render_template, render_template_string
from flask_cors import CORS
import psycopg2 
import db
import os
from psycopg2 import sql
import requests
from flasgger import Swagger
import mapper
import json
import hashlib
from cryptography.fernet import Fernet
import base64
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
        query = sql.SQL("SELECT * FROM settings WHERE email = %s")
        result = db.execute_query(query, (email,))

        if not result:
            return jsonify({'error': 'Email not found'}), 404

        query = sql.SQL("UPDATE settings SET {} = %s WHERE email = %s")
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
        SELECT p.id, p.firstname, p.lastname, p.dateofbirth, p.gender, p.email, p.phone, p.maritalstatus, p.income,
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
        WHERE p.email = %s
        """
        result = db.execute_query(query, ([email],))

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
                'adBlock': hash_data(result[0][31])
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
        decrypted_profile_data = decrypt_dict_values(profile_data)
        return jsonify({'Data': profile_data, "encrypted": decrypted_profile_data}), 200

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
        # Преобразуйте данные в формат JSON
        credentials_json = []
        for credential in credentials:
            credential_data = {
                'profileId': credential[1],
                'emails': credential[2],
                'phones': credential[3]
            }
            credentials_json.append(credential_data)
        
        # Отправьте данные в ответе в формате JSON
        return jsonify({'credentials': credentials_json})
    except psycopg2.Error as e:
        print("Error retrieving credentials:", e)
        return 'Error retrieving credentials', 500
    
    finally:
        cursor.close()
        conn.close()



def updatepostgres(filenamecsv,dataset_name):
    connect_db = Connect_db()
    print(connect_db)
    db.SaveDataInCsv(connect_db,filenamecsv,dataset_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

