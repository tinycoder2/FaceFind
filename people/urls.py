from django.urls import path


from .views import *
urlpatterns = [

    path('list-missing-person/', MissingPersonListView.as_view(), name='list_missing_person'),
    path('create-missing-person/', MissingPersonCreateView.as_view(), name='create_missing_person'),
    path('update-missing-person/<int:pk>', MisssingPersonUpdateView.as_view(), name='update_missing_person'),
    path('delete-missing-person/<int:pk>', MisssingPersonDeleteView.as_view(), name='delete_missing_person'),
    path('verify-missing-person/<int:pk>', MisssingPersonVerifyView.as_view(), name='verify_missing_person'),

    path('list-reported-person/', ReportedPersonListView.as_view(), name='list_reported_person'),
    path('create-reported-person/', ReportedPersonCreateView.as_view(), name='create_reported_person'),
    path('update-reported-person/<int:pk>', ReportedPersonUpdateView.as_view(), name='update_reported_person'),
    path('delete-reported-person/<int:pk>', ReportedPersonDeleteView.as_view(), name='delete_reported_person'),
    path('verify-reported-person/<int:pk>', ReportedPersonVerifyView.as_view(), name='verify_reported_person'),
    
    path('show-found-person/<str:face_id>', FoundPersonTemplateView.as_view(), name='show_found_person'),
    
    


]