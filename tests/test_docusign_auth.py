import pytest
from docusign_auth import dsauth


@pytest.fixture(scope="function")
def api_client_fixture():
    client = dsauth()
    return client


def test_docusign_auth(api_client_fixture):
    assert api_client_fixture is not None
