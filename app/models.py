
from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Ballot(models.Model):
    ballot_id = models.AutoField(primary_key=True)
    ballot_name = models.CharField(max_length=500, unique=True)
    ballot_address = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    ballot_end_date = models.DateTimeField(null=True)
    ballot_interface = models.TextField()

class BallotRegister(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'ballot_id'], name='uniqueBallotRegister')
        ]
    ballot_register_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)
    registered = models.BooleanField(default = False)
    created_on = models.DateTimeField(auto_now_add=True)

class AddressBallotRegister(models.Model):
    hash_string = models.TextField(unique=True)
    address = models.TextField()
    private_key = models.TextField()
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    tx_hash =models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=User)
def record_password_change(sender, **kwargs):
    user = kwargs.get('instance', None)
    if user:
        new_password = user.password
        print(new_password)
        try:
            old_password = User.objects.get(pk=user.pk).password
        except User.DoesNotExist:
            old_password = None

        if new_password != old_password:
            print(new_password)
            print(old_password)