from django.contrib import admin
from roster.models import Resident, GovboardPosition, GovboardMember
from django.contrib.auth.models import User


class ResidentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'user', 'portal', 'room_number')

    def get_name(self, resident):
        return resident.user.first_name + " " + resident.user.last_name


class GovboardMemberInline(admin.TabularInline):
    model = GovboardMember
    extra = 1

class GovboardPositionAdmin(admin.ModelAdmin):
    inlines = [GovboardMemberInline]


admin.site.register(Resident, ResidentAdmin)
admin.site.register(GovboardPosition, GovboardPositionAdmin)