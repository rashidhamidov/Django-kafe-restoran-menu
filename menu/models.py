from django.db import models
from django.forms import ModelForm, TextInput, Textarea,widgets
from mptt.models import MPTTModel, TreeForeignKey

from django.forms.widgets import FileInput, Select

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField


from django.contrib.auth.models import User


from django.utils.safestring import mark_safe
# Create your models here.
class Categori (MPTTModel):
    STATUS = (
            ('True', 'True'),
            ('False', 'False'),
    )
    TYPE = (
            ('menu', 'menu'),
            ('categori', 'categori'),
    )
    title = models.CharField (max_length=100)
    keywords = models.CharField (blank=True,max_length=255)
    description = models.CharField (max_length=255)
    status= models.CharField (max_length=10, choices=STATUS)
    
    tip= models.CharField (max_length=10, choices=TYPE,blank=True)
    slug = models.SlugField (null=False,unique=True)
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    create_at=models.DateTimeField (auto_now_add=True)
    update_at=models.DateTimeField (auto_now=True)
    def __str__(self):
        full_path=[self.title]
        k=self.parent
        while k is not None:
            full_path.append(k.title)
            k=k.parent
        return '/'.join(full_path[::-1])
    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse("categori_detail", kwargs={"slug": self.slug})


class Urun (models.Model):
    STATUS = (
            ('True', 'True'),
            ('False', 'False'),
    )
    TYPE = (
            ('menu', 'menu'),
            ('Kahvalti', 'Kahvalti'),
            ('Icecek', 'Icecek'),
            ('Diger', 'Diger'),
    )
    
    Categori = models.ForeignKey(Categori,on_delete=models.CASCADE,null=True)
    title = models.CharField (blank=True,max_length=100)
    keywords = models.CharField (blank=True,max_length=255)
    description = models.CharField (max_length=255)
    image= models.ImageField (blank=True,null=True,upload_to='images/')
    detail=RichTextUploadingField()
    price= models.FloatField (blank=True,null=True)
    tip= models.CharField (max_length=10, choices=TYPE,blank=True)
    slug = models.SlugField (null=False,unique=True)
    status= models.CharField (blank=True,max_length=10, choices=STATUS)
    create_at=models.DateTimeField (auto_now_add=True)
    update_at=models.DateTimeField (auto_now=True)
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src={} height="50"/>'.format(self.image.url))
        image_tag.short_description='Image'
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"slug": self.slug})


class Images (models.Model):
    urun=models.ForeignKey(Urun,on_delete=models.CASCADE)
    title=models.CharField (max_length=50, blank=True)
    image=models.ImageField(blank=True, null=True,upload_to='images/')
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src={} height="50"/>'.format(self.image.url))
        image_tag.short_description='Image'

class Comment (models. Model):
    STATUS=[('New', 'Yeni'),
            ('True', 'Onaylı'),
            ('False', 'Onaysız'),
    ]
    urun=models.ForeignKey(Urun,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=200)
    rate = models.IntegerField()
    status=models.CharField(max_length=10, choices=STATUS, default= 'New')
    ip = models.CharField(blank=True, max_length=20)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment','rate']


class ContentForm (ModelForm):
    class Meta:
        model = Urun
        fields =['Categori','title','slug', 'keywords', 'description','image', 'detail']
        widgets={
            'title' :TextInput(attrs={'class':'input','placeholder':'title'}),
            'slug' :TextInput(attrs={'class':'input','placeholder':'slug'}),
            'keywords' :TextInput(attrs={'class':'input','placeholder':'keywords'}),
            'description' :TextInput(attrs={'class':'input','placeholder':'description'}),
            'image':FileInput(attrs={'class':'input','placeholder':'image'}),
            'detail':CKEditorWidget(),
            

        }


class ImageFormContent(ModelForm):
    class Meta:
        model = Images
        fields = ['title','image']