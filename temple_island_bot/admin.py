from django.contrib import admin

from temple_island_bot.models import User, UserWallet


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'pending_state',
        'chat_id',
    )


@admin.register(UserWallet)
class UsersWallets(admin.ModelAdmin):
    list_display = (
        'id',
        'get_user_name',
        'address',
        'image_url'
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(UsersWallets, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].label_from_instance = lambda inst: f"{inst.first_name}"
        return form