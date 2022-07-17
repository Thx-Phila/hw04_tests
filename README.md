## Небольшой проект с блогом, покрытый тестами. Файл posts/tests.py

#### Тестами проверяется:
* После регистрации пользователя создается его персональная страница (profile)
* Авторизованный пользователь может опубликовать пост (new)
* Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
* После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице пользователя (profile), и на отдельной странице поста (post)
* Авторизованный пользователь может отредактировать свой пост и его содержимое изменится на всех связанных страницах
