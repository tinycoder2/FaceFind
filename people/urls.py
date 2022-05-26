from django.urls import path


from .views import *
urlpatterns = [
    # urls for missing person list views
    path('list-missing-person/', MissingPersonListView.as_view(), name='list_missing_person'),
    path('list-missing-person-to-be-verified/', MissingPersonToBeApprovedListView.as_view(), name='list_missing_person_to_be_verified'),
    path('list-missing-person-with-leads/', MissingPersonWithLeadsListView.as_view(), name='list_missing_person_with_leads'),
    path('list-missing-person-found/', MissingPersonFoundListView.as_view(), name='list_missing_person_found'),

    # urls for missing person create, update verify, delete
    path('create-missing-person/', MissingPersonCreateView.as_view(), name='create_missing_person'),
    path('update-missing-person/<int:pk>', MisssingPersonUpdateView.as_view(), name='update_missing_person'),
    path('delete-missing-person/<int:pk>', MisssingPersonDeleteView.as_view(), name='delete_missing_person'),
    path('verify-missing-person/<int:pk>', MisssingPersonVerifyView.as_view(), name='verify_missing_person'),

    # url to update status of missing person
    path('missing-person-match/<int:pk>', missing_person_update_status, name='missing_person_match'),

    # urls for reported person list views
    path('list-reported-person/', ReportedPersonListView.as_view(), name='list_reported_person'),
    path('list-reported-person-to-be-verified/', ReportedPersonToBeApprovedListView.as_view(), name='list_reported_person_to_be_verified'),
    path('list-reported-person-match-found/', ReportedPersonMatchedListView.as_view(), name='list_reported_person_match_found'),
    path('list-reported-person-match-not-found/', ReportedPersonNotMatchedListView.as_view(), name='list_reported_person_match_not_found'),

  # urls for reported person create, update verify, delete
    path('create-reported-person/', ReportedPersonCreateView.as_view(), name='create_reported_person'),
    path('update-reported-person/<int:pk>', ReportedPersonUpdateView.as_view(), name='update_reported_person'),
    path('delete-reported-person/<int:pk>', ReportedPersonDeleteView.as_view(), name='delete_reported_person'),
    path('verify-reported-person/<int:pk>', ReportedPersonVerifyView.as_view(), name='verify_reported_person'),
    
    # url for showing found/matched person
    path('show-found-person/<str:face_id>', FoundPersonTemplateView.as_view(), name='show_found_person'),

    # urls for form success
    path('missing-person-form-success/', MissingPersonFormSuccessView.as_view(), name='missing_person_form_success'),
    path('reported-person-form-success/', ReportedPersonFormSuccessView.as_view(), name='reported_person_form_success'),

    
    


]