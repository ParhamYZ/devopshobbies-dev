import random
from abc import abstractmethod
from django.db import models, OperationalError
from slugify import slugify

class SlugMixin(models.Model):
    """This mixin handles auto-generating slugs"""
    slug = models.SlugField(unique=True, max_length=100)

    class Meta:
        abstract = True    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        return super().save(*args, **kwargs)

    def get_slug(self):
        slug_source = self.get_slug_source()
        slug = slugify(slug_source)
        for _ in range(300):
            slug += str(random.randint(300000,500000))
            if not self.__class__.objects.filter(slug=slug).exclude(id=self.id).exists():
                break
        else:
            raise OperationalError("System could not generate a unique slug for this new record!")
        return slug
    
    @abstractmethod
    def get_slug_source(self):
        pass
