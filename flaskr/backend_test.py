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
def test_sign_up_add_user(mock_storage, backend):
    mock_gcs_client = mock_storage.Client.return_value
    mock_bucket = Mock()
    #Blob won't exist so we expect to make the blob
    mock_bucket.get_blob.return_value = None
    mock_gcs_client.get_bucket.return_value = mock_bucket
    backend = Backend()
    backend.sign_up("Capy", "CapybaraLove")
    mock_bucket.get_blob.assert_called_with('Capy')
    mock_bucket.blob.assert_called_once_with('Capy')

@mock.patch('flaskr.backend.storage')
def test_sign_up_user_exists(mock_storage, backend):
    mock_gcs_client = mock_storage.Client.return_value
    mock_bucket = Mock()
    #Blob will exist so we expect to only call get_blob once
    mock_bucket.get_blob.return_value = True
    mock_gcs_client.get_bucket.return_value = mock_bucket

    backend = Backend()
    backend.sign_up("Capy", "CapybaraLove")
    mock_bucket.get_blob.assert_called_once_with('Capy')
    assert not mock_bucket.blob.called


def test_sign_in(backend):
    assert backend.sign_in("Capy", "CapybaraLove")

def test_get_image(backend):
    # integration test
    assert backend.get_image("LeroneJoyner.jpg")