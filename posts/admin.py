from django.contrib import admin
from . models import Post,Category,Comment,ChildComment

# Register your models here.
admin.site.register(Category)

admin.site.register(ChildComment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ["title","draft","created_date"]

    list_display_links = ["title","created_date"]

    search_fields = ["title","content"]

    list_filter = ["created_date"]

    class Meta:
        model = Post

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','user','created_date']