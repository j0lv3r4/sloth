import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def create_key_pair():
    key = rsa.generate_private_key(
        backend=default_backend(), public_exponent=65537, key_size=2048
    )

    private_key = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )

    public_key = key.public_key().public_bytes(
        serialization.Encoding.OpenSSH, serialization.PublicFormat.OpenSSH
    )

    return (private_key, public_key)


def get_actor(username, domain, pubkey):
    return json.dumps(
        {
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1",
            ],
            "id": "https://{0}/u/{1}".format(domain, username),
            "type": "Person",
            "name": "",
            "summary": "",
            "preferredUsername": username,
            "following": "https://{0}/u/{1}/following".format(domain, username),
            "followers": "https://{0}/u/{1}/followers".format(domain, username),
            "inbox": "https://{0}/u/{1}/inbox".format(domain, username),
            "outbox": "https://{0}/u/{1}/outbox".format(domain, username),
            "publicKey": {
                "id": "https://{0}/u/{1}#main-key".format(domain, username),
                "owner": "https://{0}/u/{1}".format(domain, username),
                "publicKeyPem": pubkey,
            },
        }
    )


def get_webfinger(username, domain):
    return json.dumps(
        {
            "subject": "acct:{0}@{1}".format(username, domain),
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": "https://{0}/u/{1}".format(domain, username),
                }
            ],
        }
    )

