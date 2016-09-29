from django import forms



class CommentForm(forms.Form):
	"""docstring for CommentForm"""
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	#parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
	content = forms.CharField(label='', widget=forms.Textarea)
	#def __init__(self, arg):
	#	super(CommentForm, self).__init__()
	#	self.arg = arg
