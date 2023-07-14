from django.db import models
import uuid
from user import models as usermodel



# Create your models here.
class Project(models.Model):
    owner=models.ForeignKey(usermodel.Profile, on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    demo_link=models.CharField(max_length=2000,null=True,blank=True)
    source_link=models.CharField(max_length=2000,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    tags=models.ManyToManyField('Tag',blank=True)
    vote_total=models.IntegerField(default=0,blank=True,null=True)
    vote_ratio=models.IntegerField(default=0,blank=True,null=True)
    image=models.ImageField(null=True, blank=True,default='default.jpg')
    def __str__(self):
        return self.title
    class Meta:
        ordering=['-vote_ratio','-vote_total','title']

    @property
    def reviewers(self):
        querySet=self.review_set.all().values_list('owner_id',flat=True)    
        return querySet

    @property
    def getVote(self):
        reviews=self.review_set.all()
        upvote=reviews.filter(value='up').count()
        totalvote=reviews.count()
        ratio=(upvote//totalvote)*100
        self.vote_ratio=ratio
        self.vote_total=totalvote
        self.save()    
    

class review(models.Model):
    VOTE_TYPE=(('up','Upvote'),('down','Downvote'))
    owner=models.ForeignKey(usermodel.Profile,on_delete=models.CASCADE,null=True)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)    
    value=models.CharField(max_length=200,choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    class Meta:
        unique_together=[['owner','project']]
    
    def __str__(self):
        return self.value

class Tag(models.Model):

    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.name
