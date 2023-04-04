from flaskr import create_app
import shutil

import pytest
import io


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'LOGIN_DISABLED': True,
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.


def test_good():
    assert True


def integration_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Star Wars Wiki" in resp.data


def integration_signup(client):
    resp = client.get("/signup")
    assert resp.status_code == 200
    assert b"Sign up" in resp.data


def integration_login(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Log in" in resp.data


def integration_pages(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Pages Contained in this Wiki" in resp.data


def integration_upload(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"Select a file to upload (md, jpg, png, gif, zip)" in resp.data


def integration_upload_submit_wrong_format(client):
    file_name = "flower.txt"
    data = {'file': (io.BytesIO(b"some initial text data"), file_name)}
    resp = client.post("/upload/upload_submit", data=data)
    assert resp.status_code == 200
    assert b"Incorrect file format or file not selected" in resp.data


# TODO(Project 1): Write tests for other routes.
