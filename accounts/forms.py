from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    nickname = forms.CharField(label="Enter your nickname here")
    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_details = User.objects.filter(email=email)
        if user_details.exists():
            raise forms.ValidationError("There is already an account with this email , please try logging in!")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        # user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'nickname', 'hidden','is_active', 'is_admin', 'is_staff')