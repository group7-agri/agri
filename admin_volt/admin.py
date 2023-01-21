from django.contrib import admin
from django.http import Http404

def custom_404(request, exception):
    return render(request, '404.html', status=404)
# Register your models here.
