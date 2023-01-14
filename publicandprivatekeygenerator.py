import crypto
from Crypto.PublicKey import RSA

key =RSA.generate(2048)
privatekey=key.export_key()
publickey=key.publickey().export_key()

with open('private.pem','wb') as f:
    f.write(privatekey)

with open('public.pem','wb') as f:
    f.write(publickey)
    
print('Private Key saved to privatekey.pem')
print('public Key saved to publickey.pem')
print('done')