from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import psycopg2 
import db
import os
from psycopg2 import sql
import requests
from flasgger import Swagger

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Максимальный размер файла в байтах (здесь 16 МБ)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'swagger',
            "route": '/swagger.json',
            "rule_filter": lambda rule: True,  
            "model_filter": lambda tag: True,  
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger"
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
        SELECT p.id, p.firstName, p.lastName, p.dateOfBirth, p.gender, p.email, p.phone, p.maritalStatus, p.income,
               bd.interests, bd.languages, bd.religionViews, bd.politicalViews,
               c.mobilePhone, c.address, c.linkedAccounts, c.website,
               w.placeOfWork, w.skills, w.university, w.faculty,
               pr.currentCity, pr.birthPlace, pr.otherCities,
               pi.briefDescription, pi.hobby, pi.sport,
               di.operatingSystem, di.displayResolution, di.browser, di.ISP, di.adBlock,
               co.sessionState, co.language, co.region, co.recentPages, co.productId, co.productName, co.productPrice,
               co.quantity, co.subTotal, co.total, co.couponCode, co.shippingInformation, co.taxInformation
        FROM profile p
        LEFT JOIN basicData bd ON p.id = bd.profileId
        LEFT JOIN contacts c ON p.id = c.profileId
        LEFT JOIN workAndEducation w ON p.id = w.profileId
        LEFT JOIN placeOfResidence pr ON p.id = pr.profileId
        LEFT JOIN personalInterests pi ON p.id = pi.profileId
        LEFT JOIN deviceInformation di ON p.id = di.profileId
        LEFT JOIN cookies co ON p.id = co.profileId
        WHERE p.email = %s
        """
        result = db.execute_query(query, ([email],))

        if not result:
            return jsonify({'error': 'No profile found for the provided email'}), 404

        profile_data = {
            'profile': {
            'id': result[0][0],
            'firstName': result[0][1],
            'lastName': result[0][2],
            'dateOfBirth': str(result[0][3]),
            'gender': result[0][4],
            'email': result[0][5],
            'phone': result[0][6],
            'maritalStatus': result[0][7],
            'income': result[0][8],
            },

            'basicData': {
                'interests': result[0][9],
                'languages': result[0][10],
                'religionViews': result[0][11],
                'politicalViews': result[0][12]
            },
            'contacts': {
                'mobilePhone': result[0][13],
                'address': result[0][14],
                'linkedAccounts': result[0][15],
                'website': result[0][16]
            },
            'workAndEducation': {
                'placeOfWork': result[0][17],
                'skills': result[0][18],
                'university': result[0][19],
                'faculty': result[0][20]
            },
            'placeOfResidence': {
                'currentCity': result[0][21],
                'birthPlace': result[0][22],
                'otherCities': result[0][23]
            },
            'personalInterests': {
                'briefDescription': result[0][24],
                'hobby': result[0][25],
                'sport': result[0][26]
            },
            'deviceInformation': {
                'operatingSystem': result[0][27],
                'displayResolution': result[0][28],
                'browser': result[0][29],
                'ISP': result[0][30],
                'adBlock': result[0][31]
            },
            'cookies': {
                'sessionState': result[0][32],
                'language': result[0][33],
                'region': result[0][34],
                'recentPages': result[0][35],
                'productId': result[0][36],
                'productName': result[0][37],
                'productPrice': result[0][38],
                'quantity': result[0][39],
                'subTotal': result[0][40],
                'total': result[0][41],
                'couponCode': result[0][42],
                'shippingInformation': result[0][43],
                'taxInformation': result[0][44]
            }
        }

        return jsonify({'Data': profile_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/updatecsv', methods=['POST','GET'])
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
        dataset_name = request.form.get('datasetName')
        csv_file = request.files.get('csv')

        if csv_file is None:
            return 'No file uploaded', 400

        csv_file.save(os.path.join(os.getcwd(), csv_file.filename))

        print("file saved")   
        updatepostgres(csv_file.filename, dataset_name)
        SendPostRequest(dataset_name)

        return {"code":200, "response":"successfully"}
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
    print(db.Create_Table_Datasets(connect_db))
    print(db.Create_Table_Profile(connect_db))
    print(db.Create_Table_Credentials(connect_db))
    print(db.Create_Table_BasicData(connect_db))
    print(db.Create_Table_Contacts(connect_db))
    print(db.Create_Table_WorkdAndEducation(connect_db))
    print(db.Create_Table_PlaceOfResidence(connect_db))
    print(db.Create_Table_PersonalInterested(connect_db))
    print(db.Create_Table_DeviceInformation(connect_db))
    print(db.Create_Table_Cookies(connect_db))
    print(db.Create_Table_Settings(connect_db))
    db.SaveDataInCsv(connect_db,filenamecsv,dataset_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

