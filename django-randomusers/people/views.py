from django.conf import settings
from django.shortcuts import render
from django.http import Http404
from .services.randomuser import fetch_users

def user_list(request):
    page = int(request.GET.get('page', '1'))
    page_size = int(request.GET.get('page_size', settings.DEFAULT_PAGE_SIZE))
    data = fetch_users(page=page, results=page_size)
    users = data.get('results', [])
    info = data.get('info', {})
    ctx = {
        'users': users,
        'page': info.get('page', page),
        'page_size': page_size,
        'has_prev': page > 1,
        'next_page': page + 1,
        'prev_page': page - 1 if page > 1 else 1,
    }
    return render(request, 'people/list.html', ctx)

def user_detail(request, uuid: str):
    page = int(request.GET.get('page', '1'))
    page_size = int(request.GET.get('page_size', settings.DEFAULT_PAGE_SIZE))
    data = fetch_users(page=page, results=page_size)
    users = data.get('results', [])
    user = next((u for u in users if u.get('login', {}).get('uuid') == uuid), None)
    if user is None:
        fallback = fetch_users(page=1, results=50)
        user = next((u for u in fallback.get('results', []) if u.get('login', {}).get('uuid') == uuid), None)
        if user is None:
            raise Http404('Usuario no encontrado')
    return render(request, 'people/detail.html', {'u': user, 'page': page, 'page_size': page_size})
