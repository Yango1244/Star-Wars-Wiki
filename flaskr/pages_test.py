from flaskr import create_app
import shutil

from unittest.mock import patch

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


def home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Star Wars Wiki" in resp.data


def test_signup(client):
    resp = client.get("/signup")
    assert resp.status_code == 200
    assert b"Sign up" in resp.data


def test_login(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Log in" in resp.data


@patch('flaskr.backend.Backend.sign_in')
def test_login_successful(mock_sign_in, client):
    username = "Test User"
    password = "some password"
    mock_sign_in.return_value = True
    resp = client.post("/login/validate",
                       data={
                           "username": username,
                           "password": password
                       })
    assert resp.status_code == 200
    assert b"Log in Success" in resp.data
    assert b"Welcome back, Test User!" in resp.data


@patch('flaskr.backend.Backend.get_all_page_names')
def test_pages(mock_get_all_page_names, client):
    mock_get_all_page_names.return_value = ([], [])
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Pages Contained in this Wiki" in resp.data


def test_upload(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"Select a file to upload (md, jpg, png, gif, zip)" in resp.data


@patch('flaskr.backend.Backend.upload')
def test_upload_submit_wrong_format(mock_upload, client):
    mock_upload.return_value = "Failure"
    file_name = "flower.txt"
    data = {'file': (io.BytesIO(b"some initial text data"), file_name)}
    resp = client.post("/upload/upload_submit", data=data)
    assert resp.status_code == 200
    assert b"Incorrect file format or file not selected" in resp.data


@patch('flaskr.backend.Backend.change_profile')
def test_edit_profile_success(mock_profile, client):
    mock_profile.return_value = "Success"
    with client.session_transaction() as sess:
        sess['username'] = 'Tim'

    new_password = "test_pass"
    profile_pic = (io.BytesIO(b"some initial text data"), "profile_pic.jpg")
    banner_pic = (io.BytesIO(b"some initial text data"), "banner_pic.jpg")
    bio = "This is a test bio"

    data = {
        "new_password": new_password,
        "profile_pic": profile_pic,
        "banner_pic": banner_pic,
        "bio": bio
    }

    resp = client.post("/edit_profile/submit", data=data)
    assert resp.status_code == 200
    assert b"Profile successfully updated" in resp.data


@patch('flaskr.backend.Backend.change_profile')
def test_edit_profile_failure(mock_profile, client):
    mock_profile.return_value = "Failure"
    with client.session_transaction() as sess:
        sess['username'] = 'Tim'

    new_password = "test_pass"
    profile_pic = (io.BytesIO(b"some initial text data"), "profile_pic.exe")
    banner_pic = (io.BytesIO(b"some initial text data"), "banner_pic.exe")
    bio = "This is a test bio"

    data = {
        "new_password": new_password,
        "profile_pic": profile_pic,
        "banner_pic": banner_pic,
        "bio": bio
    }

    resp = client.post("/edit_profile/submit", data=data)
    assert resp.status_code == 200
    assert b"Wrong file format chosen" in resp.data


@patch('flaskr.backend.Backend.get_users')
def test_profiles(mock_users, client):
    mock_users.return_value = []
    resp = client.get("/profiles")
    assert resp.status_code == 200
    assert b"User profiles" in resp.data


@patch('flaskr.backend.Backend.get_users')
def test_user_profile_invalid_user(mock_users, client):
    mock_users.return_value = ["yinka23", "Blake33", "Bart"]
    resp = client.get("/profiles/bobby34")
    assert resp.status_code == 200
    assert b"User does not exist" in resp.data


@patch('flaskr.backend.Backend.get_bio')
@patch('flaskr.backend.Backend.get_banner_pic')
@patch('flaskr.backend.Backend.get_profile_pic')
@patch('flaskr.backend.Backend.get_users')
def test_user_profile_valid_user(mock_users, mock_profile_pic, mock_banner_pic,
                                 mock_bio, client):
    mock_users.return_value = ["yinka23", "Blake33", "Bart"]
    mock_profile_pic.return_value = "/fakeurl.png"
    mock_banner_pic.return_value = "/fakeurl.png"
    mock_bio.return_value = "Test bio"

    resp = client.get("/profiles/yinka23")
    assert resp.status_code == 200
    assert b"yinka23" in resp.data


def test_edit_profile(client):
    resp = client.get("/edit_profile")
    assert resp.status_code == 200
    assert b"Manage Your Profile" in resp.data


def test_character_profile_failed(client):
    resp = client.get("/character_profile<name>")
    assert resp.status_code == 200
    assert b"That character doesn't exist" in resp.data


def test_character_profile_passed(client):
    resp = client.get("/character_profile<Anakin Skywalker>")
    assert resp.status_code == 200
    assert b"Profile:" in resp.data


# TODO(Project 1): Write tests for other routes.
