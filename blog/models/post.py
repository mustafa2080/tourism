from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field # Updated to use CKEditor5
from django.db import models # Ensure models is imported directly
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings

# Import related models from the main models module now
from blog.models.category import Category
from blog.models.tag import Tag

class Post(models.Model):
    """Blog post model - Refactored for django-modeltranslation"""

    # Translatable fields (will be handled by modeltranslation)
    title = models.CharField(_('Title'), max_length=255)
    excerpt = models.TextField(_('Excerpt'), max_length=500)
    content = models.TextField(_('Content'))
    seo_title = models.CharField(_('SEO Title'), max_length=70, blank=True)
    seo_description = models.CharField(_('SEO Description'), max_length=160, blank=True)

    # Basic fields (language neutral)
    slug = models.SlugField(max_length=255, unique=True, blank=True) # Allow blank for auto-generation
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    featured_image = models.ImageField(upload_to='blog/posts/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    # Publishing fields
    is_published = models.BooleanField(_('Published'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    # Additional settings
    allow_comments = models.BooleanField(_('Allow comments'), default=True)
    featured = models.BooleanField(_('Featured'), default=False)
    view_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        # modeltranslation provides access to current language field directly
        return self.title or self.slug
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Generate slug from title (current language) if not provided
        if not self.slug and self.title:
             # Use the title attribute directly, modeltranslation handles language context
            self.slug = slugify(self.title)
            # Ensure slug uniqueness if needed (e.g., add pk or timestamp)
            # Might need more robust slug generation logic here
        super().save(*args, **kwargs)
    
    @property
    def comments_count(self):
        return self.comments.filter(approved=True).count()
    
    def increase_view_count(self):
        """Increase post view count by 1"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


# Removed PostTranslation class


class PostImage(models.Model):
    """Additional images for blog posts"""
    # Keep this model as is
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog/posts/')
    caption = models.CharField(_('Caption'), max_length=255, blank=True)
    position = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        verbose_name = _('Post Image')
        verbose_name_plural = _('Post Images')
        ordering = ['position']
    
    def __str__(self):
        return f"Image {self.position} for {self.post}"
