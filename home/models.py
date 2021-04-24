from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from django.forms import ModelForm, TextInput, Textarea,widgets
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
# Create your models here.



# Create your models here.
class Ayarlar (models.Model):
    STATUS = (
            ('True', 'Evet'),
            ('False', 'Hayır'),
    )
    baslik=models.CharField(blank=True,max_length=150)
    anahtar_kelime=models.CharField(blank=True,max_length=250)
    company=models.CharField(blank=True,max_length=50)
    adress=models.CharField(blank=True,max_length=150)
    phone=models.CharField(blank=True,max_length=20)
    phone_2=models.CharField(blank=True,max_length=20)
    fax=models.CharField(blank=True,max_length=15)
    email=models.CharField(blank=True,max_length=50)
    smtpserver=models.CharField(blank=True,max_length=20)
    smtpemail=models.CharField(blank=True,max_length=20)
    smtp_password=models.CharField(blank=True,max_length=15)
    smtp_port=models.CharField(blank=True,max_length=5)
    icon=models.ImageField (blank=True, upload_to='images/')
    logo=models.ImageField (blank=True, upload_to='images/')
    facebook=models.CharField(blank=True,max_length=255)
    twitter=models.CharField(blank=True,max_length=50)
    instagram=models.CharField(blank=True,max_length=50)
    hakkimizda=RichTextUploadingField()
    iletisim=RichTextUploadingField()
    referanslar=RichTextUploadingField()
    status=models.CharField(blank=True,max_length=10,choices=STATUS)
    create_at=models.DateTimeField (auto_now_add=True)
    update_at=models.DateTimeField (auto_now=True)
    def __str__(self):
        return self.baslik

class ContactFormMessage(models.Model):
    STATUS = (
            ('New', 'Yeni'),
            ('Read', 'Okundu'),
            ('Closed', 'Cevaplandi'),
    )
    name=models.CharField(blank=True,max_length=20)
    email=models.CharField(blank=True,max_length=50)
    subject=models.CharField(blank=True,max_length=50)
    message=models.CharField(blank=True,max_length=250)
    ip=models.CharField(blank=True,max_length=20)
    note=models.CharField(blank=True,max_length=100)
    status=models.CharField(blank=True,max_length=20,choices=STATUS,default='New')
    create_at=models.DateTimeField (auto_now_add=True)
    update_at=models.DateTimeField (auto_now=True)

    def __str__(self):
        return self.name

class ContactFormu(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name','subject','email','message']
        widgets={
        'name' : TextInput(attrs={'class':'input','placeholder':'Name & Surname'}),
        'subject'  : TextInput(attrs={'class':'input','placeholder':'Subject'}),
        'email' : TextInput(attrs={'class':'input','placeholder':'Email Adress'}),
        'message' : TextInput(attrs={'class':'input','placeholder':'Your Message','rows':'5'}),
            }


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,blank=True) 
    city = models.CharField(max_length=20,blank=True) 
    country = models.CharField(max_length=50,blank=True) 
    adress = models.CharField(max_length=150,blank=True) 
    image=models.ImageField (blank=True, upload_to='images/users')

    def user_name(self):
        return self.user.username
    def Full_name(self):
        return self.user.first_name+'  '+self.user.last_name
    def image_tag(self):
        return mark_safe('<img src={} height="50"/>'.format(self.image.url))
        image_tag.short_description='Image'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone','city','country','adress','image']

class FAQ(models.Model):
    STATUS = (
            ('True', 'Evet'),
            ('False', 'Hayır'),
    )
    ordernumber=models.IntegerField()
    question=models.CharField(blank=True,max_length=250)
    answer=models.TextField(blank=True)
    status=models.CharField(blank=True,max_length=10,choices=STATUS)
    create_at=models.DateTimeField (auto_now_add=True)
    update_at=models.DateTimeField (auto_now=True)
    def __str__(self):
        return self.question