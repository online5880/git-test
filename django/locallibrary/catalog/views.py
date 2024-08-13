from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm

# Create your views here.
# URL 을 받아서 실제 뷰를 생성한다.

# index라고 하는 함수나 클래스가 필요함.

# Flask 의 다음 함수와 같다.
# @app.route("---")
# def aaa():
#     return render_template()


# 함수형 뷰에서 로그인 정보를 체크하는 방법
@login_required
def index(request):

    # ?keyword=asdf 받을 수 있게해야한다.
    keyword = request.GET.get("keyword")

    # 세션을 가져오는 방법
    # request.session.get('mysession')
    # request.user.is_authenticated = True

    # Django ORM
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # select count(1)
    # from BookInstance
    # where status = 'a'
    num_instances_available = BookInstance.objects.filter(
        status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # keyword로 장르와 책들의 개수를 가져온다.
    num_books_by_keyword = Book.objects.filter(title__exact=keyword).count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_books_by_keyword": num_books_by_keyword,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context=context)


# LoginRequiredMixin 클래스를 상속하면 로그인이 필요해진다.
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    # template안에서 [model]_list 형태로 보여지게 된다.
    # content_object_name > 함수 view context
    # context_object_name = 'my_book_list'

    # 모델이 보여지는 방식을 지정
    # queryset = Book.objects.all()[:5]
    paginate_by = 5

    # queryset은 다음과 같이 지정할 수도 있습니다.
    # def get_queryset(self):
    #     return Book.objects.all()[:5]

    # 다음 함수를 오버라이드 해서 필요한 데이터를
    # 추가로 넣어줄 수도 있습니다.
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        context["some_data"] = "This is just some data"
        return context

    # template_name = 'books_list.html'


class BookDetailView(generic.DetailView):
    model = Book


# 함수형으로 만들었을 경우
# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')
#
#     return render(request, 'catalog/book_detail.html', context={'book': book})

# 리버스 검색
# Foreign Key가 달려있지 않은 곳에서 연결된 리스트를 찾아주는 함수
# book_instance = book.bookinstance_set.all()


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)

        context["some_data"] = "This is just some data"
        return context


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstancelist_borrowed_user.html"
    paginate_by = 5

    def get_queryset(self):
        return (BookInstance.objects.filter(
            borrow_id=self.request.user).filter(
                status__exact="o").order_by("due_back"))


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # POST 요청이면 폼 데이터를 처리한다
    if request.method == "POST":

        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # 폼이 유효한지 체크한다:
        if book_renewal_form.is_valid():
            # form.cleaned_data 데이타를 요청받은대로 처리한다(여기선 그냥 모델 due_back 필드에 써넣는다)
            book_instance.due_back = book_renewal_form.cleaned_data[
                "renewal_date"]
            book_instance.save()

            # 새로운 URL로 보낸다:
            return HttpResponseRedirect(reverse("all-borrowed"))

    # GET 요청 (혹은 다른 메소드)이면 기본 폼을 생성한다.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(
            weeks=3)
        book_renewal_form = RenewBookForm(
            initial={"renewal_date": proposed_renewal_date})

    context = {
        "form": book_renewal_form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/book_renew_librarian.html", context)
