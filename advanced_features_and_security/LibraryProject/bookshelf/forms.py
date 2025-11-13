from django import forms

class ExampleForm(forms.Form):
    """
    A simple form to demonstrate data validation and safe rendering 
    (which prevents XSS by default).
    """
    title = forms.CharField(
        max_length=100,
        label='Title',
        help_text='Enter a book title (max 100 characters).'
    )
    author = forms.CharField(
        max_length=100,
        label='Author',
        help_text='Enter the author\'s name.'
    )
    
    # Example of a field with specific validation requirements
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        label='Rating (1-5)',
        help_text='Rate the book from 1 to 5.'
    )