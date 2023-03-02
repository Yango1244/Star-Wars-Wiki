from flaskr.backend import Backend
import pytest
# TODO(Project 1): Write tests for Backend methods.

@pytest.fixture
def backend():
    return Backend()

def test_sign_up(backend):
    backend.sign_up("Capy", "CapybaraLove")

def test_sign_in(backend):
    assert backend.sign_in("Capy", "CapybaraLove")