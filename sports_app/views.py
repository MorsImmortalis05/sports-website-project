import datetime
from http.client import HTTPResponse

from django.http import HttpRequest
from django.shortcuts import render

from sports_app.models import (
    Exercise,
    Workout,
    WorkoutRoutine,
)


def index(request: HttpRequest):
    exercises = Exercise.objects.count()
    workouts = Workout.objects.count()
    workouts_attended_today = WorkoutRoutine.objects.filter(
        date=datetime.date.today())
    context = {
        "exercises": exercises,
        "workouts": workouts,
        "workouts_attended_today": workouts_attended_today,
    }
    return render(request, sports_app/index.html, context=context)
