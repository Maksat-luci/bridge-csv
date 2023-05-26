from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2 
import app
import os
from psycopg2 import sql



app = Flask(__name__)

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
        result = app.execute_query(query, (email,))

        if not result:
            return jsonify({'error': 'Email not found'}), 404

        query = sql.SQL("UPDATE settings SET {} = %s WHERE email = %s")
        query = query.format(sql.Identifier(category))
        app.execute_query(query, (settings_value, email))

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/get-profile-data', methods=['GET'])
def get_profile():
    auth_token = os.getenv('AUTH_TOKEN')

    if request.headers.get('Authorization') != auth_token:
        return jsonify({'error': 'Invalid token'}), 401
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415


    data = request.get_json()
    email = data.get('email')
    print(email)

    if not email:
        return jsonify({'error': 'Email parameter is missing'}), 400

    try:
        # Получение данных о профиле и связанных данных из других таблиц
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
        result = app.execute_query(query, ([email],))

        if not result:
            return jsonify({'error': 'No profile found for the provided email'}), 404

        # Преобразование результата запроса в словарь для удобного формата JSON
        print(result)
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

@app.route('/api/v1/update-csv', methods=['POST'])
def update_csv():
    if 'csv' not in request.files:
        return 'No file uploaded', 400
    
    csv_file = request.files['csv']
    csv_file.save(os.path.join(os.getcwd(), 'data.csv'))

    print("file saved")   
    updatepostgres()
    return "File saved and updated postgres", 200

def updatepostgres():
    db = Connect_db()
    print(db)
    print(app.Create_Table_Profile(db))
    print(app.Create_Table_BasicData(db))
    print(app.Create_Table_Contacts(db))
    print(app.Create_Table_WorkdAndEducation(db))
    print(app.Create_Table_PlaceOfResidence(db))
    print(app.Create_Table_PersonalInterested(db))
    print(app.Create_Table_DeviceInformation(db))
    print(app.Create_Table_Cookies(db))
    print(app.Create_Table_Settings(db))
    app.SaveDataInCsv(db)

# docker tag local-image:tagname new-repo:tagname
# docker push new-repo:tagname

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

