# test_task_progress
Тестовое задание
API для работы с достижениями

Задача: реализовать на python3 простой сервер (с помощью fastapi или flask) для общения с базой данных.

Инструменты реализации: python3, flask, MySQL

## База данных должна иметь таблицы:
  1.   таблица пользователей;
необходимые поля:
    •  имя пользователя, 
    •  выбранный пользователем язык (ru/en).
  2.   таблица достижений;
необходимые поля:
    • имя достижения;
    • количество баллов (очков достижений) за достижение (целое положительное число)
    • текстов описание сути достижения.

## Сервер должен выполнять следующие функции:
    • предоставлять информацию о пользователе;
    • предоставлять информацию о всех доступных достижениях;
    • добавлять достижения;
    • выдавать достижения пользователю с сохранением времени выдачи (сохранять связь пользователя с достижением и датой выдачи);
    • предоставлять информацию о выданных пользователю достижениях на выбранном пользователем языке;
    • предоставлять статистические данные системы:
    ◦ пользователь с максимальным количеством достижений (штук);
    ◦ пользователь с максимальным количеством очков достижений (баллов суммарно);
    ◦ пользователи с максимальной разностью очков достижений (разность баллов между пользователями);
    ◦ пользователи с минимальной разностью очков достижений(разность баллов между пользователями);
    ◦ пользователи, которые получали достижения 7 дней подряд (по дате выдачи, хотя бы одно в каждый из 7 дней).Опциональные задачи:
    • составить docker compose файл для развертывания сервера и всех его компонентов(к примеру, СУБД);
    • одним из компонентов развертывания должен быть сервер nginx, через который организует reverse proxy доступ к серверу;
    • показать навыки оформления проекта (комментарии к функциям, логирование, написание read.me);
    • показать умение работать с историей git;
    • проявить фантазию в именовании достижений и их описании;
    • показать умение тестировать разработанный код.
