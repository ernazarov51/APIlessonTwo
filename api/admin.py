from django.contrib import admin

from api.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    exclude = 'created_at', 'updated_at'
# Register your models here.
