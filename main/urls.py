from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.HomeView.as_view()),
    path('parks/', views.ParksListView.as_view(), name='parks.list'),
    path('parks/<int:pk>', views.parks_detail, name='parks.detail'),
    path('parks/new', views.ParksCreateView.as_view(), name='parks.new'),
]