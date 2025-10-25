# Kutt API Client

**Lightweight Python client for the [Kutt](https://kutt.it/) URL shortener API.**

---

## Features

* Create, update, delete, and list short links
* Fetch link statistics
* Fully typed using Pydantic models
* Easy integration in Python projects

---

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

---

## Usage

```python
from kutt_api_client import KuttAPI

# Initialize client with your API key and custom Base URL
api_key = "YOUR_KUTT_API_KEY"
base_url = "https://kutt.it/api/v2"
client = KuttAPI(api_key=api_key, base_url=base_url)

# Create a new short link
link = client.create_link(target="https://www.python.org/", customurl="python-test", description="Python official website", reuse=True)
print("Short link created:", link.link)
print("Target URL:", link.target)

# Update an existing short link
updated_link = client.update_link(id=link.id, description="Updated description")
print("Updated description:", updated_link.description)

# Fetch all links
links = client.get_links()
print("Retrieved", links.total, "links")
for l in links.data:
    print(l.link, "->", l.target)
```

---

## Testing

Run tests with `pytest`:

```bash
pip install requests pytest requests-mock

export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run tests
pytest -v
```

---

## Models

All request, response, and domain models are included in `kutt_api_client.models`:

* `Link`, `Domain`, `User`
* `CreateLinkRequest`, `UpdateLinkRequest`, `CreateDomainRequest`
* `Stats`, `StatsItem`, `StatsItemStats`
* `DeleteResponse`, `LinkListResponse`

---

## License

See [LICENSE](https://chatgpt.com/c/LICENSE) file.
