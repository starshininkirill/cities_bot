from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, null=True)
    vk_uid = models.IntegerField(null=True)
    stage = models.CharField(max_length=100, null=True, default='menu')
    used_citi = models.TextField(null=True, default='')
    #used_citi = models.JSONField(null=True)
    # game_session = models.IntegerField(null=True)


class Stage(models.Model):
    current_stage = models.CharField(max_length=40, null=True)
    next_stage = models.CharField(max_length=40, null=True)


class Citi(models.Model):
    data = models.JSONField(null=True)
    # name = models.CharField(max_length=100, null=True)
    #
    # def __str__(self):
    #     return self.name


# class Game(models.Model):
#     game_session = models.IntegerField(null=True)
#     vk_uid = models.IntegerField(null=True)
#     citi = models.ForeignKey(Citi, on_delete=models.CASCADE)
#     used = models.BooleanField(null=True)


