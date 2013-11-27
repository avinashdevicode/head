from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Count
# Create your models here.
class LinkVoteCounterManager(models.Manager):
    def get_query_set(self):
        return super(LinkVoteCounterManager, self).get_query_set().annotate(
                     votes = Count('vote')).order_by('-votes')


class Link(models.Model):
    title = models.CharField(max_length= 250, help_text= 'max no of characters allowed are 250')
    submitter = models.ForeignKey(User)
    submitted_on = models.DateField(default = datetime.now())
    rank_score = models.FloatField(default= 0.0)
    url = models.URLField('URL', max_length = 250, blank=True)
    description = models.TextField(blank=True)
    with_votes = LinkVoteCounterManager()
    objects = models.Manager()
    
    def __unicode__(self):
        return self.title
    
class Vote(models.Model):
    voter = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    
    def __unicode__(self):
        return '%s voted on %s' %(self.voter.username, self.link.title)
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(null= True)
    report_to = models.CharField(max_length=250,null= True)
    
    def __unicode__(self):
        return "%s Profile" % (self.user.username)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user= instance)
        
from django.db.models.signals import post_save
post_save.connect(create_user_profile, sender=User)
