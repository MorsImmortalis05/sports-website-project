from django.contrib.auth.views import LogoutView
from django.urls import path, include

import sports_app
from sports_app.views import index, ProfileListView, ExerciseListView, \
    WorkoutListView, WorkoutRoutineListView, WorkoutDetailView, \
    ProfileDetailView, register, ProfileFormView, ExerciseFormView, \
    WorkoutFormView, WorkoutRoutineFormView, ExerciseCreateView, \
    WorkoutCreateView, WorkoutRoutineCreateView, ExerciseDetailView, \
    WorkoutUpdateView, ExerciseUpdateView, WorkoutPlanCreateView, \
    WorkoutPlanDetailView, WorkoutPlanUpdateView, WorkoutScheduleUpdateView

app_name = "sports_app"


urlpatterns = [
    path("", index, name="index"),
    path("createprofile/",
         ProfileFormView.as_view(),
         name="profile-form"),
    path(
        "register/",
        register,
        name="user-register"
    ),
    path(
        "profiles/",
        ProfileListView.as_view(),
        name="profile-list",
    ),
    path(
        "exercises/",
        ExerciseListView.as_view(),
        name="exercise-list",
    ),
    path(
        "workouts/",
        WorkoutListView.as_view(),
        name="workout-list",
    ),
    path(
        "routines/",
        WorkoutRoutineListView.as_view(),
        name="workout-routine-list",
    ),
    path(
        "workouts/<int:pk>/",
        WorkoutDetailView.as_view(),
        name="workout-detail"
    ),
    path(
        "profiles/<int:pk>/",
        ProfileDetailView.as_view(),
        name="profile-detail"
    ),
    path(
        "exercises/<int:pk>/",
        ExerciseDetailView.as_view(),
        name="exercise-detail"
    ),
    path('accounts/logout/',
         LogoutView.as_view(next_page='/'),
         name='logout'),
    path('exercises/create',
         ExerciseCreateView.as_view(),
         name='exercise-create'),
    path('workouts/create',
         WorkoutCreateView.as_view(),
         name='workout-create'),
    path('workoutroutines/create',
         WorkoutRoutineCreateView.as_view(),
         name='add-workout-routine'),
    path('workouts/<int:pk>/update',
         WorkoutUpdateView.as_view(),
         name='workout-update'),
    path('exercises/<int:pk>/update',
         ExerciseUpdateView.as_view(),
         name='exercise-update'),
    path("profiles/<int:pk>/create-workout-plan",
         WorkoutPlanCreateView.as_view(),
         name="workout-plan-create"),
    path("workout-plans/<int:pk>",
         WorkoutPlanDetailView.as_view(),
         name="workout-plan-detail"),
    path("workout-plans/<int:pk>/schedule",
         WorkoutPlanUpdateView.as_view(),
         name="workout-plan-update"),
    path("workout-plans/<int:pk>/schedule-update",
         WorkoutScheduleUpdateView.as_view(),
         name="workout-schedule-update")
]
