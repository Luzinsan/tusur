from django import forms


class UserForm(forms.Form):
    name = forms.CharField(max_length=20, min_length=2, empty_value='heiodd')
    age = forms.IntegerField(min_value=5, max_value=150)
    # answer = forms.NullBooleanField(help_text="Ваш ответ.")
    # email = forms.EmailField()
    # ip = forms.GenericIPAddressField(required=False)
    # url = forms.URLField(required=False)
    # combo = forms.ComboField(fields=[name, age, answer])
    # image = forms.ImageField()
    # date = forms.DateField()
    # password = forms.CharField(widget=forms.PasswordInput)
    # comment = forms.CharField(widget=forms.Textarea, label='Комментарий: ', initial='Напишите здесь свой мнение!')
    # field_order = ["date", "name", "email", "password", "comment"]
