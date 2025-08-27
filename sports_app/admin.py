from django.contrib import admin

from sports_app.models import Profile, Workout, WorkoutExercise, \
    WorkoutRoutine, Exercise

admin.site.register(Profile)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(WorkoutExercise)
admin.site.register(WorkoutRoutine)
