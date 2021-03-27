from django.shortcuts import (render,
                                HttpResponseRedirect,
                                reverse,
                                get_object_or_404,
                                redirect,
                                Http404,
                                )
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, 
                                CreateView, 
                                DetailView, 
                                UpdateView, 
                                DeleteView, 
                                FormView,
                                )

from django.contrib.auth import (login, 
                                authenticate, 
                                get_user_model, 
                                logout)
import datetime

# Create your views here.

from blog.models import Post, Comment
from blog.forms import PostForm, CommentsForm
from blog.forms import UserProfileInfoForm,UserRegister

User = get_user_model()


class PostListView(ListView):
    model = Post
    
    template_name = 'blog/post_list.html'
    
        
        
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self, **kwargs).get_context_data(**kwargs)
        qs = Post.objects.filter(published=True)
        context['qs']=qs
        return context
    

class DraftListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Post
    permission_required = ('blog.delete_post')
    
    template_name = 'blog/post_list.html'
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Post.objects.filter(published=False)
        context['qs']=qs
        return context


class PostDetailView(DetailView, FormView):
    model = Post
    form_class = CommentsForm
    template_name = 'blog/detail_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentsForm
        context['comments_list'] = Comment.objects.filter(post=self.get_object())
        return context
    
    def get_object(self):
        obj = Post.objects.get(id=self.kwargs.get('pk'))
        return obj
    
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        form = self.get_form()
        if form.is_valid() and request.user.is_authenticated:
            author=request.user
            text=form.cleaned_data.get("text")
            comment = Comment.objects.create(author=author, text=text)
            comment.post = obj
            comment.save()
            qs = Comment.objects.all()
            context = {
                'form': form,
                'qs' : qs
            }
            return redirect('detail-cbv', kwargs={ 'pk' : self.kwargs.get('pk') })
        else:
            return Http404('Form is invalid or User doesn\'t exist')
            
        
    
class CreatePostView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/login/'
    permission_required = ('blog.delete_post')
    redirect_field_name = 'blog/detail_list.html'
    form_class = PostForm
    model = Post
    
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    permission_required = ('blog.delete_post')

    redirect_field_name = 'blog/post_list.html'

    form_class = PostForm

    model = Post
    
    
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    
    permission_required = ('blog.delete_post')
    raise_exception=False
    
    
    model = Post
    success_url= reverse_lazy('list-cbv')
    
def about(request):
    print(request.user.is_superuser)
    return render(request, 'blog/about.html')    



#################################################################


def login_user(request):
    form = UserProfileInfoForm(request.POST or None)
    context = {
        'form' : form
    }
    if request.POST:
       if form.is_valid():
           name = form.cleaned_data.get('name')
           email = form.cleaned_data.get('email')
           password = form.cleaned_data.get('password')
        #    phone_num = form.cleaned_data.get('phone_num')
           
           user = authenticate(request, username=name, email=email, password=password)
           if user is not None:
               login(request, user)
               form = UserProfileInfoForm(request.POST or None)
               return redirect('list-cbv')
           else:
               print("User not found")
    else:
        form = UserProfileInfoForm(request.POST or None)
    return render(request, 'blog/login.html', context)
    




def register_user(request):
    form = UserRegister(request.POST or None)
    context = {
        'form':form
    }
    if request.POST:
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            User = authenticate(request, username=name, email=email, password=password)
            print(User)
            if User is None:
                new_user = user.objects.create_user(username=name, email=email, password=password)
                new_user.save()
                return redirect('list-cbv')
    return render(request, 'blog/register.html', context)

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('list-cbv'))


######################################################################




## PUBLISH  URL BAKI 6E
@login_required
def publish_button(request, pk=None):
    post = Post.objects.get(pk=pk)
    post.publish_post()
    return redirect('list-cbv')
    
    
    


## MAKE COMMENTS  URL BAKI 6E
@login_required
def create_comments(request):
    form = CommentsForm(request.POST or None)
    context = {
                'form': form,
                
            }
    if request.POST and request.user.is_authenticated:
        if form.is_valid():
            author=request.user
            text=form.cleaned_data.get("text")
            comment = Comment.objects.create_object(author=author, text=text)
            comment.save()
            qs = Comment.objects.all()
            context = {
                'form': form,
                'qs' : qs
            }
            return redirect('detail-cbv')

    else:
        form = CommentsForm(request.POST or None)
    return render(request, 'blog/detail-cbv', context)

## DELETE COMMENTS  URL BAKI 6E


## DRAFTS  URL BAKI 6E