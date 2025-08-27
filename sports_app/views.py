import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from sports_app.forms import RegisterForm, ProfileForm, ExerciseForm, \
    WorkoutForm, WorkoutRoutineForm, WorkoutExerciseFormSet, WorkoutPlanForm, \
    WorkoutPlanScheduleFormset, ExerciseSearchForm, WorkoutSearchForm, \
    WorkoutScheduleForm
from sports_app.models import (
    Exercise,
    Workout,
    WorkoutRoutine, Profile, WorkoutPlan, WorkoutSchedule,
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
    return render(request, "sports_app/index.html", context=context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("sports_app:profile-form")
    else:
        form = RegisterForm()
    return render(
        request,
        "registration/register.html",
        {"form": form}
    )


class ProfileFormView(LoginRequiredMixin, generic.CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "sports_app/profile_form.html"
    success_url = reverse_lazy("sports_app:index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProfileListView(LoginRequiredMixin, generic.ListView):
    model = Profile
    context_object_name = "profile_list"
    template_name = "sports_app/profile_list.html"
    paginate_by = 5


class ExerciseListView(generic.ListView):
    model = Exercise
    context_object_name = "exercise_list"
    template_name = "sports_app/exercise_list.html"
    paginate_by = 5


    def get_context_data(
        self, *, object_list=..., **kwargs
    ):
        context = super(ExerciseListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("model", "")
        context["search_form"] = ExerciseSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ExerciseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset

class WorkoutListView(generic.ListView):
    model = Workout
    context_object_name = "workout_list"
    template_name = "sports_app/workout_list.html"
    paginate_by = 5

    def get_context_data(
        self, *, object_list=..., **kwargs
    ):
        context = super(WorkoutListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("model", "")
        context["search_form"] = WorkoutSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = WorkoutSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset


class WorkoutRoutineListView(LoginRequiredMixin, generic.ListView):
    model = WorkoutRoutine
    context_object_name = "routine_list"
    template_name = "sports_app/workout_routine(not used yet)/workout_routine_list.html"
    paginate_by = 5

    def get_queryset(self):
        return WorkoutRoutine.objects.filter(profile__user=self.request.user)


class ProfileDetailView(generic.DetailView):
    model=Profile
    queryset = Profile.objects.select_related("user")
    template_name = "sports_app/profile_detail.html"

    def get_object(self, queryset=None):
        user = self.request.user
        if hasattr(user, 'profile'):
            return user.profile
        else:
            return redirect(reverse_lazy("sports_app:profile-form"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        current = profile.workout_plans.filter(current=True).first()
        if current:
            context["current_workout"] = current
        return context



class WorkoutDetailView(generic.DetailView):
    model=Workout
    template_name = "sports_app/workout_detail.html"
    context_object_name = "workout"


class WorkoutPlanDetailView(generic.DetailView):
    model=WorkoutPlan
    template_name = "sports_app/workout_plan_detail.html"
    context_object_name = "workout_plan"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        days = [
            ("1", "Monday"),
            ("2", "Tuesday"),
            ("3", "Wednesday"),
            ("4", "Thursday"),
            ("5", "Friday"),
            ("6", "Saturday"),
            ("7", "Sunday"),
        ]
        schedules_by_day = {num: [] for num, _ in days}
        for s in self.object.schedules.all():
            schedules_by_day[s.weekday].append(s)

        days_with_schedules = [
            (label, schedules_by_day[num]) for num, label in days
        ]
        context["days_with_schedules"] = days_with_schedules
        return context

class ExerciseDetailView(generic.DetailView):
    model=Exercise
    template_name = "sports_app/exercise_detail.html"
    context_object_name = "exercise"


class WorkoutRoutineDetailView(generic.DetailView):
    model=WorkoutRoutine
    template_name = "sports_app/workout_routine(not used yet)/workout_routine_detail.html"

    def get_queryset(self):
        return WorkoutRoutine.objects.select_related("workout")


class ExerciseFormView(generic.FormView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "sports_app/exercise_form.html"
    success_url = reverse_lazy("sports_app:exercise-list")


class WorkoutFormView(generic.FormView):
    model = Workout
    form_class = WorkoutForm
    template_name = "sports_app/workout_form.html"


class WorkoutRoutineFormView(generic.FormView):
    model = WorkoutRoutine
    form_class = WorkoutRoutineForm
    template_name = "sports_app/workout_form.html"


DEFAULT_IMAGES = {
        'chest': 'default_image_1_public_id',
        'back': 'default_image_2_public_id',
        'shoulders': 'default_image_3_public_id',
        'arms': 'default_image_4_public_id',
        'core': 'default_image_5_public_id',
        'legs': 'default_image_6_public_id',
    }

class ExerciseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "sports_app/exercise_form.html"
    success_url = reverse_lazy("sports_app:exercise-list")


class ExerciseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = "sports_app/exercise_form.html"
    success_url = reverse_lazy("sports_app:exercise-list")


class WorkoutCreateView(LoginRequiredMixin, generic.CreateView):
    model = Workout
    form_class = WorkoutForm
    template_name = "sports_app/workout_form.html"
    success_url = reverse_lazy("sports_app:workout-list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = WorkoutExerciseFormSet(self.request.POST)
        else:
            data["formset"] = WorkoutExerciseFormSet()
        return data


class WorkoutPlanCreateView(LoginRequiredMixin, generic.CreateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = "sports_app/workout_plan_form.html"

    def get_success_url(self):
        return reverse("sports_app:workout-schedule-update", kwargs={
            "pk": self.object.id
        })

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = WorkoutPlanScheduleFormset(self.request.POST)
        else:
            data["formset"] = WorkoutPlanScheduleFormset()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return redirect(
            "sports_app:workout-schedule-update",
            pk=self.object.pk
        )


class WorkoutScheduleUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = WorkoutPlan
    template_name = "sports_app/workout_schedule_form.html"
    fields = []
    success_url = reverse_lazy("sports_app:index")

    def get_formset_class(self):
        return inlineformset_factory(
            parent_model=WorkoutPlan,
            model=WorkoutSchedule,
            form=WorkoutScheduleForm,
            extra=self.object.days_per_week,
            max_num=7,
            can_delete=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "formset" not in context:
            context["formset"] = self.get_formset_class()(
                instance=self.object,
                prefix="schedules"
            )
        else:
            context["formset"] = kwargs["formset"]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset_class()(
            self.request.POST,
            instance=self.object,
            prefix="schedules"
        )

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(self.get_success_url())

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
class WorkoutPlanUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = WorkoutPlan
    form_class = WorkoutPlanForm
    template_name = "sports_app/workout_plan_form.html"
    success_url = reverse_lazy("sports_app:index")


class WorkoutUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = "sports_app/workout_form.html"
    success_url = reverse_lazy("sports_app:workout-list")


class WorkoutRoutineCreateView(LoginRequiredMixin, generic.CreateView):
    model = WorkoutRoutine
    form_class = WorkoutRoutineForm
    template_name = "sports_app/workout_routine(not used yet)/workout_routine_form.html"
    success_url = reverse_lazy("sports_app:workout-routine-list")