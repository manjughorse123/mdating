from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import *
from django import forms
from django.utils.html import format_html
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django.contrib import messages



class TestModelForm(forms.ModelForm):
    is_register_user_verified  = forms.CheckboxInput()
#     class Meta:
#         model = User
#         fields = "__all__"
#         widgets = {
#             "is_govt_id_verified": DjangoToggleSwitchWidget(klass="django-toggle-switch-success",)

#         }

class UserAdmin(admin.ModelAdmin):
#     class Media:
#         js = ('app/formset_handlers.js',)
#         css = (
#             'css/main.css',)

#     form = TestModelForm
    list_display = ('email', 'mobile', 'name', 'id','create_at',)
    list_display_links = ('email', 'name')
    list_filter = ('email', 'mobile', 'name', 'create_at')
#     list_per_page = 10
#     list_editable = ['is_register_user_verified']
#     actions = ['enable_selected', 'disable_selected']

#     def enable_selected(self, request, queryset):
#         queryset.update(is_register_user_verified=True)
#         messages.add_message(request, messages.INFO, 'User Successfully verified ')

#     def disable_selected(self, request, queryset):
#         queryset.update(is_register_user_verified=False)
#         messages.add_message(request, messages.INFO, 'User Successfully Unverified ')

#     enable_selected.short_description = "Enable the selected Post"
#     disable_selected.short_description = "Disable the selected Post"
#     # change_list_template = 'admin/index_list.html'
#     # list_editable = ('is_govt_id_verified',)


#     def govt_id_pic (self,obj):
#         return  format_html(f'<img src= "/media/{obj.govt_id}" style = height:100px;width:100px/ onclick= "manju">')
#     def is_button (self,obj):
#         return  format_html(f'<button style = height:40px;width:40px/>{obj.is_govt_id_verified}</button>'
#                            )
#         # return format_html(f'<input type="checkbox" style = height:30px;width:30px value ={obj.is_govt_id_verified}/>')
#         # return format_html(f'<div style="display:inline-block"><label class="switch"> <input type="checkbox"><span class="slider round"></span>/></label></div>')

    # readonly_fields =  ('email', 'mobile', 'name', 'otp', 'is_phone_verified', 'govt_id_pic', 'location','id', 'create_at', 'update_at')
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