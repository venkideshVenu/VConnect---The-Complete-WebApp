from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.contrib import messages
from core.models import CustomUser
from .models import Post, Comment, PostReport, Notification
from .forms import CommentForm, ReportPostForm, PostForm
import json
from .models import Profile

def paginate_queryset(request, queryset, per_page=10):
    """Helper function to paginate querysets"""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)

@login_required
def home_view(request):
    """Home view showing posts from followed users and own posts"""
    profile = get_object_or_404(Profile, user=request.user)
    
    # Get posts from followed users
    follows_users = profile.follows.all()
    follows_posts = Post.objects.filter(author__in=follows_users)
    
    # Get user's own posts
    user_posts = Post.objects.filter(author=request.user)
    # Combine and order posts
    post_list = (follows_posts | user_posts).distinct().order_by('-date_posted')
    
    posts = paginate_queryset(request, post_list, 4)
    notifications = Notification.objects.filter(receiver=request.user)
    context = {
        'posts': posts,
        'section': 'home',
        'notifications': notifications,
    }
    return render(request, 'socialhub/home.html', context)

@login_required
def post_detail_view(request, slug):
    """Detail view for a single post"""
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by('-date_posted')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('socialhub:post-detail', slug=post.slug)
    else:
        form = CommentForm()
        report_form = ReportPostForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'report_form': report_form
    }
    return render(request, 'socialhub/post_detail.html', context)

@login_required
def post_create_view(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return JsonResponse({'url': post.get_absolute_url()})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = PostForm()
        context = {'form': form, 'action': 'Create'}
        return render(request, 'socialhub/post_form.html', context)

@login_required
def post_update_view(request,pk):
    post1 = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,instance=post1)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.save()
            ctx = {'url':post.get_absolute_url()}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        post = get_object_or_404(Post,pk=pk)
        form = PostForm(instance = post)
        context = {
            'form': form,
            'post':post,
        }
        return render(request,'socialhub/post_form_update.html',context)
    

@login_required
def post_delete_view(request, pk=None):
    context = {}
    post = get_object_or_404(Post,pk=pk)
    
    if request.method =="POST":
        if post.author == request.user:
            post.delete()
            return redirect('socialhub:profile', username=request.user.username)
    context = {"post":post}
    return render(request,'socialhub/post_confirm_delete.html',context)

@login_required
def search_view(request):
    """Search for posts and users"""
    posts = Post.objects.all().order_by('-date_posted')
    posts = paginate_queryset(request, posts, 4)
    context = {'posts': posts, 'flag': True}
    
    if request.method == 'POST':
        search_input = request.POST.get('search', '').strip()
        if not search_input:
            messages.warning(request, "Please enter a search term")
            return render(request, 'socialhub/search.html', context)
            
        result_posts = Post.objects.filter(
            Q(title__icontains=search_input) | 
            Q(content__icontains=search_input)
        )
        users = CustomUser.objects.filter(username__iexact=search_input)
        notifications = Notification.objects.filter(receiver=request.user)
        context = {
            'posts': posts,
            'search_input': search_input,
            'result_posts': result_posts if result_posts.exists() else None,
            'users': users if users.exists() else None,
            'notifications': notifications,
        }
        
        if not (result_posts.exists() or users.exists()):
            messages.info(request, f"No results found for: {search_input}")
            
    return render(request, 'socialhub/search.html', context)

@login_required
@require_POST
def like_view(request):
    """Toggle like status on a post"""
    post_id = request.POST.get('pk')
    if not post_id:
        return JsonResponse({'error': 'Post ID is required'}, status=400)
        
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
        
    return JsonResponse({
        'likes_count': post.total_likes,
        'liked': liked,
        'post_id': f'#like{post.id}'
    })

@login_required
@require_POST
def post_report_view(request):
    """Report a post"""
    post_id = request.POST.get('pk')
    reason = request.POST.get('reason')
    
    if not all([post_id, reason]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)
        
    post = get_object_or_404(Post, pk=post_id)
    
    # Check if user already reported this post
    if PostReport.objects.filter(post=post, user=request.user).exists():
        return JsonResponse({'error': 'You have already reported this post'}, status=400)
        
    PostReport.objects.create(
        post=post,
        reason=reason,
        user=request.user
    )
    
    messages.success(request, 'Post reported successfully')
    return JsonResponse({'message': 'Report submitted successfully'})

@login_required
def notifications_view(request, username):
    """View user notifications"""
    user = get_object_or_404(CustomUser, username=username)
    if user != request.user:
        messages.error(request, "You can't view other users' notifications")
        return redirect('socialhub:home')
        
    notifications = Notification.objects.filter(receiver=user)
    notifications = paginate_queryset(request, notifications, 6)
    
    return render(request, 'socialhub/notifications.html', {
        'notifications': notifications
    })

@login_required
def notifications_update_view(request, username):
    """Mark notifications as read"""
    user = get_object_or_404(CustomUser, username=username)
    if user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    Notification.objects.filter(
        receiver=user,
        read=False
    ).update(read=True)
    
    return JsonResponse({'message': 'Notifications updated successfully'})

@login_required
def notifications_unread_count_view(request, username):
    """Get count of unread notifications"""
    user = get_object_or_404(CustomUser, username=username)
    if user != request.user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    count = Notification.objects.filter(
        receiver=user,
        read=False
    ).count()
    
    return JsonResponse({'count': count})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReportUserForm

# @login_required
def profile(request,username=None):
    report_form = ReportUserForm()
    user =  get_object_or_404(CustomUser,username=username)
    post_list = Post.objects.filter(author=user).order_by('-id')
    post_count = post_list.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 4)
    if request.user.is_authenticated:
        is_following = user in request.user.profile.follows.all()
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    
    
    context = {
        'report_form':report_form,
        'posts':posts,
        'user_id':user,
        'post_count':post_count,
        'is_following': is_following,
    }
    template_name = 'socialhub/profile.html'

    return render(request, template_name, context)



@login_required
def userFollowUnfollow(request,pk=None):
    current_user = request.user
    other_user = CustomUser.objects.get(pk=pk)

    if other_user not in current_user.profile.follows.all():
        current_user.profile.follows.add(other_user)
        other_user.profile.followers.add(current_user)
        
        notify = Notification.objects.create(sender=current_user,receiver=other_user,action="started following you.")

    else:
        current_user.profile.follows.remove(other_user)
        other_user.profile.followers.remove(current_user)
    return redirect('socialhub:profile',username=other_user.username)