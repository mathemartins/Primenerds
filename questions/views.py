from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

# Create your views here.
from videos.models import Video
from questions.models import Question
from questions.forms import QuestionForm
from notifications.signals import notify

@login_required
def question_thread(request, id):
    question = Question.objects.get(id=id)
    form = QuestionForm()

    context = {
        'form':form,
        'question':question,
    }
    return render (request, 'question/question_thread.html', context)

def question_create_view(request):
    if request.method == 'POST' and request.user.is_authenticated():
        parent_id = request.POST.get('parent_id')
        video_id = request.POST.get('video_id')
        instance_location_destination = request.POST.get('instance_location_destination')
        form = QuestionForm(request.POST)

        try:
            video = Video.objects.get(id=video_id)
        except Exception as e:
            video = None

        parent_question = None
        if parent_id is not None:
            try:
                parent_question = Question.objects.get(id=parent_id)
            except Exception as e:
                parent_question = None
            if parent_question is not None and parent_question.video is not None:
                video = parent_question.video
        if form.is_valid():
            question_text = form.cleaned_data['question']
            if parent_question is not None:
                new_question = Question.objects.create_question(
                    user = request.user,
                    destination = parent_question.get_instance_location,
                    text = question_text,
                    video = video,
                    parent = parent_question
                )
                affected_users = parent_question.get_affected_users()
                notify.send(
                    request.user,
                    action=new_question,
                    target = parent_question,
                    recipient=parent_question.user,
                    affected_users = affected_users,
                    verb = 'replied to ',
                )
                messages.success(request, "<strong>Reply</strong> posted successfully, Thank you for your reply.", extra_tags='html_safe')
                return HttpResponseRedirect(parent_question.get_absolute_url())
            else:
                new_question = Question.objects.create_question(
                    user = request.user,
                    destination = instance_location_destination,
                    text = question_text,
                    video = video,
                )
                notify.send(
                    request.user,
                    action=new_question,
                    target = new_question.video,
                    recipient=request.user,
                    verb = 'Commented on ',
                )

                #notify.send(request.user, recipient=request.user, action='new comment added')
                messages.success(request, "<strong>Comment</strong> posted successfully, Thank you for your comment.", extra_tags='html_safe')
                return HttpResponseRedirect(new_question.get_absolute_url())
        else:
            messages.error(request, "<strong>Oops!</strong>, an error occurred in your comment, please try again.", extra_tags='html_safe')
            return HttpResponseRedirect(instance_location_destination)
    else:
        raise Http404
