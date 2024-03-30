from django.db import models


class Contact(models.Model):
    precedenceChoices = (("primary", "primary"), ("secondary", "secondary"))
    phoneNumber = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=128, null=True)
    linkedId = models.IntegerField(null=True)
    linkPrecedence = models.CharField(max_length=10, choices=precedenceChoices)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True)

    def __str__(self):
        return (f"{str(self.id)} {self.email} {self.phoneNumber} {str(self.linkedId)} "
                f"{self.linkPrecedence}")
