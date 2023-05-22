from django.contrib import admin
from .models import *


admin.register(Citi)
admin.register(User)
admin.register(Stage)


@admin.register(Stage)
class Stage_admin(admin.ModelAdmin):
    list_display = ('id', 'current_stage', 'next_stage')
    list_display_links = ('id',)
    list_editable = ('current_stage', 'next_stage')


@admin.register(Citi)
class Citi_admin(admin.ModelAdmin):
    list_display = ('id', 'data')
    list_display_links = ('id',)
    list_editable = ('data', )


@admin.register(User)
class User_admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'vk_uid', 'stage', 'used_citi')
    list_display_links = ('id', 'name')
    list_editable = ('vk_uid', 'stage', 'used_citi')



# @admin.register(Game)
# class Game_admin(admin.ModelAdmin):
#     list_display = ('id', 'game_session', 'vk_uid', 'citi', 'used')
#     list_display_links = ('id',)
#     list_editable = ('game_session', 'vk_uid', 'citi', 'used')