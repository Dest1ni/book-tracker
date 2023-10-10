from django import template
from tracker.models import Book

register = template.Library()
@register.inclusion_tag('tracker/listbook_tag.html')
def show_books(id: int = None):
    if id: 
        books = Book.objects.filter(Book.author.pk == id)
    else:
        books = Book.objects.all()
    return {'books': books}