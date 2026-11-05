#===================
# paginas - urls.py
#===================

from django.urls import path
from . import views

# Cria um namespace para ser utilizado nas URLs
app_name = 'paginas'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('politica_privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('contato/', views.contato, name='contato')
    
    

]