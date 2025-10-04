#  Сократитель url-адресов
## Возможности
Веб-приложение для создания коротких ссылок
- Преобразование длинных URL в короткие коды
- Перенаправление по коротким ссылкам
- Просмотр статуса всех созданных ссылок

## Cтек использованных технологий:
```
Python
Flask
SQLite
HTML
bootstrap
```

## Структура проекта
app.py - основное приложение
constants_query.py - SQL запросы
templates/ - HTML шаблоны
database.db - база данных, создается автоматически

## Как запустить проект: 
Клонировать репозиторий и перейти в него в командной строке: 
``` 
git clone https://github.com/IvanPrudey/url_shortener.git 
``` 
``` 
cd url_shortener
```

Cоздать и активировать виртуальное окружение: 
``` 
python -m venv venv 
``` 
``` 
source venv/Scripts/activate 
``` 
``` 
python -m pip install --upgrade pip 
``` 

Установить зависимости из файла requirements.txt: 
``` 
pip install -r requirements.txt 
```
Запустить приложение в bash
```
python app.py
```
Откройте в браузере:
```
http://localhost:5000
```