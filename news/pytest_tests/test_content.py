from datetime import datetime, timedelta

import pytest
from pytest_lazyfixture import lazy_fixture

from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from news.models import Comment

User = get_user_model()


@pytest.mark.parametrize(
    'parametrized_client, form_news_home',
    (
        (lazy_fixture('author_client'), True),
        (lazy_fixture('client'), True),
    )
)
@pytest.mark.django_db
def home_for_different_users(
        news, parametrized_client
):
    url = reverse('news:home')
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    assert news in object_list


@pytest.mark.django_db
def test_news_count(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    first_news_date = object_list[0].date
    all_dates = [all_news.date for all_news in object_list]
    assert first_news_date == max(all_dates)


def test_edit_comment_page_contains_form(id_for_args, author_client):
    url = reverse('news:edit', args=id_for_args)
    response = author_client.get(url)
    assert 'form' in response.context


def test_comments_order(comment, news, admin_client):
    author = User.objects.create(username='Комментатор')
    now = datetime.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    url = reverse('news:detail', args=(news.id,))
    response = admin_client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'parametrized_client, form_news_detail',
    (
        (lazy_fixture('author_client'), True),
        (lazy_fixture('client'), False),
    )
)
@pytest.mark.django_db
def detail_for_different_users(
        news, parametrized_client
):
    url = reverse('news:detail', args=(news.id,))
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    assert news in object_list
