from django import forms
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .admin import (
    #SiteAdmin,
    CameraAdmin,
    #PenguinCountAdmin,
    PenguinObservationAdmin,
    VideoAdmin,
)
from .models import (
    #Site,
    Camera,
    #PenguinCount,
    PenguinObservation,
    Video,
    UserHelper
)


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class UserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'last_login')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'groups')}),
    )
    form = UserChangeForm
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_superuser',
        'is_staff',
        'is_active',
        'observation_count',
        'completion_count',
        'completion_hours',
    )
    list_filter = UserAdmin.list_filter + ('groups__name',)
    filter_horizontal = ('groups',)
    readonly_fields = ('email', 'last_login')

    def changelist_view(self, request, extra_context=None):
        context = {}
        context.update(extra_context or {})
        return super(UserAdmin, self).changelist_view(request, context)

    def response_add(self, request, obj, post_url_continue=None):
        return super(UserAdmin, self).response_add(request, obj, post_url_continue)

    def completion_hours(self,obj):
        if not obj  :
            return "-"
        else:
            return UserHelper.completion_hours(obj)
    completion_hours.short_description = "Completion Hours"

    def completion_count(self,obj):
        if not obj  :
            return "-"
        else:
            return UserHelper.completion_count(obj)
    completion_count.short_description = "Completion Count"

    def observation_count(self,obj):
        if not obj  :
            return "-"
        else:
            return UserHelper.observation_count(obj)
    observation_count.short_description = "Observation Count"


class PenguinSite(AdminSite):

    def has_permission(self, request):
        return request.user.is_active

    def index(self, request, extra_context=None):
        cameras = Camera.objects.filter(active=True)
        context = {
            'cameras': cameras,
        }
        context.update(extra_context or {})
        return super(PenguinSite, self).index(request, context)


site = PenguinSite()
site.register(Camera, CameraAdmin)
site.register(Video, VideoAdmin)
site.register(PenguinObservation, PenguinObservationAdmin)
site.register(User, UserAdmin)
#site.register(Site, SiteAdmin)
#site.register(PenguinCount, PenguinCountAdmin)
