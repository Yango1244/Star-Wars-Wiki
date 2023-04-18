from flaskr.backend import Backend

from unittest import mock
from unittest.mock import MagicMock, Mock, patch

from google.cloud import storage
from google.cloud.storage.bucket import Bucket

import pytest


@pytest.fixture
def file_stream():
    return MagicMock()


@pytest.fixture
def blob(file_stream):
    blob = MagicMock()
    blob.open.return_value.__enter__.return_value = file_stream
    return blob


def make_bucket(blob):
    bucket = MagicMock()
    bucket.get_blob.return_value = blob
    bucket.blob.return_value = blob

    return bucket


def sha256(return_value):
    s = MagicMock()
    s.hexdigest.return_value = return_value
    return s


@pytest.fixture
def page_bucket(blob):
    return make_bucket(blob)


@pytest.fixture
def login_bucket(blob):
    return make_bucket(blob)

@pytest.fixture
def user_bucket(blob):
    return make_bucket(blob)


@pytest.fixture
def backend(page_bucket, login_bucket, user_bucket):
    storage_client = MagicMock()
    storage_client.bucket = Mock()
    storage_client.bucket.side_effect = [page_bucket, login_bucket, user_bucket]
    return Backend(storage_client=storage_client)


def test_sign_up_add_user(backend, login_bucket):
    login_bucket.get_blob.return_value = None

    backend.sign_up("Capy", "CapybaraLove")
    login_bucket.blob.assert_called_once_with('Capy')


def test_sign_up_user_exists(backend, login_bucket):
    # Blob will exist so we expect to only call get_blob once
    login_bucket.get_blob.return_value = True

    backend.sign_up("Capy", "CapybaraLove")
    login_bucket.get_blob.assert_called_once_with('Capy')
    assert not login_bucket.blob.called


def test_sign_in_user_incorrect(backend, login_bucket):
    # Blob won't exist so we expect to return False
    login_bucket.get_blob.return_value = None
    assert not backend.sign_in("Capy", "CapyWrong")


@mock.patch('flaskr.backend.blake2s')
def test_sign_in_user_correct(mock_blake, backend, login_bucket):
    mock_digest = Mock()
    mock_blake.return_value = mock_digest
    mock_bucket = Mock()
    mock_blob = Mock()
    mock_file = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file)
    mock_open.__exit__ = Mock(return_value=None)
    login_bucket.return_value = mock_bucket
    login_bucket.get_blob.return_value = mock_blob
    mock_blob.open.return_value = mock_open
    mock_file.read.return_value = "Correct"
    mock_digest.hexdigest.return_value = "Correct"

    assert backend.sign_in("Capy", "CapyRight")


def integration_sign_in(backend):
    assert backend.sign_in("Capy", "CapybaraLove")


# def get_image(backend):
#     # integration test
#     assert backend.get_image("LeroneJoyner.jpg")


def test_upload_empty_file(backend):
    mock_file_obj = Mock()
    assert backend.upload("", mock_file_obj) == "Failure"


def test_upload_wrong_format(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)

    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.upload("Luke.exe", mock_file_obj) == "Failure"


def test_upload_single_file(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)

    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.upload("test.md", mock_file_obj) == "Success"


@mock.patch('flaskr.backend.os')
@mock.patch('flaskr.backend.zipfile')
@mock.patch('flaskr.backend.storage')
def test_upload_zip_all_accepted(mock_storage, mock_zip, mock_os, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    mock_os.listdir.return_value = ["test1.md", "test2.md"]

    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.upload("test.zip", mock_file_obj) == "Success"


@mock.patch('flaskr.backend.os')
@mock.patch('flaskr.backend.zipfile')
def test_upload_zip_not_all_accepted(mock_zip, mock_os, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    mock_os.listdir.return_value = ["test1.md", "test2.exe"]

    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.upload("test.zip", mock_file_obj) == "Failure"


def test_get_page_names_no_pages(backend):
    files, page_names = backend.get_all_page_names()
    assert files == [] and page_names == []


def test_get_page_names_one_page(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    mock_file_obj.save.return_value = Mock(return_value=None)
    files, page_names = backend.get_all_page_names()
    if backend.upload("test.md", mock_file_obj) == "Success":
        page_names.append('test')
    assert page_names[0] == 'test'


def test_mult_page_names(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    mock_file_obj.save.return_value = Mock(return_value=None)
    files, page_names = backend.get_all_page_names()
    file_names = ['luke.md', 'anakin.md', 'yoda.md', 'vader.md']
    for i in file_names:
        if backend.upload("test.md", mock_file_obj) == 'Success':
            page_names.append(i)

    assert page_names == ['luke.md', 'anakin.md', 'yoda.md', 'vader.md']


def test_get_page_none(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.get_wiki_page('luke.md') == None


@mock.patch('flaskr.backend.blake2s')
def test_change_password(mock_blake, backend):
    mock_digest = Mock()
    mock_blake.return_value = mock_digest
    assert backend.change_profile("Timmy", "newpass", "", "", "", "", "") == "Success"

def test_change_profile_picture(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)

    mock_file_obj.save.return_value = Mock(return_value=None)
    assert backend.change_profile("Timmy", "", "jedi.jpg", mock_file_obj, "", "", "") == "Success"

def test_change_profile_picture_wrong_format(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)

    mock_file_obj.save.return_value = Mock(return_value=None)
    assert backend.change_profile("Timmy", "", "jedi.gif", mock_file_obj, "", "", "") == "Failure"

def test_change_banner_picture(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)

    mock_file_obj.save.return_value = Mock(return_value=None)
    assert backend.change_profile("Timmy", "", "", "", "palunky.png", mock_file_obj, "") == "Success"

def test_change_banner_picture_wrong_format(backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)

    mock_file_obj.save.return_value = Mock(return_value=None)
    assert backend.change_profile("Timmy", "", "", "", "palunky.exe", mock_file_obj, "") == "Failure"

def test_change_bio(backend):
    assert backend.change_profile("Timmy", "", "", "", "", "", "Bio test") == "Success"

@mock.patch('flaskr.backend.blake2s')
def test_change_entire_profile(mock_blake, backend):
    mock_digest = Mock()
    mock_blake.return_value = mock_digest
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.change_profile("Timmy", "new_pass", "luke.png", mock_file_obj, "space.jpg", mock_file_obj, "Bio test") == "Success"

    




    

