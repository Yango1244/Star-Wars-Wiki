from flaskr.backend import Backend
import unittest
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch
import google
import pytest
# TODO(Project 1): Write tests for Backend methods.


@pytest.fixture
def backend():
    return Backend()


@mock.patch('flaskr.backend.storage')
def sign_up_add_user(mock_storage, backend):
    mock_gcs_client = mock_storage.Client.return_value
    mock_bucket = Mock()
    # Blob won't exist so we expect to make the blob
    mock_bucket.get_blob.return_value = None
    mock_gcs_client.get_bucket.return_value = mock_bucket
    backend = Backend()
    backend.sign_up("Capy", "CapybaraLove")
    mock_bucket.get_blob.assert_called_with('Capy')
    mock_bucket.blob.assert_called_once_with('Capy')


@mock.patch('flaskr.backend.storage')
def sign_up_user_exists(mock_storage, backend):
    mock_gcs_client = mock_storage.Client.return_value
    mock_bucket = Mock()
    # Blob will exist so we expect to only call get_blob once
    mock_bucket.get_blob.return_value = True
    mock_gcs_client.get_bucket.return_value = mock_bucket

    backend = Backend()
    backend.sign_up("Capy", "CapybaraLove")
    mock_bucket.get_blob.assert_called_once_with('Capy')
    assert not mock_bucket.blob.called


@mock.patch('flaskr.backend.storage')
def sign_in_user_incorrect(mock_storage, backend):
    mock_gcs_client = mock_storage.Client.return_value
    mock_bucket = Mock()
    # Blob won't exist so we expect to return False
    mock_bucket.get_blob.return_value = None
    mock_gcs_client.get_bucket.return_value = mock_bucket

    backend = Backend()
    assert not backend.sign_in("Capy", "CapyWrong")


@mock.patch('flaskr.backend.storage')
@mock.patch('flaskr.backend.blake2s')
def sign_in_user_correct(mock_blake, mock_storage, backend):
    mock_digest = Mock()
    mock_blake.return_value = mock_digest
    mock_bucket = Mock()
    mock_blob = Mock()
    mock_file = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file)
    mock_open.__exit__ = Mock(return_value=None)
    mock_gcs_client = mock_storage.Client.return_value
    mock_gcs_client.get_bucket.return_value = mock_bucket
    mock_bucket.get_blob.return_value = mock_blob
    mock_blob.open.return_value = mock_open
    mock_file.read.return_value = "Correct"
    mock_digest.hexdigest.return_value = "Correct"

    backend = Backend()
    assert backend.sign_in("Capy", "CapyRight")


def integration_sign_in(backend):
    assert backend.sign_in("Capy", "CapybaraLove")


# def get_image(backend):
#     # integration test
#     assert backend.get_image("LeroneJoyner.jpg")


def upload_empty_file(backend):
    mock_file_obj = Mock()
    assert backend.upload("", mock_file_obj) == "Failure"


@mock.patch('flaskr.backend.storage')
def upload_wrong_format(mock_storage, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    backend = Backend()

    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.upload("Luke.exe", mock_file_obj) == "Failure"


@mock.patch('flaskr.backend.storage')
def upload_single_file(mock_storage, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    backend = Backend()

    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.upload("test.md", mock_file_obj) == "Success"


@mock.patch('flaskr.backend.os')
@mock.patch('flaskr.backend.zipfile')
@mock.patch('flaskr.backend.storage')
def upload_zip_all_accepted(mock_storage, mock_zip, mock_os, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    backend = Backend()
    mock_os.listdir.return_value = ["test1.md", "test2.md"]

    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.upload("test.zip", mock_file_obj) == "Success"


@mock.patch('flaskr.backend.os')
@mock.patch('flaskr.backend.zipfile')
@mock.patch('flaskr.backend.storage')
def upload_zip_not_all_accepted(mock_storage, mock_zip, mock_os, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    backend = Backend()
    mock_os.listdir.return_value = ["test1.md", "test2.exe"]

    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.upload("test.zip", mock_file_obj) == "Failure"


@mock.patch('flaskr.backend.storage')
def get_page_names_no_pages(mock_storage, backend):
    mock_file_obj = Mock()
    backend = Backend()
    files, page_names = backend.get_all_page_names()
    assert files == [] and page_names == []


@mock.patch('flaskr.backend.storage')
def get_page_names_one_page(mock_storage, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    backend = Backend()
    mock_file_obj.save.return_value = Mock(return_value=None)
    files, page_names = backend.get_all_page_names()
    if backend.upload("test.md", mock_file_obj) == "Success":
        page_names.append('test')
        print()
        assert page_names[0] == 'test'
    else:
        assert page_names == []


@mock.patch('flaskr.backend.storage')
def mult_page_names(mock_storage, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    backend = Backend()
    mock_file_obj.save.return_value = Mock(return_value=None)
    files, page_names = backend.get_all_page_names()
    file_names = ['luke.md', 'anakin.md', 'yoda.md', 'vader.md']
    for i in file_names:
        if backend.upload("test.md", mock_file_obj) == 'Success':
            page_names.append(i)

    assert page_names == ['luke.md', 'anakin.md', 'yoda.md', 'vader.md']


@mock.patch('flaskr.backend.storage')
def get_page_none(mock_storage, backend):
    mock_file_obj = Mock()
    mock_open = Mock()
    mock_open.__enter__ = Mock(return_value=mock_file_obj)
    mock_open.__exit__ = Mock(return_value=None)
    backend = Backend()
    mock_file_obj.save.return_value = Mock(return_value=None)

    assert backend.get_wiki_page('luke.md') == None


def delete_blob(backend):
    blob = Mock()
    blob.delete.return_value = Mock()
    backend.delete_blob(blob)
    assert blob.delete.assert_called_once_with()


@mock.patch('flaskr.backend.storage')
def get_comments(mock_storage, backend):
    mock_blob1 = Mock()
    mock_blob2 = Mock()
    mock_blob3 = Mock()
    mock_blob1.name.return_value = "Han/1.cmt/capy"
    mock_blob1.download_as_bytes = "Hello!".encode('utf-8')
    mock_blob2.name.return_value = "Han/2.cmt/jake"
    mock_blob2.download_as_bytes = "Hello Capy!".encode('utf-8')
    mock_blob3.name.return_value = "Han/3.cmt/poe"
    mock_blob3.download_as_bytes = "I love han!".encode('utf-8')
    mock_client = Mock()
    mock_storage.client.return_value = mock_client
    mock_client.list_blobs.return_value = [mock_blob1, mock_blob2, mock_blob3]

    assert (backend.get_comments("Han")) == {
        1: [("Hello!", "capy")],
        2: [("Hello Capy!", "jake")],
        3: [("I love han!", "poe")]
    }


@mock.patch('flaskr.backend.storage')
def get_comments(mock_storage, backend):
    mock_client = Mock()
    mock_bucket = Mock()
    mock_storage.client.return_value = mock_client
    mock_client.get_bucket.return_value = mock_bucket

    backend.upload_comment("han", "capy", "hello", "1")

    assert mock_bucket.get_blob.assert_called_once_with("han/1.cmt/1.cmt/capy")
