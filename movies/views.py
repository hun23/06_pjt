from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Comment
from .forms import MovieForm, CommentForm
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

@require_http_methods(['GET', 'POST'])
@login_required()
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/create.html', context)

@require_http_methods(['GET'])
@login_required()
def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    context = {
        'movie': movie,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, 'movies/detail.html', context)

@require_http_methods(['POST'])
@login_required()
def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user == movie.user:
        movie.delete()
    return redirect('movies:index')

@require_http_methods(['GET','POST'])
@login_required()
def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user != movie.user:
        return render(request, 'movies/index.html')
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies/update.html', context)

# ===== 댓글 ======
# 1) 댓글 작성
@require_http_methods(['POST'])
@login_required()
def comments_create(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    parent_pk = request.POST.get('parent_pk')
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        if parent_pk:
            comment.parent = Comment.objects.get(pk=parent_pk)
        comment.movie = movie
        # 댓글 작성시 작성자 정보가 함께 저장
        comment.user = request.user
        comment.save()
    return redirect('movies:detail', movie.pk)

# 2) 댓글 삭제
@require_http_methods(['POST'])
@login_required()
def comments_delete(request, movie_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user: 
        comment.delete()
    return redirect('movies:detail', movie_pk)

# 3) like
@require_http_methods(['POST'])
@login_required()
def likes(request, movie_pk):
    if request.user.is_authenticated: 
        movie = Movie.objects.get(pk=movie_pk)
        
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)  

        else:
            movie.like_users.add(request.user) 
        return redirect('movies:index') 
    
    return redirect('movies:login')  
