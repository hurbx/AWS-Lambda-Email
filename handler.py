import pymysql
from datetime import datetime
from pytz import timezone
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



endpoint = 'endpoint'
username = 'username'
password = 'pass'
database_name = 'db_name'

connection = pymysql.connect(host=endpoint, user=username,
                             password=password, db=database_name)


def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name'] 
    key = event['Records'][0]['s3']['object']['key'] 
    
    chile = timezone('America/Santiago')
    chileDate = datetime.now(chile)
    final = chileDate.strftime('%d/%m/%Y %H:%M')
   
    
  
    
    sniffer = key.split('/')[0]

    cursor = connection.cursor()
    cursor.execute('INSERT INTO h_RebornTelemetry_t_datacheckups (check_file_name, creation_date, sniffer) VALUE (%s, %s, %s)',(key, final, sniffer))
 
    
    connection.commit()

    msg = MIMEMultipart()
    message = "El vehiculo con sniffer "+" "+ sniffer +" "+ " subio un archivo a AWS\n" + "el path del archivo es " +" "+ key
    password = 'zyhhy4-dofher-dusgUt'
    msg['From'] = 'hurbina@rebornelectric.cl'
    msg['To'] = 'hugo.urbina@mayor.cl'
    msg['Subject'] = 'nuevo archivo en S3 de '+" "+ sniffer 
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(['From'], msg['To'], msg.as_string())
    server.quit()

    print('ok')


    


