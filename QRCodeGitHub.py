import cv2
import time
import mysql.connector as mysql
from datetime import datetime
from pyzbar.pyzbar import decode

#
#Made by Pierre-Ardo PERON
#In 2021 for a college projet at ESME Sudria Paris
#

print("Starting the program")
# N° of second of delay
time.sleep(2)

#WebCam direct (take out "cv2.CAP_DSHOW" if you work on a raspberry, if you only have error webcam when you start the program it's doesn't work with certain camera)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#FPS settings
cap.set(cv2.CAP_PROP_FPS, 30.0)
#Put the video flow in MJPEG (compress the video in JPEG)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
#Resolation Width and Height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 540)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# N° of second of delay
time.sleep(1.0)

#If the camera is not detect
if (cap.isOpened()== False):
    print("Error webcam not detected")

#Decoding of the code with utf-8 normes
while (cap.isOpened()== True):
    ret, img = cap.read()
    if ret == True:
        for barcode in decode(img):
            #print(barcode.data)
            QRData = barcode.data.decode('utf-8')

            #Split the information give by QRcode every "++" signe
            Deku = QRData.split("++")
            LastNameClient = (Deku[0])
            NameClient = (Deku[1])
            EmailClient = (Deku[2])
            PhoneClient = (Deku[3])
            # N° d'attente avant lancement capture
            time.sleep(7.0)
            # verif
            print(Deku)

            #IP address of the SQL serveur
            HOST = '127.0.0.1'
            DATABASE = 'bdd'
            # User and Password
            USER = 'root'
            PASSWORD = ''

            #Connexion to MySQL
            bddConnect = mysql.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD
                )

            click = bddConnect.cursor()
            date_time = datetime.fromtimestamp(time.time())
            dateIns = date_time.strftime("%Y-%m-%d %H:%M:%S")
                #("%d-%m-%Y %H:%M:%S") coco rico vive la france

            #New user classe
            val_client = ("INSERT INTO cordonnee" "(Nom, Prenom, Email, date_entre, telephone)"
                                "VALUES (%(Nom)s, %(Prenom)s, %(Email)s, %(date_entre)s, %(telephone)s)")

            #Insert the information of the QRCode
            data_client = {
                'Nom': LastNameClient,
                'Prenom': NameClient,
                'Email': EmailClient,
                'date_entre': dateIns,
                'telephone': PhoneClient,
            }
            # N° of second of delay
            time.sleep(7.0)
            #Insert the command in the data base
            click.execute(val_client, data_client)
            #Close data base and curseur after the request
            bddConnect.commit()
            click.close()
            bddConnect.close()

        #Camera feedback
        cv2.imshow('Cam', img)

    #Press 'q' for closing the programme
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Program Close")
        break

#Quand tout est finie, relacher la capture vidéo
cap.release()
cv2.destroyAllWindows()


#OdanKey ( •̀ ω •́ )y
