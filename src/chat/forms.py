from django import forms


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
