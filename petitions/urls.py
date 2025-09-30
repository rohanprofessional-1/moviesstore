from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='petitions.index'),
    path('<int:id>/', views.show, name='petitions.show'),
    path('create/', views.create_petition, name='petitions.create'),
    path('<int:id>/vote/', views.vote_yes, name='petitions.vote'),
]
