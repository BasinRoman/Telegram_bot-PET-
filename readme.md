Бот создан для системы оповещения о падении серверов с помощью библиотеки Aiogram.
Для взаимодействия между службой Сервис-Деск и пользователями. Для получения актуальной информации о дежурстве сотрудников Сервис Деска. Для просмотра веб камер необходимых мест в офисе с мобильного телефона(телеграм + web app(html+css)). Данные хранятся в БД, исползуется библиотека SQLite. Модуль с камерами развернут на веб сервере на Flask(см.репозиторий Bot_cameras) Запуск с помощью bot_run.bat.

Вам потребуется изменить пути для pikperson.dat и pikserver.dat, а так же для bot_bd.db и dej_graph.xlsx. т.к. в моем случае я использовал докер и отдельные volumes для этих данных.
-example варианты я разместил в корне проекта. 



Этой мой первый проект на Python, многое в нем написано абсолютно некорректно, пытаюсь исправлять по ходу получения новых знаний и опыта. Благодарю за любую обратную свзяь и помощь в исправлении косяков и багов.
