# django-var
Various utilities suitable for Django

Manifest:

local_tags.py:
  Custom template tags for Django
  
  dget:
  Extracts values from 1 or 2 layered dictionary.
  Typical usecase is if one wants to pass multiple objects to a template and unpack tem at different locations.
  

diagnostics.py:
  Utilities for inspecting/diagnosing aspects of Django (actually, could be used for any python code)
  
  inspect_me:
  Returns information about the the method and the parent class and calling method.
  When overriding class methods in Django it is sometimes useful to know who is calling you, as this is not always obvious!

