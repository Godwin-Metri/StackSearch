from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
import requests as req


def search(request):
    context = {}
    if request.method == 'POST':
        query = request.POST['search_query']
        if cache.get(f'{query}'):
            context = cache.get(f'{query}')
        else:
            url = f"https://api.stackexchange.com/2.3/search/advanced?page=1&order=desc&sort=activity&title={query}&site=stackoverflow"
            r = req.get(url=url).json()
            p = Paginator(list(r['items']), 15)
            page_num = request.GET.get('page')
            try:
                page_obj = p.get_page(page_num)
            except PageNotAnInteger:
                page_obj = p.page(1)
            except EmptyPage:
                page_obj = p.page(p.num_pages)
            context['size'] = len(page_obj)
            context['query'] = query
            context['data'] = page_obj
            cache.set(f'{query}', context, 60 * 10)
    return render(request, 'search/search.html', context=context)