from django.contrib import admin
from django.db import models
import chat.models


# Iterate over the defined models and add each of them to the admin console
for model in dir(chat.models):

    # Get the object from its name
    obj = getattr(chat.models, model)

    # Only add actual models, not other things defined in chat.models
    if isinstance(obj, type(models.Model)):
        admin.site.register(obj)