import base64
import hashlib

from Cryptodome.Cipher import AES
from django.conf import settings


class AESCipher:
    def __init__(self):
        self.BS = 16
        self.pad = lambda s: s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)
        self.unpad = lambda s: s[0:-s[-1]]
        self.key = hashlib.sha256(settings.SECRET_KEY.encode('utf-8')).digest()
        self.iv = settings.IV.encode('utf-8')

    def encrypt(self, raw):
        if raw is None:
            data = None
        else:
            raw = raw.encode('utf-8')
            raw = base64.b64encode(raw)
            raw = raw.decode('utf-8')
            raw = self.pad(raw).encode('utf-8')
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            data = base64.b64encode(self.iv + cipher.encrypt(raw))
        return data

    def encrypt_str(self, row):
        if not row:
            return row
        return self.encrypt(row).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))

    def decrypt_str(self, enc):
        if enc is None:
            data = None
        else:
            if type(enc) == str:
                enc = str.encode(enc)
            enc = self.decrypt(enc).decode('utf-8')
            enc = base64.b64decode(enc)
            data = enc.decode('utf-8')
        return data
