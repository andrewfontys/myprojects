from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages, send_file, send_from_directory
import mysql.connector
import boto3
import json
import requests
import pymysql
import mysql.connector
import os
import csv
from pythonping import ping
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt, check_password_hash
import boto3
from botocore.exceptions import NoCredentialsError
from urllib.parse import quote_plus




dynamodb = boto3.resource()

dynamodb2 = boto3.resource(
                          )
s3 = boto3.client(
                     )
BUCKET_NAME1='asiadoctorbucket'
BUCKET_NAME2='europedoctorbucket'
BUCKET_NAME3='africadoctorbucket'
BUCKET_NAME4='northamericadoctorbucket'

table = dynamodb.Table('doctors')
# No longer used switched from dynamodb to RDS
#table2 = dynamodb2.Table('submissions')

# Connection to the AWS RDS
connection = mysql.connector.connect(
)

# Google Cloud Connection
db = pymysql.connect()

app = Flask(__name__)
app.secret_key = 'yomo'
bcrypt = Bcrypt(app)




@app.route('/')
def index():
    return render_template ('home.html')

@app.route("/aboutus")
def aboutus():
    return render_template ("aboutus.html")

@app.route("/services")
def services():
    return render_template ("services.html")

@app.route('/buckets')
def buckets():
    return render_template ("buckets.html")

@app.route("/asia")
def region1():
     # Check if the user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))

    # Check the role of the  user
    email = session['email']
    response = table.get_item(Key={'email': email})

    # Check if the 'Item' key is present in the response
    if 'Item' not in response:
        flash('User data not found.', 'error')
        return redirect(url_for('dashboard'))

    user_data = response['Item']

    # Check if the user is an admin or has location 'all'
    if user_data.get('role') == 'admin' or user_data.get('location') == 'all':
        # Render the page for admin users or users with location 'all'
        return render_template("asia.html", user_data=user_data)
    elif user_data.get('location') == 'asia':
        # Render the page for users with location 'asia'
        return render_template("asia.html", user_data=user_data)
    else:
        flash("You are not authorized to access this page.")
        return redirect(url_for('dashboard'))
    

@app.route("/europe")
def region2():
     # Check if the user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))

    # Check the role of the logged-in user
    email = session['email']
    response = table.get_item(Key={'email': email})

    # Check if the 'Item' key is present in the response
    if 'Item' not in response:
        flash('User data not found.', 'error')
        return redirect(url_for('dashboard'))

    user_data = response['Item']

    # Check if the user is an admin or has location 'all'
    if user_data.get('role') == 'admin' or user_data.get('location') == 'all':
        # Render the page for admin users or users with location 'all'
        return render_template("europe.html", user_data=user_data)
    elif user_data.get('location') == 'europe':
        # Render the page for users with location 'europe'
        return render_template("europe.html", user_data=user_data)
    else:
        flash("You are not authorized to access this page.")
        return redirect(url_for('dashboard'))
    

@app.route("/northamerica")
def region3():

    # Check if the user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))

    # Check the role of the logged-in user
    email = session['email']
    response = table.get_item(Key={'email': email})

    # Check if the 'Item' key is present in the response
    if 'Item' not in response:
        flash('User data not found.', 'error')
        return redirect(url_for('dashboard'))

    user_data = response['Item']

    # Check if the user is an admin or has location 'all'
    if user_data.get('role') == 'admin' or user_data.get('location') == 'all':
        # Render the page for admin users or users with location 'all'
        return render_template("northamerica.html", user_data=user_data)
    elif user_data.get('location') == 'america':
        # Render the page for users with location 'america'
        return render_template("northamerica.html", user_data=user_data)
    else:
        flash("You are not authorized to access this page.")
        return redirect(url_for('dashboard'))



@app.route("/africa")
def region4():
     # Check if the user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))

    # Check the role of the logged-in user
    email = session['email']
    response = table.get_item(Key={'email': email})

    # Check if the 'Item' key is present in the response
    if 'Item' not in response:
        flash('User data not found.', 'error')
        return redirect(url_for('dashboard'))

    user_data = response['Item']

    # Check if the user is an admin or has location 'all'
    if user_data.get('role') == 'admin' or user_data.get('location') == 'all':
        # Render the page for admin users or users with location 'all'
        return render_template("africa.html", user_data=user_data)
    elif user_data.get('location') == 'africa':
        # Render the page for users with location 'africa'
        return render_template("africa.html", user_data=user_data)
    else:
        flash("You are not authorized to access this page.")
        return redirect(url_for('dashboard'))

@app.route('/asiaupload',methods=['post'])
def useruploadasia():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME1,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "
    return render_template("asia.html",msg =msg)

@app.route('/europeupload',methods=['post'])
def useruploadeurope():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME2,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "
    return render_template("europe.html",msg =msg)

@app.route('/africaupload',methods=['post'])
def useruploadafrica():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME3,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "
    return render_template("africa.html",msg =msg)

@app.route('/northamericaupload',methods=['post'])
def useruploadna():
    if request.method == 'POST':
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME4,
                    Filename=filename,
                    Key = filename
                )
                msg = "Upload Done ! "
    return render_template("northamerica.html",msg =msg)

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connect to DynamoDB
        table = dynamodb.Table('doctors')

        # Read table for email
        response = table.query(
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )

        # Check if the email exists
        if 'Items' not in response or not response['Items']:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)

        user_data = response['Items'][0]

        # Check if the entered password matches the hashed password in the database
        if 'password' in user_data and check_password_hash(user_data['password'], password):
            session['email'] = email
            session['role'] = user_data.get('role')
            session['submitted_data'] = False

            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)

    else:
        return render_template('login.html')
    

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email exists
        table = dynamodb.Table('doctors')
        response = table.query(
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )

        if response.get('Items'):
            user_data = response['Items'][0]
            if user_data['password'] == password:
                session['email'] = email
                return redirect(url_for('dashboard'))
        
        # If email or password is invalid
        error = 'Invalid email or password'
        return render_template('dashboard.html', error=error)

    else:
        # Render the dashboard template with user data if needed
        return render_template('dashboard.html')
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        plain_password = request.form['password']
        role = request.form.get('role', 'user')  # Default role is 'user'
        location = request.form.get('location', '')  # Default location is an empty string

        # Check if the email already exists
        table = dynamodb.Table('doctors')
        try:
            response = table.query(
                KeyConditionExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )

            if response.get('Items'):
                error = 'Email already taken'
                return render_template('signup.html', error=error)

            # Hash the password before storing it
            hashed_password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

            # Insert the new user with hashed password, role, and location
            table.put_item(
                Item={
                    'email': email,
                    'password': hashed_password,
                    'role': role,
                    'location': location
                }
            )
            return redirect(url_for('dashboard'))

        except Exception as e:
            return render_template('signup.html', error='An error occurred while processing your request.')

    else:
        return render_template('signup.html')


@app.route('/grafana', methods=['GET', 'POST'])
def grafana():
    
    # Check if the user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))

    # Check the role of the user
    email = session['email']
    response = table.get_item(Key={'email': email})
    
    # Check if the 'Item' key is present in the response
    if 'Item' not in response:
        flash('User data not found.', 'error')
        return redirect(url_for('dashboard'))

    user_data = response['Item']

    # Check if the user is an admin
    if user_data.get('role') != 'admin':
        flash("You are not authorized to access this page.")
        return redirect(url_for('dashboard'))

    return render_template("grafana.html", user_data=user_data)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)  # Clear the session data
    return redirect(url_for('login'))

@app.route('/display')
def display_data():
    # Check if the user is authorized
    if 'email' not in session:
        return redirect(url_for('login'))

    email = session['email']
    response = table.get_item(Key={'email': email})

    if 'Item' not in response:
        flash('User data not found.', 'error')
        return redirect(url_for('dashboard'))

    user_data = response['Item']

    if user_data.get('role') != 'admin':
        flash("You are not authorized to access this page.")
        return redirect(url_for('dashboard'))
    
    # Fetch data from the 'doctors' table (DynamoDB)
    response_doctors = table.scan()
    doctors_data = response_doctors['Items']

    # Fetch data from the Submissions table (AWS RDS)
    try:
        cursor = connection.cursor()
        query_submissions = "SELECT company_name, company_mail, continent, region FROM Submissions"
        cursor.execute(query_submissions)
        submissions_data = cursor.fetchall()
        cursor.close()

        print(submissions_data)  # Add this line to check the content before rendering

        return render_template('displaydata.html', submissions=submissions_data, doctors=doctors_data)

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        flash("An error occurred while fetching data.", 'error')
        return redirect(url_for('dashboard'))

@app.route('/patients', methods=['POST', 'GET'])
def patients():
    if request.method == 'POST':
        patient_name = request.form['patientName']
        patient_info = request.form['patientInfo']

        with db.cursor() as cursor:
            cursor.execute('INSERT INTO patients (patientname, patientinfo) VALUES (%s, %s)', (patient_name, patient_info))
            db.commit()

    cursor = db.cursor()
    cursor.execute('SELECT patientname, patientinfo FROM patients')
    patients_data = cursor.fetchall()
    return render_template('patients.html', patients=patients_data)

@app.route('/deletePatient', methods=['POST'])
def delete_patient():
    patient_name = request.form['patientName']
    patient_info = request.form['patientInfo']
    print("Received Patient Name:", patient_name)
    print("Received Patient Info:", patient_info)

    with db.cursor() as cursor:
        cursor.execute('DELETE FROM patients WHERE patientname = %s AND patientinfo = %s', (patient_name, patient_info))
        db.commit()

    return redirect(url_for('patients'))

@app.route('/updatePatient', methods=['POST'])
def update_patient():
    patient_name = request.form['patientName']
    updated_patient_info = request.form['patientinfo']

    with db.cursor() as cursor:
        cursor.execute('UPDATE patients SET patientinfo = %s WHERE patientname = %s', (updated_patient_info, patient_name))
        db.commit()

    # Fetch all patients after the update
    cursor = db.cursor()
    cursor.execute('SELECT patientname, patientinfo FROM patients')
    patients_data = cursor.fetchall()

    return render_template('patients.html', patients=patients_data)

def generate_aws_credentials(company_name):
    print(f"Generating AWS credentials for {company_name}")

    aws_access_key_id = 'A'
    aws_secret_access_key = 'd'

    # Initialize the IAM client
    iam_client = boto3.client('iam', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Create a new IAM user with the email as the username
    response = iam_client.create_user(UserName=company_name)

    # Add the IAM user to the IAM group 'DoctorsOnTheMove'
    iam_client.add_user_to_group(UserName=company_name, GroupName='DoctorsOnTheMove')  
    print(f"AWS user created and added to IAM group successfully: {company_name}")

    # Create an access key for the user
    access_key_response = iam_client.create_access_key(UserName=company_name)
    
    # Display the generated AWS credentials
    access_key_id = access_key_response['AccessKey']['AccessKeyId']
    secret_access_key = access_key_response['AccessKey']['SecretAccessKey']

    print(f"Access Key ID: {access_key_id}")
    print(f"Secret Access Key: {secret_access_key}")

    # Write the generated AWS credentials to a CSV file
    csv_filename = f"{company_name}.csv"
    with open(csv_filename, 'w', newline='') as csv_file:
        fieldnames = ['AccessKeyId', 'SecretAccessKey']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'AccessKeyId': access_key_id, 'SecretAccessKey': secret_access_key})

    print(f"AWS credentials written to CSV file: {csv_filename}")

    # Store the CSV filename in the session
    session['csv_filename'] = csv_filename
    print(f"AWS credentials stored in session for {company_name}")

    # Return the generated AWS credentials as a dictionary
    return {
        'AccessKeyId': access_key_id,
        'SecretAccessKey': secret_access_key,
        'csv_filename': csv_filename  
    }


@app.route('/process_submission', methods=['POST', 'GET'])
def submission():
    global connection  
    
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        region = request.form.get('region')
        continent = request.form.get('continent')
        company_mail = request.form.get('company_mail')
        submission_url = "https://1lrbxiez42.execute-api.eu-central-1.amazonaws.com/prod"
        data = {
                "input": "{\"region\": \"" + region + "\"}",
                "stateMachineArn": "arn:aws:states:eu-central-1:452220760922:stateMachine:MyStateMachine-p06y8gn0e"
        }
        
        json_string = json.dumps(data)
        response = requests.post(submission_url, data=json_string, headers={'Content-Type': 'application/json'})
        print(json_string)

        aws_credentials = None  # Initialize aws_credentials 

        try:
            cursor = connection.cursor()

            # Process the data and insert it into the database
            cursor.execute("INSERT INTO Submissions (company_name, company_mail, region, continent) VALUES (%s, %s, %s, %s)",
                           (company_name, company_mail, region, continent))
            connection.commit()

            # Call the function to generate AWS credentials
            aws_credentials = generate_aws_credentials(company_name)

            if aws_credentials:
                session['aws_credentials'] = aws_credentials
            else:
                # Handle the case where credentials are not generated successfully
                return render_template('submission.html', error_message="Failed to generate AWS credentials.")
            
            # Redirect to thank you page
            return redirect(url_for('thank_you'))
        except Exception as e:
            # Handle exceptions (print or log the error)
            print(f"Error: {e}")
            # Display an error message on the same page
            return render_template('submission.html', error_message="An error occurred while processing your submission.")
        finally:
            # Close the cursor (not the connection) after executing queries
            if 'cursor' in locals():
                cursor.close()

    else:
        return render_template('submission.html')
    

@app.route('/download_csv')
def download_csv():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    aws_credentials = session.get('aws_credentials')

    if aws_credentials:
        # Retrieve the CSV file path from the session
        csv_filename = aws_credentials.get('csv_filename', None)

        if csv_filename:
            return send_file(csv_filename, as_attachment=True)
        
    return "File not found"

@app.route('/thank_you')
def thank_you():
    if 'email' not in session:
        return redirect(url_for('login'))

    return render_template('thankyou.html')

# Dictionary to store host stats
host_stats = {}

def check_host(host):
    try:
        response = ping(host, count=4)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if host not in host_stats:
            host_stats[host] = {
                'last_seen': now,
                'uptime': 0,
                'rtt_avg': 'N/A',
                'packet_loss': 'N/A'
            }

        if response.success():
            last_seen = now
            if host_stats[host]['last_seen'] != last_seen:
                uptime_increment = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S") - datetime.strptime(host_stats[host]['last_seen'], "%Y-%m-%d %H:%M:%S")
                host_stats[host]['uptime'] += uptime_increment.total_seconds()
                host_stats[host]['last_seen'] = last_seen
            
            host_stats[host]['rtt_avg'] = response.rtt_avg if hasattr(response, 'rtt_avg') else 'N/A'
            host_stats[host]['packet_loss'] = response.packet_loss if hasattr(response, 'packet_loss') else 'N/A'

            return {
                'host': host,
                'success': True,
                'last_seen': host_stats[host]['last_seen'],
                'uptime': int(host_stats[host]['uptime']),
                'rtt_avg': host_stats[host]['rtt_avg'],
                'packet_loss': host_stats[host]['packet_loss']
            }
        else:
            return {
                'host': host,
                'success': False,
                'last_seen': host_stats[host]['last_seen'],
                'uptime': int(host_stats[host]['uptime']),
                'rtt_avg': host_stats[host]['rtt_avg'],
                'packet_loss': host_stats[host]['packet_loss']
            }
    except Exception as e:
        return {
            'host': host,
            'success': False,
            'last_seen': 'N/A',
            'uptime': 0,
            'rtt_avg': 'N/A',
            'packet_loss': 'N/A',
            'error': str(e)
        }

@app.route('/stats')
def monitoring_page():
        # Check if the user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))


    # Check if user is admin
    email = session['email']
    response = table.get_item(Key={'email': email})
    user_data = response['Item']

    if user_data.get('role') != 'admin':
        flash("You are not authorized to access this page.")
        return redirect(url_for('dashboard'))

    # Check the role of the logged-in user
    email = session['email']
    response = table.get_item(Key={'email': email})
    # Check if the 'Item' key is present in the response
    if 'Item' not in response:
        flash('User data not found.', 'error')
        return redirect(url_for('dashboard'))
    hosts = ['18.198.226.108', '35.156.74.108', 'doctorsonthemove.org']
    ping_results = []
    for host in hosts:
        result = check_host(host)
        ping_results.append(result)
    return render_template('monitoring.html', ping_results=ping_results)

 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
