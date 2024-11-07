import cv2 
import numpy as np
import urllib.request
from pushbullet import PushBullet
import time

global time_cat 
global time_dog
global time_person

time_cat = 0
time_dog = 0
time_person = 0

access_token = "o.4W7lcFwEL5UWBz7GdfDsONwQ3QtdQ59Z"

data = "Camera de supraveghere"
text_pisica = "Alerta pisica."
text_caine = "Alerta caine."
text_persoana = "Alerta persoana."

# de la acest url va prelua imaginile
url = 'http://10.41.161.103/cam-hi.jpg'

# o variabila cap de tip "capture object" care capteaza frame-uri de la url
cap = cv2.VideoCapture(url)

# dimensiunea patratului maxim in care intra un obiect de interes
whT = 320
# thresholdul peste care se afiseaza apartenenta la o clasa
# daca algoritmul este peste 50% sigur de obiect se afiseaza
confThreshold = 0.5

# un coeficient care elimina redundanta: daca sunt 2 sau mai multe obiecte se suprapun
# ele sunt retinute si sortate in functie de scorul de incredere
# daca setam acest coeficient ca fiind mai mic, se elimina mai puternic obiectele suprapuse
# insa este posibil sa se elimine si detectii valide. Daca este mai mare, este posibil
# sa priveasca acelasi obiect ca pe 2 obiecte diferite
nmsThreshold = 0.3

# fisierul unde sunt stocate numele claselor
classesfile = "C:/Users/Violeta/Desktop/AMp/coco.names"

# o lista unde se vor stoca numele obiectelor din fisierul de mai sus
classNames = []

# populam lista
with open(classesfile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# incarcam modelul YOLO
modelConfig = "C:/Users/Violeta/Desktop/AMp/yolov3.cfg"
modelWeights = "C:/Users/Violeta/Desktop/AMp/yolov3.weights"

# obiectul net reprezinta modelul nostru. Este incarcat din cele 2 fisiere
net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)

# seteaza backend-ul preferat- cine ruleaza reteaua neurala (o alternativa ar fi CUDA)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

# seteaza componenta hardware care se ocupa de partea computationala.
# se alege CPU-ul pentru portabilitate (alternativa: GPU)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# functia care foloseste modelul caruia i-am facut setup mai sus
# pentru detectia de obiecte in fluxul video
# are ca parametri: o variabila outputs- contine rezultate ale detectiei
# si im - frame-ul
def findObject(outputs, im):

    # variabile care vor numara in cate cadre apar anumite obiecte
    global time_cat
    global time_dog
    global time_person
    
    # extragem dimensiunile imaginii im: inaltime, latime si nr de canale
    hT, wT, cT = im.shape

    # initializam cateva liste pentru detectia de obiecte: bounding boxurile,
    # id-urile de clasa si confidece scorurile
    bbox = []
    classIds = []
    confs = []

    # loop pentru detectie- trece prin fiecare output layer si fiecare detectie din 
    # fiecare output layer
    for output in outputs:
        for det in output:

            # sse extrag info despre fiecare detectie in parte
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            
            # daca se gaseste ceva peste pragul de incredere
            if confidence > confThreshold:

                # se calculeaza colturile bounding- boxurilor si se adauga la lista de bb-uri
                # det[2] = latimea, det[3] = inaltimea bb-ului prezisa de reteaua neurala
                # asa ca se scaleaza imaginea
                w, h = int(det[2] * wT), int(det[3] * hT)

                # det[0] = coordonata x a bb si det[1] coordonata y
                # x, y reprezinta coordonatele bb-ului (coltul stanga sus)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
               
                # adaug in liste informatii
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    # se aplica Non- Maximum Supression ca sa filtreze obiectele gasite si sa lase cele mai relevante date
    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

    # daca un obiect e detectat se fac bb-urile si se masoara in cate frame-uri apar
    # + se trimit sms-urile
    if len(indices) > 0:  
        for i in indices.flatten():
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            if classNames[classIds[i]] == 'dog':
                time_dog = time_dog + 1
                  
            elif classNames[classIds[i]] == 'cat':
                time_cat = time_cat + 1
                print(" ")
                print(time_cat)

            elif classNames[classIds[i]] == 'person':
                time_person = time_person + 1

            if classNames[classIds[i]] == 'dog':
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv2.putText(im, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%', (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            if classNames[classIds[i]] == 'cat':
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv2.putText(im, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%', (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                
            if classNames[classIds[i]] == 'person':
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 255), 2)
                cv2.putText(im, f'{classNames[classIds[i]].upper()} {int(confs[i] * 100)}%', (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            if time_cat == 20:
                pb = PushBullet(access_token)
                push = pb.push_note(data, text_pisica)

            if time_dog == 20:
                pb = PushBullet(access_token)
                push = pb.push_note(data, text_caine)

            if time_person == 20:
                pb = PushBullet(access_token)
                push = pb.push_note(data, text_persoana)

while True:
    # se ia o imagine de la url
    img_resp = urllib.request.urlopen(url)
    # se converteste intr-un format numeric
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    # converteste imaginea din format numeric intr-un format pentru opencv
    im = cv2.imdecode(imgnp, -1)
    # se intoarce imaginea cu fundul in jos pentru o asezare mai usoara a hardware-ului
    im = cv2.flip(im, 0)

    #success, img = cap.read()
    # un obiect de tip blob (binary large object) e creat din imaginea preluata de la url
    blob = cv2.dnn.blobFromImage(im, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
    # acest blob e setat ca input pentru reteaua neurala cu numele "net"
    net.setInput(blob)

    # in outputNames se pun numele straturilor de output ale modelului
    outputNames = net.getUnconnectedOutLayersNames()
    # se retin in outputs datele ce ies din straturile de iesire
    outputs = net.forward(outputNames)

    # se apeleaza functia 
    findObject(outputs, im)

  
 
    cv2.waitKey(1)