# data_import/views.py

import logging
from django.shortcuts import render
from django.db import connection
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import viewsets
from .models import DHSI2
from .serializers import DHSI2Serializer
from .tasks import import_csv_data
import csv

logger = logging.getLogger(__name__)

class DHSI2ViewSet(viewsets.ModelViewSet):
    queryset = DHSI2.objects.all()
    serializer_class = DHSI2Serializer

def data_table(request):
    import_csv_data.delay()  # Lance l'importation en arrière-plan

    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    date = request.GET.get('date', '')

    cache_key = f'data_table:{search_query}:{category}:{date}'
    cached_data = cache.get(cache_key)

    if cached_data is None:
        with connection.cursor() as cursor:
            query = "SELECT * FROM DHSI2"
            params = []

            if search_query or category or date:
                query += " WHERE "
                conditions = []

                if search_query:
                    conditions.append("(CAST(id AS TEXT) ILIKE %s OR CAST(date_importation AS TEXT) ILIKE %s)")
                    params.extend([f'%{search_query}%', f'%{search_query}%'])

                if category:
                    conditions.append(f"{category} ILIKE %s")
                    params.append(f'%{search_query}%')

                if date:
                    conditions.append("DATE(date_importation) = %s")
                    params.append(date)

                query += " AND ".join(conditions)

            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        cache.set(cache_key, (columns, data), 300)  # Cache for 5 minutes
    else:
        columns, data = cached_data

    logger.info(f"Recherche effectuée - Query: {search_query}, Category: {category}, Date: {date}")

    context = {
        'columns': columns,
        'data': data,
        'search_query': search_query,
        'category': category,
        'date': date,
    }

    return render(request, 'data_import/data_table.html', context)

def export_pdf(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    date = request.GET.get('date', '')

    with connection.cursor() as cursor:
        query = "SELECT * FROM DHSI2"
        params = []

        if search_query or category or date:
            query += " WHERE "
            conditions = []

            if search_query:
                conditions.append("(CAST(id AS TEXT) ILIKE %s OR CAST(date_importation AS TEXT) ILIKE %s)")
                params.extend([f'%{search_query}%', f'%{search_query}%'])

            if category:
                conditions.append(f"{category} ILIKE %s")
                params.append(f'%{search_query}%')

            if date:
                conditions.append("DATE(date_importation) = %s")
                params.append(date)

            query += " AND ".join(conditions)

        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'

    writer = csv.writer(response)
    writer.writerow(columns)
    writer.writerows(data)

    logger.info(f"Export PDF généré - Query: {search_query}, Category: {category}, Date: {date}")

    return response