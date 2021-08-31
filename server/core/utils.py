from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def add_query_params_to_url(url, params):
    """Add query params to a url."""
    redirect_parts = list(urlparse(url))
    query = dict(parse_qsl(redirect_parts[4]))
    query.update(params)
    redirect_parts[4] = urlencode(query)
    return urlunparse(redirect_parts)
