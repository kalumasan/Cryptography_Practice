from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID,ExtensionOID
from cryptography.hazmat.primitives import hashes
from datetime import datetime,timedelta

privateKeyFile='./cert/privateKey.pem'
certificateFile='./cert/selfsignedCertificate.pem'

def generatePrivateKey():
    keyString=rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    with open(privateKeyFile,'wb')as f:
        f.write(
            keyString.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    return keyString

def generateCertificate():
    keyString=generatePrivateKey()
    subjectInfo=issuer=x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u'CN'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'BeiJing'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u'BeiJing'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'getuplate'),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'getuplate'),
        x509.NameAttribute(NameOID.COMMON_NAME, u'www.cuccloud.getuplate.com'),
        x509.NameAttribute(ExtensionOID.SUBJECT_ALTERNATIVE_NAME, u'DNS:www.cuccloud.getuplate.com'),
    ])
    certString=x509.CertificateBuilder().subject_name(subjectInfo).issuer_name(issuer).public_key(keyString.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow()+timedelta(days=10)).add_extension(x509.SubjectAlternativeName([x509.DNSName(u'pan.c919.com')]), critical=False).sign(keyString, hashes.SHA512())
    with open(certificateFile,'wb')as f:
        f.write(certString.public_bytes(serialization.Encoding.PEM))
    return certString

if __name__=='__main__':
    generateCertificate()
    print('generate certificate success')
