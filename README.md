[:u5272:Русский перевод](#Русский)

CRM3
-

Customer relationship management system based on the Django platform. Open source.

- out of the box empty crm with the ability to add new plugins from the repository, a system of users and roles
- the system is developed only for a modular system from applications that are installed from their repository and interact with each other
- the whole crm infrastructure is designed only for a modular system and the ability of each plugin to have data associated with any other plugin. which simplifies the development and the ability to create your own solutions or integrate ready-made from the repository

Features
-

- multilingual
- version control
- order plugin

Requirements
-
django
python -m pip install djangorestframework
mysqlclient

Documentation
-
read [documentation.md](documentation.md)



## Русский перевод
CRM3
-

Система управления взаимоотношениями с клиентами основанная на платформе Django. Открытый исходный код.

- из коробки пустая crm c возможностью добавлять новые плагины из репозитория , система пользователей и ролей
- система разрабатывается только под модульную систему из приложений, которые устанавливаются их репозитория и взаимодействуют между собой
- вся инфраструктруа crm рассчитана только на модульную систему и возможность каждого плагина иметь связанные данные с любым другим плагином. что упрощает разработку и возможность создание своих решений или интеграция готовых из репозитория

Создание плагина
-

Плагин это обычное startapp с файлом конфигурации
читать documentation.md


Документация
-
читать [documentation.md](documentation.md)

crm paper:

- единая база данных, подгрузка конкретных версий приложений и роли пользователей
- плагин создания печатных данных
- mixin для взаимодействия приложений utils.py [DONE]
- написан плагин создания заказов [DONE] 
- написан плагин бухгалтерия [DONE]
- написан плагин клиенты [DONE]
- создан репозиторий [DONE]