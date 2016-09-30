from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.shortcuts import render, redirect, HttpResponseRedirect, Http404, get_object_or_404
from django.utils.safestring import mark_safe
# Create your views here.
# custom import

#from comments.forms import CommentForm
#from comments.models import Comment

from questions.forms import QuestionForm
from questions.models import Question
from videos.models import Video, Category, TaggedItem

#@login_required
def staff_home(request):
    context = {}
    return render (request, "video/video_home.html", context)

@login_required
def video_detail(request, cat_slug, vid_slug):
    cat = get_object_or_404(Category, slug=cat_slug)
    obj = get_object_or_404(Video, slug=vid_slug, category=cat)
    if request.user.is_authenticated() or obj.has_preview:
        questions = obj.question_set.all()
        for q in questions:
            q.get_children()

        question_form = QuestionForm()

        context = {
            "obj":obj,
            "questions":questions,
            "question_form":question_form,
        }
        return render (request, "video/video_detail.html", context)
    else:
        next_url = obj.get_absolute_url()
        return HttpResponseRedirect("%s?next=%s" %(reverse('login'), next_url))


#@login_required
def category_list(request):
    queryset = Category.objects.all()
    context = {
        "queryset":queryset,
    }
    return render (request, "video/category_list.html", context)

#@login_required
def category_detail(request, cat_slug):
    #destination = request.get_full_path()
    obj = get_object_or_404(Category, slug=cat_slug)
    queryset = obj.video_set.all()
    context = {
        "obj":obj,
        "queryset":queryset,
    }
    return render (request, "video/video_list.html", context)






#def video_edit(request):
#    context = {}
#    return render (request, "video/video_edit.html", context)

#def video_create():
#    context = {}
#    return render (request, "video/video_create.html", context)
