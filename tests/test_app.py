from webtest import TestApp
from app import app


def test_index():
    webapp = TestApp(app)
    response = webapp.get("/")

    assert response.status_code == 200
    assert response.json == {"message": "hello world"}

    webapp.reset()


def test_signup():
    webapp = TestApp(app)

    username = "testsignup"
    password = "p455w0rd"

    response = webapp.post("/auth/signup", {"username": username, "password": password})

    assert response.status == "200 OK"
    assert response.json["username"] == username
    assert response.json["user_id"] == 1

    webapp.reset()


def test_webfinger():
    webapp = TestApp(app)

    username = "testwebfinger"
    password = "p455w0rd"
    domain = "oth.be"

    webapp.post("/auth/signup", {"username": username, "password": password})

    webfinger = webapp.get("/{0}/.well-known/webfinger".format(username))

    expected_webfinger = {
        "subject": "acct:{0}@{1}".format(username, domain),
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": "https://{0}/u/{1}".format(domain, username),
            }
        ],
    }

    assert webfinger.status == "200 OK"
    assert webfinger.json == expected_webfinger

    webapp.reset()
