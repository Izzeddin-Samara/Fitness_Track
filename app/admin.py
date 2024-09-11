from django.contrib import admin
from django import forms  
from .models import Coach, Experience, Education
import bcrypt

class CoachForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True) 

    class Meta:
        model = Coach
        fields = ('first_name', 'last_name', 'email', 'image', 'bio', 'password')  

class CoachAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'image', 'created_at')
    form = CoachForm  

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['password']:
            
            obj.password = bcrypt.hashpw(form.cleaned_data['password'].encode(), bcrypt.gensalt()).decode()
        super().save_model(request, obj, form, change)

admin.site.register(Coach, CoachAdmin)
admin.site.register(Experience)
admin.site.register(Education)