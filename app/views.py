from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import FeedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from .models import Blog
from .forms import CommentForm
from .models import Comment  # Импорт модели комментариев
from .forms import BlogForm
from django.views.decorators.http import require_POST
from .models import Branch
from django.contrib.auth.decorators import login_required
from .models import CarouselImage
from .models import CompanyVideo# Импорт новой модели

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',  # Переведено
            'year':datetime.now().year,
        }
    )


def about(request):
    carousel_images = CarouselImage.objects.all().order_by('-created_at')[:5]
    latest_video = CompanyVideo.objects.last()  # Последнее загруженное видео

    return render(request, 'app/about.html', {
        'title': 'О нас',
        'message': 'Описание вашего приложения.',
        'carousel_images': carousel_images,
        'latest_video': latest_video,
    })

def blog_list(request):
    posts = Blog.objects.all().order_by('-posted')
    return render(request, 'app/blog/blog_list.html', {'posts': posts})

def links(request):
    return render(request, 'app/links.html', {'title': 'Полезные ресурсы'})

def feedback(request):
    context = dict()  # Создаем переменную-словарь
    
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Сохраняем данные в словарь
            context["data"] = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"] or "Не указан",
                "rating": form.cleaned_data["rating"],
                "favorite_section": dict(form.fields["favorite_section"].choices)[form.cleaned_data["favorite_section"]],
                "newsletter": "Да" if form.cleaned_data["newsletter"] else "Нет",
                "message": form.cleaned_data["message"] or "Нет сообщения",
                "visit_date": form.cleaned_data["visit_date"].strftime("%d.%m.%Y")
            }
            return render(request, "app/pool.html", context)
        else:
            context["form"] = form
            return render(request, "app/pool.html", context)
    else:
        context["form"] = FeedbackForm()
        return render(request, "app/pool.html", context)

#регистрация

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
        else:
            # Передаем форму с ошибками в шаблон
            messages.error(request, 'Исправьте ошибки в форме')
            return render(request, 'app/registration.html', {'regform': form})
    else:
        form = UserCreationForm()
    return render(request, 'app/registration.html', {'regform': form})

#блог

def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})

def blog(request):
    posts = Blog.objects.all()
    return render(request, 'app/blog.html', {'title': 'Блог', 'posts': posts, 'year': datetime.now().year})

def blogpost(request, parametr):
    post = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=post)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('blogpost', parametr=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'app/blogpost.html', {
        'post_1': post,
        'comments': comments,
        'form': form,
        'year': datetime.now().year
    })

def newpost(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = BlogForm()
    
    return render(request, 'app/newpost.html', {
        'form': form,
        'title': 'Новая статья',
        'year': datetime.now().year
    })

def videopost(request):
    return render(request, 'app/videopost.html', {
        'title': 'Видео',
        'year': datetime.now().year
    })

# app/views.py
def contact(request):
    branches = Branch.objects.all()  # Берем данные из БД
    current_day = datetime.now().strftime('%A')  # Для подсветки дня
    
    return render(request, 'app/contact.html', {
        'title': 'Контакты',
        'branches': branches,
        'current_day': current_day
    })

def contacts_view(request):
    return render(request, 'app/contact.html', {
        'title': 'Контакты',
    })



@login_required
@require_POST
def toggle_warning(request, branch_id):
    if request.user.is_superuser:
        branch = get_object_or_404(Branch, id=branch_id)
        branch.is_warning = not branch.is_warning
        branch.save()
    return redirect('contact')


