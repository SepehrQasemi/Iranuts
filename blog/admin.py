from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "summary_preview")
    search_fields = ("title", "summary", "body", "author__phone")
    list_filter = ("author",)

    @admin.display(description="Summary")
    def summary_preview(self, obj):
        return (obj.summary or "")[:60]
