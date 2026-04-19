from django.urls import path
from . import views

app_name = 'diagnosis'

urlpatterns = [
    # Web interface
    path('', views.home_page, name='home_page'),
    path('upload-page/', views.upload_page, name='upload_page'),
    path('test/', views.api_test_page, name='api_test_legacy'),
    path('api-test/', views.api_test_page_drf, name='api_test'),
    path('history/', views.history_page, name='history'),
    path('result/', views.result_page, name='result_page'),
    path('result/<int:pk>/', views.result_page, name='result_detail'),

    # Upload avec redirection (formulaire traditionnel)
    path('upload-and-predict/', views.upload_and_predict, name='upload_and_predict'),
    path('upload/', views.upload_and_predict, name='upload_and_predict_direct'),

    # API REST endpoints
    path('api/predict/', views.predict_diagnosis, name='api_predict'),
    path('api/predict-multiple/', views.predict_multiple, name='api_predict_multiple'),
    path('api/model-info/', views.get_model_info, name='api_model_info'),
    path('api/result/<int:prediction_id>/', views.get_prediction_result, name='api_result'),
]