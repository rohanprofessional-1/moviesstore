from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
    path('feedback-prompt/<int:order_id>/', views.feedback_prompt, name='cart.feedback_prompt'),
    path('submit-feedback/<int:order_id>/', views.submit_feedback, name='cart.submit_feedback'),
    path('purchase-complete/<int:order_id>/', views.purchase_complete, name='cart.purchase_complete'),
    path('feedback/view/', views.view_feedback, name='cart.view_feedback'),
]