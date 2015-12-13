"""
- This module allows you to print results from your db queries in Django in nicely formatted
JSON when using the manage.py shell.  

- To use it, simply include this file somewhere in your Django project
(I reccomend making a folder called 'lib' at the root level of your project) and make sure to import it after
starting the shell.  For example, using the lib folder at the root level example, once your shell has started
simply type 'from lib.pretty_printer import pretty print'.  

-After you have imported it, simply use your query set as an argument to the pretty print function.

EXAMPLE:  pretty_print(User.objects.all())

************NOTE*************
If you are doing a .get() query, you need to surround your argument to pretty_print with square brackets.
EXAMPLE:  pretty_print([User.objects.get(id=1)])
*****************************
"""
from django.core import serializers

def pretty_print(model):
	
	data = serializers.serialize("json", model, indent=4)
	print(data)