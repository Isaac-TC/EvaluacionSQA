import requests
from django.conf import settings

BASE_URL = 'https://randomuser.me/api/'

def fetch_users(page: int = 1, results: int | None = None, seed: str | None = None) -> dict:
    if results is None:
        results = settings.DEFAULT_PAGE_SIZE
    if seed is None:
        seed = settings.RANDOMUSER_SEED

    params = {'page': page, 'results': results, 'seed': seed}
    r = requests.get(BASE_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json()
