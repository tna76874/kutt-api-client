import pytest
import pandas as pd
from kutt_api_client.api import KuttAPI
from kutt_api_client.models import Link, CreateLinkRequest, UpdateLinkRequest


@pytest.fixture
def api():
    return KuttAPI("dummy-key")


@pytest.fixture
def fake_link_response():
    """Basisdaten für Fake-API-Antworten."""
    return {
        "id": "00000000-0000-0000-0000-000000000001",
        "address": "example",
        "banned": False,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "target": "https://example.com",
        "link": "https://kutt.it/example",
        "password": False,
        "visit_count": 0,
    }


# --- CREATE LINK TESTS --------------------------------------------------------

def test_create_link_with_payload(requests_mock, api, fake_link_response):
    """Create link via CreateLinkRequest payload."""
    requests_mock.post("https://kutt.it/api/v2/links", json=fake_link_response)

    payload = CreateLinkRequest(target="https://example.com")
    link = api.create_link(payload)

    assert isinstance(link, Link)
    assert str(link.target).rstrip("/") == "https://example.com"
    assert str(link.link).startswith("https://kutt.it/")


def test_create_link_with_kwargs(requests_mock, api, fake_link_response):
    """Create link directly with kwargs (no payload object)."""
    response = fake_link_response.copy()
    response["id"] = "00000000-0000-0000-0000-000000000002"
    response["target"] = "https://example2.com"
    response["link"] = "https://kutt.it/example2"
    requests_mock.post("https://kutt.it/api/v2/links", json=response)

    link = api.create_link(target="https://example2.com")

    assert isinstance(link, Link)
    assert str(link.target).rstrip("/") == "https://example2.com"
    assert str(link.link).endswith("/example2")


# --- UPDATE LINK TESTS --------------------------------------------------------

def test_update_link_with_payload(requests_mock, api, fake_link_response):
    """Update existing link via UpdateLinkRequest payload."""
    updated = fake_link_response | {
        "description": "Updated via payload",
        "updated_at": "2024-01-03T00:00:00Z",
    }
    requests_mock.patch(
        f"https://kutt.it/api/v2/links/{updated['id']}", json=updated
    )

    # target erforderlich, sonst Pydantic ValidationError
    payload = UpdateLinkRequest(
        id=updated["id"],
        target=updated["target"],
        address=updated["address"],
        description="Updated via payload",
    )

    link = api.update_link(payload)

    assert isinstance(link, Link)
    assert str(link.target).rstrip("/") == "https://example.com"
    assert link.description == "Updated via payload"


def test_update_link_with_kwargs(requests_mock, api, fake_link_response):
    """Update existing link using kwargs instead of payload."""
    response = fake_link_response | {
        "id": "00000000-0000-0000-0000-000000000002",
        "target": "https://example2.com",
        "link": "https://kutt.it/example2",
        "description": "Updated via kwargs",
        "updated_at": "2024-01-04T00:00:00Z",
    }
    requests_mock.patch(
        f"https://kutt.it/api/v2/links/{response['id']}", json=response
    )

    link = api.update_link(
        id=response["id"],
        target=response["target"],
        address=response["address"],
        description="Updated via kwargs",
    )

    assert isinstance(link, Link)
    assert str(link.target).rstrip("/") == "https://example2.com"
    assert link.description == "Updated via kwargs"

# --- DATAFRAME TEST ---------------------------------------------------------

def test_get_links_dataframe(requests_mock, api, fake_link_response):
    """Test that get_links_dataframe() returns a Pandas DataFrame with the correct data."""

    # Mock GET request to simulate first page with 1 link, second page empty
    requests_mock.get(
        "https://kutt.it/api/v2/links",
        [
            {"json": {"data": [fake_link_response]}},  # first page
            {"json": {"data": []}},                     # second page -> loop ends
        ]
    )

    df = api.get_links_dataframe()

    import pandas as pd
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    expected_columns = set(fake_link_response.keys())
    assert expected_columns.issubset(df.columns)

    first_row = df.iloc[0]
    for key in ["id", "target", "link"]:
        assert isinstance(first_row["target"], str)


    assert first_row["id"] == fake_link_response["id"]
    assert first_row["target"].rstrip("/")  == fake_link_response["target"]
    assert first_row["link"].rstrip("/")  == fake_link_response["link"]
