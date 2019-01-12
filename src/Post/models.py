from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class GeneralPost(models.Model):
	author = models.ForeignKey(
		User, related_name= 'user_posts', on_delete=models.CASCADE)
	title = models.CharField(verbose_name= ('post title'),
							 null=False, blank=False, max_length=30)
	content= models.TextField(verbose_name= ('post content'),
							  blank=False, max_length=40000)
	created = models.DateTimeField(verbose_name=('post created'),
								   auto_now_add=True)
	last_edited = models.DateTimeField(verbose_name= ('post edited'),
									   auto_now=True)
	img = models.ImageField(verbose_name=('Image'), upload_to='images/',blank=True)

	tag = models.CharField(verbose_name=('post tag'),
						   blank=True, max_length=40)
	published = models.BooleanField(default=False)



	class Meta:
		verbose_name = ('general post')
		verbose_name_plural = ('general posts')

	def __str__(self):
		return f'{self.pk}:{self.author}:{self.title}:{self.created}'