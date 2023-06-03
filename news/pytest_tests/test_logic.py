from pytest_django.asserts import assertRedirects

from django.urls import reverse

from news.models import News, Comment


# Указываем фикстуру form_data в параметрах теста.
def test_user_can_create_comment(author_client, author, form_data, news, comment):
    url = reverse('news:detail', args=(news.id,))
    # В POST-запросе отправляем данные, полученные из фикстуры form_data:
    response = author_client.post(url, data=form_data)
    # Проверяем, что был выполнен редирект на страницу успешного добавления заметки:
    assertRedirects(response, reverse('news:detail', args=(news.id,)))
    # Считаем общее количество заметок в БД, ожидаем 1 заметку.
    assert Comment.objects.count() == 1
    # Чтобы проверить значения полей заметки -
    # получаем её из базы при помощи метода get():
    new_comment = Comment.objects.get()
    # Сверяем атрибуты объекта с ожидаемыми.
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
