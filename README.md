# Kutt API Client

**Lightweight Python client for the [Kutt](https://kutt.it/) URL shortener API.**

------

## Features

- Create, update, delete, and list short links
- Fetch link statistics
- Fully typed using Pydantic models
- Easy integration in Python projects

------

## Installation


```bash
pip install --upgrade git+https://github.com/tna76874/kutt-api-client.git@main
```

Install via `pip` in editable/development mode:

```bash
git clone https://github.com/tna76874/kutt-api-client.git
cd kutt-api-client
pip install -e .
```

Dependencies:

```bash
pip install requests pydantic tqdm PyYAML pytest requests-mock
```

------

## Usage

```python
from kutt_api_client import KuttAPI
from kutt_api_client.models import CreateLinkRequest

# Initialize client with your API key
api_key = "YOUR_KUTT_API_KEY"
client = KuttAPI(api_key)

# Create a new short link
payload = CreateLinkRequest(
    target="https://www.python.org/",
    description="Python official website",
    customurl="python-test",
    reuse=True
)

link = client.create_link(payload)
print("Short link created:", link.link)
print("Target URL:", link.target)

# Fetch all links
links = client.get_links(limit=10)
print("Retrieved", links.total, "links")
```

------

## Testing

Run tests with `pytest`:

```bash
pip install requests pytest requests-mock

export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run tests
pytest -v
```

Example tests include:

- Utility functions (e.g., URL sanitizing)
- Pydantic model validations
- API client methods using `requests-mock`

------

## Models

All request, response, and domain models are included in `kutt_api_client.models`:

- `Link`, `Domain`, `User`
- `CreateLinkRequest`, `UpdateLinkRequest`, `CreateDomainRequest`
- `Stats`, `StatsItem`, `StatsItemStats`
- `DeleteResponse`, `LinkListResponse`

------

## License

see [LICENSE](https://chatgpt.com/c/LICENSE) file.

