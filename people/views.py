from pipes import Template
from django.shortcuts import render

# Create your views here.

# Create your views here.
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


class MissingPersonListView(ListView):
    model = MissingPerson
    template_name = 'people/missing_person_list.html'
    context_object_name = "missing_persons"

class MissingPersonCreateView(CreateView):
    model = MissingPerson
    form_class = MissingPersonCreateForm
    template_name = 'people/create_update_form.html'
    success_url = reverse_lazy ('list_missing_person')

class MisssingPersonUpdateView(UpdateView):
    model = MissingPerson
    form_class = MissingPersonUpdateForm
    template_name = 'people/create_update_form.html'
    success_url = reverse_lazy ('list_missing_person')


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
                if not self.object.face_id:
                    print ("Calling Face ID Generation")
                

                    face_client = FaceClient(config['ENDPOINT'], CognitiveServicesCredentials(config['KEY']))
                    response_detected_face = face_client.face.detect_with_stream(
                        image=open(self.object.photo.path, 'rb'),
                        detection_model='detection_03',
                        recognition_model='recognition_04',)
                    print ("Detected Face ID is",response_detected_face[0].face_id)
                    self.object.face_id = response_detected_face[0].face_id
                    self.object.save()
        return super().post(request, **kwargs)


 
class MisssingPersonDeleteView(DeleteView):
    model = MissingPerson
    template_name = 'people/delete_form.html'
    success_url = reverse_lazy ('list_missing_person')
from django.contrib.auth.mixins import LoginRequiredMixin

#######REPORTED#####
class ReportedPersonListView(ListView):
    model = ReportedPerson
    template_name = 'people/reported_person_list.html'
    context_object_name = "reported_persons"
    

class ReportedPersonCreateView(CreateView):
    model = ReportedPerson
    form_class = ReportedPersonCreateForm
    template_name = 'people/reported_create_update_form.html'
    success_url = reverse_lazy ('list_reported_person')

class ReportedPersonUpdateView(UpdateView):
    model = ReportedPerson
    form_class = ReportedPersonUpdateForm
    template_name = 'people/reported_create_update_form.html'
    success_url = reverse_lazy ('list_reported_person')

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
                
                missing_persons_face_ids = list(MissingPerson.objects.all().values_list('face_id', flat=True))
                # missing_persons_names = list(MissingPerson.objects.all().values_list('first_name', flat=True))
                
                # db = dict(zip(missing_persons_names, missing_persons_face_ids))

                if not self.object.face_id:
                    print ("Calling Face ID Generation")
                    face_client = FaceClient(config['ENDPOINT'], CognitiveServicesCredentials(config['KEY']))
                    response_detected_face = face_client.face.detect_with_stream(
                        image=open(self.object.photo.path, 'rb'),
                        detection_model='detection_03',
                        recognition_model='recognition_04',)
                    print ("Detected Face ID is",response_detected_face[0].face_id)
                    self.object.face_id = response_detected_face[0].face_id
                    self.object.save()

                    matched_faces = face_client.face.find_similar(
                        face_id=self.object.face_id,
                        face_ids=missing_persons_face_ids
                    )

                    

                    if MissingPerson.objects.filter(face_id=matched_faces[0].face_id).exists():
                        print ("match found da")
                        print (matched_faces[0].face_id, matched_faces[0].confidence)
                        
                        found_person = MissingPerson.objects.get(face_id = matched_faces[0].face_id)
                        self.object.matched_face_id = matched_faces[0].face_id
                        self.object.is_matched_with_missing_person = True
                        self.object.matched_confindence = "This could be " + found_person.first_name + "lost at " + found_person.last_seen + " reported by "+ found_person.contact_person +  " with confidence rate of" + str(matched_faces[0].confidence*100) +"%" 
                        self.object.save()

                    

                    # for matched_face in matched_faces:
                    #     print("conf", matched_face.confidence)
                    #     # person = [person_name for person_name, face_id in db.items() if face_id == matched_face.face_id]
                    #     print(person)




        return super().post(request, **kwargs)

 
class ReportedPersonDeleteView(DeleteView):
    model = ReportedPerson
    template_name = 'people/delete_form.html'
    success_url = reverse_lazy ('list_reported_person')


class FoundPersonTemplateView(TemplateView):
    model = MissingPerson
    template_name = 'people/found_person_details.html'
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['found_person_details'] = MissingPerson.objects.filter(face_id = self.kwargs['face_id'] )
        return context


