import base64
from cloud_browser.services.aws.base import BaseAwsService

class KeyManagementServiceService(BaseAwsService):
    def __init__(self, region) -> None:
        super().__init__('kms', region)

    def decrypt(self, ciphertext: str, encryption_context: dict = None) -> str:
        try:
            b64 = base64.b64decode(ciphertext)
            response = None

            if encryption_context: response = self.client.decrypt(CiphertextBlob = b64, EncryptionContext = encryption_context)
            else: response = self.client.decrypt(CiphertextBlob = b64)

            return response['Plaintext'].decode()
        except Exception as e:
            raise(e)

    def encrypt(self, key: str, plaintext: str, encryption_context: dict = None) -> str:
        try:
            b = bytes(plaintext, encoding = 'utf8')
            response = None

            if encryption_context: response = self.client.encrypt(KeyId = key, Plaintext = b, EncryptionContext = encryption_context)
            else: response = self.client.encrypt(KeyId = key, Plaintext = b)

            return base64.b64encode(response['CiphertextBlob']).decode()
        except Exception as e:
            raise(e)
