from pipes import Template
from django.shortcuts import render

from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.urls import reverse_lazy

from people.models import MissingPerson, ReportedPerson
from .forms import *
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

import json

with open('./config.json', 'r') as f:
    config = json.load(f)


## MISSING PERSONS
# view to list all missing people
class MissingPersonListView(ListView):
    model = MissingPerson
    template_name = 'people/missing_person_list.html'
    context_object_name = "missing_persons"

# view to create a missing person
class MissingPersonCreateView(CreateView):
    model = MissingPerson
    form_class = MissingPersonCreateForm
    template_name = 'people/create_update_form.html'
    success_url = reverse_lazy ('list_missing_person')

# view to update a missing person
class MisssingPersonUpdateView(UpdateView):
    model = MissingPerson
    form_class = MissingPersonUpdateForm
    template_name = 'people/create_update_form.html'
    success_url = reverse_lazy ('list_missing_person')

# function to generate face_id using Azure Face API
def generate_face_id(image_path):
    face_client = FaceClient(config['ENDPOINT'], CognitiveServicesCredentials(config['KEY']))
    response_detected_face = face_client.face.detect_with_stream(
        image=open(image_path, 'rb'),
        detection_model='detection_03',
        recognition_model='recognition_04',
        )
    return response_detected_face

# function to find a match for the reported person from the list of missing people using Azure Face API
def find_match(reported_face_id, missing_face_ids):
    face_client = FaceClient(config['ENDPOINT'], CognitiveServicesCredentials(config['KEY']))
    matched_faces = face_client.face.find_similar(
        face_id=reported_face_id,
        face_ids=missing_face_ids
        )
    return matched_faces



# view to verify a missing person (if background check is done)
class MisssingPersonVerifyView(UpdateView):
    model = MissingPerson
    form_class = MissingPersonVerifyForm
    template_name = 'people/create_update_form.html'
    success_url = reverse_lazy ('list_missing_person')

    def post(self, request, **kwargs):
        print ("Catching Update Function")
            
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data['is_verified']:
                self.object = self.get_object()
                print ("image URL is", self.object.photo.url)
                print ("image Path is", self.object.photo.path)
                
                print("face ID is",self.object.face_id)

                # if the person is verified and does not already have a face id, we generate one
                if not self.object.face_id:
                    print ("Calling Face ID Generation")

                    # generating face id
                    response_detected_face=generate_face_id(self.object.photo.path)
                    print ("Detected Face ID is",response_detected_face[0].face_id)

                    # saving the generated face id to database
                    self.object.face_id = response_detected_face[0].face_id
                    self.object.save()
        return super().post(request, **kwargs)


# view to delete a missing person
class MisssingPersonDeleteView(DeleteView):
    model = MissingPerson
    template_name = 'people/delete_form.html'
    success_url = reverse_lazy ('list_missing_person')

## REPORTED PERSONS
# view to list all reported people
class ReportedPersonListView(ListView):
    model = ReportedPerson
    template_name = 'people/reported_person_list.html'
    context_object_name = "reported_persons"
    
# view to create reported people
class ReportedPersonCreateView(CreateView):
    model = ReportedPerson
    form_class = ReportedPersonCreateForm
    template_name = 'people/reported_create_update_form.html'
    success_url = reverse_lazy ('list_reported_person')

# view to update reported people
class ReportedPersonUpdateView(UpdateView):
    model = ReportedPerson
    form_class = ReportedPersonUpdateForm
    template_name = 'people/reported_create_update_form.html'
    success_url = reverse_lazy ('list_reported_person')

# view to verify a reported person 
class ReportedPersonVerifyView(UpdateView):
    model = ReportedPerson
    form_class = ReportedPersonVerifyForm
    template_name = 'people/reported_create_update_form.html'
    success_url = reverse_lazy ('list_reported_person')

    def post(self, request, **kwargs):
        print ("Catching Update Function")
            
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data['is_verified']:
                self.object = self.get_object()
                print ("image URL is", self.object.photo.url)
                print ("image Path is", self.object.photo.path)
                
                print("face ID is",self.object.face_id)
                
                # to get a list of all face_ids of missing persons
                missing_persons_face_ids = list(MissingPerson.objects.all().values_list('face_id', flat=True))
                # missing_persons_names = list(MissingPerson.objects.all().values_list('first_name', flat=True))
                
                # db = dict(zip(missing_persons_names, missing_persons_face_ids))

                # if the person is verified and does not already have a face id, we generate one
                if not self.object.face_id:
                    print ("Calling Face ID Generation")

                    # generating face id
                    response_detected_face=generate_face_id(self.object.photo.path)
                    print ("Detected Face ID is",response_detected_face[0].face_id)

                    # saving the generated face id to database
                    self.object.face_id = response_detected_face[0].face_id
                    self.object.save()

                    # finding if there is a match
                    matched_faces=find_match(self.object.face_id, missing_persons_face_ids)

                    print(matched_faces)
                    # if return list is not empty
                    if len(matched_faces)!=0:
                        # if the matched face returned exists in list of missing people
                        if MissingPerson.objects.filter(face_id=matched_faces[0].face_id).exists():
                            print ("match found !")
                            print (matched_faces[0].face_id, matched_faces[0].confidence)
                            
                            # getting the matched missing person
                            found_person = MissingPerson.objects.get(face_id = matched_faces[0].face_id)

                            # Updating matched details to reported database
                            self.object.matched_face_id = matched_faces[0].face_id
                            self.object.is_matched_with_missing_person = True
                            self.object.matched_confindence = "This could be " + found_person.first_name + "lost at " + found_person.last_seen + " reported by "+ found_person.contact_person +  " with confidence rate of" + str(matched_faces[0].confidence*100) +"%" 
                            self.object.save()

        return super().post(request, **kwargs)

# view to delete reported person
class ReportedPersonDeleteView(DeleteView):
    model = ReportedPerson
    template_name = 'people/delete_form.html'
    success_url = reverse_lazy ('list_reported_person')

# view to display matched/found person details
class FoundPersonTemplateView(TemplateView):
    model = MissingPerson
    template_name = 'people/found_person_details.html'
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['found_person_details'] = MissingPerson.objects.filter(face_id = self.kwargs['face_id'] )
        return context


