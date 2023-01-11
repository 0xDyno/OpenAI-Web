from django import forms


# class CustomRadioFieldRenderer(django.forms.renderers.DjangoTemplates):
#     def engine(self):
#         # Render the choices without the div blocks
#         return '\n'.join(['%s\n%s' % (w.tag(), w.choice_label) for w in self])


class ChatGPTForm(forms.Form):
    MODELS = [
        ("text-davinci-003", "text-davinci-003"),
        ("code-davinci-002", "code-davinci-002"),
        ("text-curie-001", "text-curie-001"),
        ("text-babbage-001", "text-babbage-001"),
        ("text-ada-001", "text-ada-001"),
    ]
    
    model = forms.ChoiceField(choices=MODELS, label=False,
                              widget=forms.RadioSelect(attrs={"class": "default-indent"}))
    
    accuracy = forms.IntegerField(min_value=0, max_value=100, step_size=1,
                                  widget=forms.NumberInput(attrs={"type": "range"}))
    
    prompt_attrs = {"placeholder": "Enter your request here", "cols": "10", "rows": "10"}
    prompt = forms.CharField(max_length=4000, label=False,
                             widget=forms.Textarea(prompt_attrs))


class DalleForm(forms.Form):
    SIZES = [
        ("1", "1024x1024"),
        ("2", "512x512"),
        ("3", "256x256"),
    ]
    
    size = forms.ChoiceField(choices=SIZES, label="Size:",
                             widget=forms.RadioSelect(attrs={"class": "default-indent"}))
    
    amount = forms.IntegerField(min_value=1, max_value=10, step_size=1, label="Amount:",
                                widget=forms.NumberInput(attrs={"type": "number", "class": "generate-amount"}))
    
    prompt_attrs = {"placeholder": "Enter your request here", "cols": "10", "rows": "10"}
    prompt = forms.CharField(widget=forms.Textarea(prompt_attrs), max_length=4000, label=False)
