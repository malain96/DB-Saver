import base64


class Cipher:
    # Class variables
    key = ""

    # Init
    def __init__(self, key):
        self.key = key

    # Return an encoded clear text
    def encode(self, clear):
        try:
            enc = []
            for i in range(len(clear)):
                key_c = self.key[i % len(self.key)]
                enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
                enc.append(enc_c)
            return base64.urlsafe_b64encode("".join(enc).encode()).decode()
        except BaseException as error:
            code, message = error.args
            print("Unexpected error", code, ":", message)
            raise

    # Return a decoded text
    def decode(self, enc):
        try:
            dec = []
            enc = base64.urlsafe_b64decode(enc).decode()
            for i in range(len(enc)):
                key_c = self.key[i % len(self.key)]
                dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
                dec.append(dec_c)
            return "".join(dec)
        except BaseException as error:
            code, message = error.args
            print("Unexpected error", code, ":", message)
            raise
