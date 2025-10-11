#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API test
"""

import pytest
import requests
from kutt_api_client.api import KuttAPI
from kutt_api_client.models import Link, CreateLinkRequest

@pytest.fixture
def api():
    return KuttAPI("dummy-key")

def test_create_link_success(requests_mock, api):
    payload = CreateLinkRequest(target="https://example.com")

    fake_response = {
        "id": "00000000-0000-0000-0000-000000000001",
        "address": "example",
        "banned": False,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "target": "https://example.com",
        "link": "https://kutt.it/example",
        "password": False,
        "visit_count": 0
    }

    requests_mock.post("https://kutt.it/api/v2/links", json=fake_response)

    link = api.create_link(payload)
    assert isinstance(link, Link)
