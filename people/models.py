from django.db import models

# Create your models here.

from phonenumber_field.modelfields import PhoneNumberField


class MissingPerson(models.Model):

    GENDER_CATEGORY_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    RELATIONSHIP_CATEGORY_CHOICES = (
        ("Father", "Father"),
        ("Mother", "Mother"),
        ("Brother", "Brother"),
        ("Sister", "Sister"),
        ("Husband", "Husband"),
        ("Wife", "Wife"),
        ("Guardian", "Guardian"),
        ("Relative", "Relative"),
        ("Friend", "Friend"),
        ("Other", "Other"),
        
    )

    CURRENT_STATUS_CHOICES = (
        ("New", "New"),
        ("Leads", "Leads"),
        ("Found", "Found"),
        ("Closed", "Closed"), 
    )

    first_name = models.CharField(verbose_name="Given Name", max_length=200, blank=False, null=False)
    last_name = models.CharField(verbose_name="Last Name", max_length=200, blank=False, null=False)
    age = models.CharField(verbose_name="Age of Missing Person",max_length=200, blank=True, null=True, )
    gender = models.CharField(verbose_name="Gender of Missing Person", choices=GENDER_CATEGORY_CHOICES, max_length=200, blank=False, null=False)
    last_seen = models.CharField(verbose_name="Last Seen Location", max_length=200, blank=False, null=False)
    description = models.TextField(verbose_name="Any Other Important Details",max_length=1000)

    photo = models.ImageField(verbose_name="Upload Photo of Missing Person",upload_to="missingpersons/",  blank=True, null=True )
    contact_person = models.CharField(verbose_name="Contact Person", max_length=200, blank=False, null=False)
    
    contact_relationship = models.CharField(verbose_name="Relationship with Missing Person", choices=RELATIONSHIP_CATEGORY_CHOICES, max_length=200, blank=False, null=False) 
    phone = PhoneNumberField(verbose_name="Contact Number", null=True, blank=True, )

    status = models.CharField(verbose_name="Current Status", choices=CURRENT_STATUS_CHOICES, max_length=200, blank=False, null=False) 
   
    # fields used in AI face recognition
    is_verified = models.BooleanField(verbose_name="Person Background Check Done?", default=False)
    face_id = models.CharField(verbose_name="Face ID of Missing Person",max_length=200, blank=True, null=True, )
    

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Mising People'
        verbose_name_plural = 'Missing People'
        ordering = ('first_name', )

    def __str__(self): 
        return str(self.first_name) + " " + str(self.last_name)



class ReportedPerson(models.Model):

    last_seen = models.CharField(verbose_name="Last Seen Location", max_length=200, blank=False, null=False)
    description = models.TextField(verbose_name="Any Other Important Details",max_length=1000)
    photo = models.ImageField(verbose_name="Upload Photo of Reported Person",upload_to="reportedpersons/")

    # fields used in AI face recognition
    is_verified = models.BooleanField(verbose_name="Is this valid reporting?", default=False)
    face_id = models.CharField(verbose_name="Face ID of Reported Person",max_length=200, blank=True, null=True, )
    is_matched_with_missing_person = models.BooleanField(verbose_name="Has the match found?", default=False)
    matched_confindence = models.CharField(verbose_name="Details of Match", max_length=200, blank=True, null=True)
    matched_face_id = models.CharField(verbose_name="Face ID of Matched Person",max_length=200, blank=True, null=True, )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Reported People'
        verbose_name_plural = 'Reported People'
        ordering = ('created_date', )

    def __str__(self): 
        return str(self.created_date)
        