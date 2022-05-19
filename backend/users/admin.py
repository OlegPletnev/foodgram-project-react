from django.contrib import admin
from users.models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'full_name',
        'followers_count',
    )
    filter_fields = ('username', 'email',)
    ordering = ('id',)

    def full_name(self, obj):
        return obj.get_full_name()

    def followers_count(self, obj):
        return obj.follower.count()

    followers_count.short_description = 'Число подписчиков'


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    search_fields = (
        'user',
        'author',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
