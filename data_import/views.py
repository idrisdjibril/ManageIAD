from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from django.core.paginator import Paginator
from django.db.models import Q
import json
#from elasticsearch_dsl import Q as ESQ
#from .search_data import DHIS2DataDocument

def data_table(request):
    return render(request, 'data_import/data_table.html')

def dhis2_data_api(request):
    start = int(request.GET.get('start', 0))
    end = int(request.GET.get('end', 50))
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    with connections['default'].cursor() as cursor:
        query = "SELECT * FROM dhis2 WHERE 1=1"
        params = []

        if search:
            query += " AND (CAST(commune_id AS TEXT) ILIKE %s OR event ILIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])

        if category:
            query += f" AND {category} IS NOT NULL"

        if date_from and date_to:
            query += " AND _date_de_saisie_ BETWEEN %s AND %s"
            params.extend([date_from, date_to])

        query += " ORDER BY commune_id OFFSET %s LIMIT %s"
        params.extend([start, end - start])

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return JsonResponse(data, safe=False)


def dashboard_admin(request):
    return render(request, 'dashboard_admin.html')

def dashboard_director(request):
    return render(request, 'dashboard_director.html')

def dashboard_agent(request):
    return render(request, 'dashboard_agent.html')

def data_table(request):
    return render(request, 'data_table.html')

def analysis(request):
    return render(request, 'analysis.html')

def decision_making(request):
    return render(request, 'decision_making.html')

def user_list(request):
    return render(request, 'user_list.html')

def compose(request):
    return render(request, 'compose.html')

def edit_profile(request):
    return render(request, 'edit_profile.html')

def advanced_search(request):
    return render(request, 'data_import/advanced_search.html')

def get_columns(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'dhis2'")
        columns = [col[0] for col in cursor.fetchall()]
        print("Columns:", columns)
    return JsonResponse(columns, safe=False)

def advanced_search_api(request):
    print("Advanced search API called")  # Debug print
    column = request.GET.get('column', '')
    search_value = request.GET.get('search', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    page = int(request.GET.get('page', 1))
    items_per_page = 50

    print(f"Params: column={column}, search={search_value}, date_from={date_from}, date_to={date_to}, page={page}")  # Debug print

    with connections['default'].cursor() as cursor:
        query = "SELECT * FROM dhis2 WHERE 1=1"
        params = []

        if column and search_value:
            query += f" AND {column}::text ILIKE %s"
            params.append(f'%{search_value}%')
        elif search_value:  # Recherche globale si aucune colonne n'est spécifiée
            query += " AND ("
            column_query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'dhis2'"
            cursor.execute(column_query)
            columns = [col[0] for col in cursor.fetchall()]
            or_conditions = [f"{col}::text ILIKE %s" for col in columns]
            query += " OR ".join(or_conditions)
            query += ")"
            params.extend([f'%{search_value}%'] * len(columns))

        if date_from and date_to:
            query += " AND _date_de_saisie_::date BETWEEN %s AND %s"
            params.extend([date_from, date_to])

        print(f"Query: {query}")  # Debug print
        print(f"Params: {params}")  # Debug print

        # Compte total des résultats
        count_query = f"SELECT COUNT(*) FROM ({query}) AS count_query"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]

        # Pagination
        offset = (page - 1) * items_per_page
        query += f" ORDER BY _date_de_saisie_ DESC LIMIT {items_per_page} OFFSET {offset}"

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    print(f"Total count: {total_count}")  # Debug print
    print(f"Data length: {len(data)}")  # Debug print

    return JsonResponse({
        'data': data,
        'total_count': total_count,
        'page': page,
        'items_per_page': items_per_page
    })


#def advanced_search_api(request):
    column = request.GET.get('column', '')
    search_value = request.GET.get('search', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    page = int(request.GET.get('page', 1))
    items_per_page = 50

    s = DHIS2DataDocument.search()

    if column and search_value:
        s = s.query("match", **{column: search_value})
    elif search_value:
        s = s.query("multi_match", query=search_value, fields=['*'])

    if date_from and date_to:
        s = s.filter('range', _date_de_saisie_={'gte': date_from, 'lte': date_to})

    total_count = s.count()
    s = s[(page-1)*items_per_page:page*items_per_page]

    response = s.execute()

    data = [hit.to_dict() for hit in response]

    return JsonResponse({
        'data': data,
        'total_count': total_count,
        'page': page,
        'items_per_page': items_per_page
    })
# Gardez les autres fonctions existantes...