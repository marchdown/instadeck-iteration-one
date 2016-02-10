# -*- coding: utf-8 -*-
"""
    Instadeck Tests
    ~~~~~~~~~~~~

    Tests the Instadeck application.
"""

import pytest

import os
import instadeck
import tempfile


@pytest.fixture
def client(request):
    db_fd, instadeck.app.config['DATABASE'] = tempfile.mkstemp()
    instadeck.app.config['TESTING'] = True
    client = instadeck.app.test_client()
    with instadeck.app.app_context():
        instadeck.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(instadeck.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client

def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data



def test_messages(client):
    """Test that messages work"""
    rv = client.post('/add_deck', data=dict(
        slug="deadbeef"
        title='<Hello>',
        contents='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
