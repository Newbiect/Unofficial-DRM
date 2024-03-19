import gnupg
import getpass

gpg = gnupg.GPG()
company_email = input("Enter the company email address: ")
user_name = input("Enter your name: ")
user_email = input("Enter your email address: ")
passphrase = getpass.getpass("Enter a passphrase for the PGP key: ")

# Generate the PGP key pair
key_input = gpg.gen_key_input(
    name_email=user_name,
    expire_date=0,
    passphrase=passphrase,
    key_type="RSA",
    key_length=2048,
    subkey_type="RSA",
    subkey_length=2048,
    cert_expire_date=0,
    sign_key=True,
    encrypt_key=True,
    auth_key=True,
    primary_uid=True,
    primary_uid_name=True,
    primary_uid_email=True,
    primary_uid_comment=True,
    primary_uid_url=False,
    subkey_sign_key=False,
    subkey_encrypt_key=False,
    subkey_auth_key=False,
    subkey_primary_uid=False,
    subkey_primary_uid_name=False,
    subkey_primary_uid_email=False,
    subkey_primary_uid_comment=False,
    subkey_primary_uid_url=False,
)
key = gpg.gen_key(key_input)

print("\nPublic Key:")
print(gpg.export_keys(key.fingerprint))

print("\nPrivate Key:")
print(gpg.export_keys(key.fingerprint, True))

print("\nPassphrase:")
print(passphrase)

with open("public_key.asc", "w") as f:
    f.write(gpg.export_keys(key.fingerprint))

with open("private_key.asc", "w") as f:
    f.write(gpg.export_keys(key.fingerprint, True))
