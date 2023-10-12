from django.db import models
from django.core.exceptions import ValidationError
from devopshobbies.core.modelmixins import SlugMixin
from devopshobbies.common.models import BaseModel
from devopshobbies.users.models import BaseUser

class Post(BaseModel, SlugMixin):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(BaseUser, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.slug
    
    def get_slug_source(self):
        return self.title
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="subs")
    target = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="targets")

    class Meta:
        unique_together = ('subscriber', 'target')

    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({"subscriber": ("subscriber cannot be equal to target")})
        
    def __str__(self) -> str:
        return f"{self.subscriber.email} - {self.target.email}"