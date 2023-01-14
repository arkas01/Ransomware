import os
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP,AES

privatekeyFile='private.pem'

def scanRecurse(baseDir):
    for entry in os.scandir(baseDir):
        if entry.is_file():
            yield entry
        else:
            yield from scanRecurse(entry.path)
            
def dec(dataFile,privatekeyFile):
    extension= '.jpeg'
    
    with open(privatekeyFile,'rb') as f:
        privateKey=f.read()
        key=RSA.import_key(privateKey)
    
    with open(dataFile,'rb') as f:
        encryptedSessionKey,nonce,tag,ciphertext=[f.read(x) for x in(key.size_in_bytes(),16,16,-1)]
    
    cipher=PKCS1_OAEP.new(key)    
    sessionKey =cipher.decrypt(encryptedSessionKey)
    
    # decrypt the data with the session key
    
    cipher=AES.new(sessionKey,AES.MODE_EAX,nonce)
    data=cipher.decrypt_and_verify(ciphertext,tag)
    
    #save decrypted data to the file
    
    dataFile=str(dataFile)
    fileName=dataFile.split(extension)[0]
    fileExtension='.decrypted'
    decryptfile=fileName+fileExtension
    with open(decryptfile,'wb') as f:
        f.write(data)
        
    print('Decrypted file saved to' + decryptfile)
    
directory='/home/kali/Desktop/'
includeExtension=['.jerarice']
    
for item in scanRecurse(directory):
    filePath=Path(item)
    fileType=filePath.suffix.lower()
    if fileType in includeExtension:
        dec(filePath, privatekeyFile)
        
        