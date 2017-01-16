import os
import tempfile

import pytest

import broadly

def test_home():
    broadly.app.config['TESTING'] = True
    app = broadly.app.test_client()
    response = app.get('/')
    assert response.status_code == 200

def test_solution():
    broadly.app.config['TESTING'] = True
    app = broadly.app.test_client()
    response = app.get('/solution')
    assert response.status_code == 200
    assert response.data == b'6.1875\n'
