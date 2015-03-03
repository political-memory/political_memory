from django.db import models
from representatives.models import Representative


class MemopolRepresentative(Representative):
    active = models.BooleanField(default=False)

    def update_active(self):
        if self.mandate_set.filter(end_date="9999-12-31"):
            self.active = True
        else:
            self.active = False
        self.save()
