from django.contrib import admin

from .models import Actor, ActorImage, ActorVideo, Application, Recruit, RecruitImage


class RecruitImageInline(admin.TabularInline):
    model = RecruitImage
    extra = 1


@admin.register(Recruit)
class RecruitAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "post_at", "closing_at", "progress")
    list_filter = ("category", "progress")
    search_fields = ("title", "movie_title", "director", "production")
    inlines = [RecruitImageInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['recruit', 'actor_name', 'created_at']

    def actor_name(self, obj):
        return obj.actor.user.username
    actor_name.short_description = 'Actor'



class ActorImageInline(admin.TabularInline):
    model = ActorImage
    extra = 1


class ActorVideoInline(admin.TabularInline):
    model = ActorVideo
    extra = 1


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("user", "stature", "weight", "education")
    list_filter = ("education",)
    search_fields = ("user__username", "user_info", "specialty")
    inlines = [ActorImageInline, ActorVideoInline]


@admin.register(ActorImage)
class ActorImageAdmin(admin.ModelAdmin):
    list_display = ("actor", "image")
    list_filter = ("actor",)
    search_fields = ("actor__user__username",)


@admin.register(ActorVideo)
class ActorVideoAdmin(admin.ModelAdmin):
    list_display = ("actor", "title", "uploaded_at")
    list_filter = ("actor", "uploaded_at")
    search_fields = ("actor__user__username", "title", "description")
