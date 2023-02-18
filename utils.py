from datetime import datetime, timezone
from typing import Optional, Mapping
from urllib.parse import urljoin, urlparse, urlencode, urlunparse


def parse_date(date: Optional[str]) -> Optional[datetime]:
    if date is None:
        return None
    try:
        return datetime.fromisoformat(date[:-1]).astimezone(timezone.utc)
    except ValueError:
        return None


def build_url(url: str, path: str, params: Mapping) -> str:
    bundled = urljoin(url, path)
    url_parts = list(urlparse(bundled))
    query = urlencode(params)
    url_parts[4] = query
    return urlunparse(url_parts)
