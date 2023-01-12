from django import forms


class DalleForm(forms.Form):
    SIZES = [
        ("1", "1024x1024"),
        ("2", "512x512"),
        ("3", "256x256"),
    ]
    
    size = forms.ChoiceField(choices=SIZES, label="Size:",
                             widget=forms.RadioSelect(attrs={"class": "default-indent"}))
    
    amount = forms.IntegerField(min_value=1, max_value=10, step_size=1, label="Amount:",
                                widget=forms.NumberInput(attrs={"type": "number", "class": "image_generator-amount"}))
    
    prompt_attrs = {"placeholder": "Enter your request here", "cols": "10", "rows": "10"}
    prompt = forms.CharField(widget=forms.Textarea(prompt_attrs), max_length=4000, label=False)
