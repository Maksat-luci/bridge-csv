from flask import Flask, request
import os
import csv

app = Flask(__name__)

@app.route('/updatecsv', methods=['POST'])
def update_csv():
    print(request.files)
    if 'csv' not in request.files:
        return 'No file uploaded', 400

    csv_file = request.files['csv']
    csv_file.save(os.path.join(os.getcwd(), 'data.csv'))
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)

    return 'File saved', 200


if __name__ == '__main__':
    app.run(debug=True, port=8000)