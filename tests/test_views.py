import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_api():
    client = APIClient()

    response = client.get('/api/users/register/')

    assert response.status_code == 200