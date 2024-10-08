from urllib.parse import urlparse, urlunparse

import pytest
from requests_mock import Mocker
from llama_index.embeddings.nvidia import NVIDIAEmbedding as Interface


@pytest.fixture()
def mock_v1_local_models2(requests_mock: Mocker, base_url: str) -> None:
    result = urlparse(base_url)
    base_url = urlunparse((result.scheme, result.netloc, "v1", "", "", ""))
    requests_mock.get(
        f"{base_url}/models",
        json={
            "data": [
                {
                    "id": "model1",
                    "object": "model",
                    "created": 1234567890,
                    "owned_by": "OWNER",
                    "root": "model1",
                },
            ]
        },
    )


# test case for invalid base_url
@pytest.mark.parametrize(
    "base_url",
    [
        "localhost",
        "localhost:8888",
        "http://localhost:8888/embeddings",
        "http://0.0.0.0:8888/rankings",
        "http://localhost:8888/chat/completions",
        "http://test_url/.../v1",
        "https://test_url/.../v1",
    ],
)
def test_base_url_invalid_not_hosted(
    base_url: str, mock_v1_local_models2: None
) -> None:
    with pytest.raises(ValueError):
        Interface(base_url=base_url)


@pytest.mark.parametrize(
    "base_url",
    [
        "http://localhost:8080/v1/embeddings",
    ],
)
def test_base_url_valid_not_hosted(base_url: str, mock_v1_local_models2: None) -> None:
    with pytest.warns(UserWarning):
        Interface(base_url=base_url)


@pytest.mark.parametrize(
    "base_url",
    [
        "https://ai.api.nvidia.com/v1/retrieval/nvidia/",
        "https://ai.api.nvidia.com/v1/retrieval/snowflake/arctic-embed-l",
        "https://integrate.api.nvidia.com/v1/",
    ],
)
def test_base_url_valid_hosted(base_url: str, mock_v1_local_models2: None) -> None:
    Interface(api_key="BOGUS", base_url=base_url)
