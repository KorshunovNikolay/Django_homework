from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from books.models import Book

def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)

def books_by_date(request, current_date):
    template = 'books/books_pagi.html'
    current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
    all_dates = list(Book.objects.dates('pub_date', 'day', order='ASC'))
    paginator = Paginator(all_dates, 1)
    for i, date in enumerate(all_dates, 1):
        if date == current_date:
            page_number = i
            break
    page_obj = paginator.get_page(page_number)
    books = Book.objects.filter (pub_date=current_date)
    current_index = all_dates.index(current_date)
    previous_date = all_dates[current_index - 1] if current_index > 0 else None
    next_date = all_dates[current_index + 1] if current_index < len(all_dates) - 1 else None
    context = {'books': books,
               'page_obj': page_obj,
               'current_date': current_date,
               'previous_date': previous_date,
               'next_date': next_date}
    return render(request, template, context)