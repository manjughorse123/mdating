from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import *
from django.forms import ModelForm
from django.utils.html import format_html
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget

# Register your models here.

class TestModelForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {
            "is_govt_id_verified": DjangoToggleSwitchWidget(klass="django-toggle-switch-success",)

        }

class UserAdmin(admin.ModelAdmin):
    form = TestModelForm
    list_display = ('email', 'mobile', 'name', 'govt_id_pic', 'id', 'is_register_user_verified','is_button','create_at',)
    list_display_links = ('email', 'name')
    list_filter = ('email', 'mobile', 'name', 'create_at')
    list_per_page = 10


    def govt_id_pic (self,obj):
        return  format_html(f'<img src= "/media/{obj.govt_id}" style = height:100px;width:100px/>')
    def is_button (self,obj):
        return  format_html(f'<button style = height:40px;width:40px/>{obj.is_govt_id_verified}</button>')
        # return format_html(f'<input type="checkbox" style = height:30px;width:30px value ={obj.is_govt_id_verified}/>')
    readonly_fields =  ('email', 'mobile', 'name', 'otp', 'is_phone_verified', 'govt_id_pic', 'location','id', 'create_at', 'update_at')
admin.site.register(User, UserAdmin)


class GenderAdmin(admin.ModelAdmin):
    readonly_fields = ('photo_icon',)
    list_display = ('gender', 'photo_icon','icon_color','id')
    list_filter = ('gender', 'id')

    def photo_icon (self,obj):
        return  format_html(f'<img src= "/media/{obj.icon}" style = height:100px;width:100px/>')


admin.site.register(Gender, GenderAdmin)


class PassionAdmin(admin.ModelAdmin):
    readonly_fields = ('photo_icon',)
    list_display = ('passion', 'photo_icon','icon_color','id')
    list_filter = ('passion', 'id')
    def photo_icon (self,obj):
        return  format_html(f'<img src= "/media/{obj.icon}" style = height:100px;width:100px/>')

admin.site.register(Passion, PassionAdmin)

class MaritalStatusAdmin(admin.ModelAdmin):
    readonly_fields = ('photo_icon',)
    list_display = ('status','icon_color','photo_icon', 'id')
    list_filter = ('status', 'id')
    def photo_icon (self,obj):
        return  format_html(f'<img src= "/media/{obj.icon}" style = height:100px;width:100px/>')
admin.site.register(MaritalStatus, MaritalStatusAdmin)

class IdealMatchAdmin(admin.ModelAdmin):
    readonly_fields = ('photo_icon',)
    list_display = ('idealmatch','icon_color','photo_icon', 'id')
    list_filter = ('idealmatch', 'id')
    def photo_icon (self,obj):
        return  format_html(f'<img src= "/media/{obj.icon}" style = height:100px;width:100px/>')
admin.site.register(IdealMatch, IdealMatchAdmin)

class HeightAdmin(admin.ModelAdmin):
    list_display = ('height', 'id')
admin.site.register(Heigth, HeightAdmin)