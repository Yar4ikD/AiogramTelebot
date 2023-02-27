# Yandex Timetable aiogram telegram bot

Телеграм бот на Python, для предоставления информации пользователю о маршрутах и времени движения транспортных средств:
1. Самолётов
2. Поездов
3. Электричек
4. Автобусов

Бот работает с [API Яндекс Расписания.](https://yandex.ru/dev/rasp/)

## Начало работы
### Основные шаги для запуска работы бота:
1. Получить **\<token\>** бота
2. Получить и активировать ключ API Яндекс Расписания (используется в каждом запросе к API)
3. Установить зависимости с файла [requirements. txt](python_basic_diploma/requirements.txt)
```
venv\Scripts\activate.bat - для Windows;
source venv/bin/activate - для Linux и MacOS.
```
```
pip install -r requirements.txt
```
4. В корне проекта создать файл **.env** и добавить:
```
TOKEN=
YANDEX_API_KEY=
```

## Структура проекта бота 
- main.py (Файл, который содержит объект бота)
- loader.py (Инициализация бота)
- config.py (Файл с настройками)
- requirements.txt (Библиотеки)
- api/ (Пакет - работа с API)
- commands/ (Пакет - обработка команд пользователя)
- database/ (Пакет - работа с БД)
- keyboard/ (Пакет - клавиатура и кнопки)

## Команды бота

### Команда - Старт
Запуск бота, вывод пользователю приветствия и информацию о взаимодействии и командах бота.
- [/start, start, старт]()

<img src="images/start-work.jpg" width="500">

#### Модули отвечающие за работу команды:

```
commands/
    base_command.py
```

```python
async def information_bot(message: types.Message) -> None
```

### Команда - help
Выводит список команд бота. 
- [/help]()

<img src="images/command-help.jpg" width="500">

#### Модули отвечающие за работу команды:

```
commands/
    base_command.py
```

```python
async def base_list_command(message: types.Message) -> None
```

### Команда - history
Выводи историю запросов пользователя
- [/history]()

<img src="images/command-history.jpg" width="500">

#### Модули отвечающие за работу команды:

```
commands/
    response_history.py
    
database/
    user_request_history/
                work_with_db.py
                
keyboard/
    response_history.py
```

### Команда - Расписание рейсов между городами
Запрос позволяет получить список рейсов транспорта, следующих от указанного города отправления к указанному городу прибытия 
и информацию по каждому рейсу.

<img src="images/com-fl-bet-c-01.jpg" width="500">
<img src="images/com-fl-bet-c-02.jpg" width="500">
<img src="images/com-fl-bet-c-03.jpg" width="500">
<img src="images/com-fl-bet-c-04.jpg" width="500">

#### Модули отвечающие за работу команды:

```
commands/
    schedule_flights_between_cities.py
    
api/
    get_schedule_flights_between_cities.py
    
database/
    select_data_for_command/
                for_schedule_flights_between_cities.py
        
keyboard/
    schedule_between_cities_buttons.py
```

### Команда - Расписание рейсов по станции
Запрос позволяет получить список рейсов, отправляющихся от указанной станции и информацию по каждому рейсу.

<img src="images/com-sch-stat-01.jpg" width="500">
<img src="images/com-sch-stat-03.jpg" width="500">
<img src="images/com-sch-stat-02.jpg" width="500">

#### Модули отвечающие за работу команды:

```
commands/
    station_timetable.py
    
api/
    get_schedule_station.py
    
database/
    select_data_for_command/
                station_timetable.py
        
keyboard/
    station_timetable_buttons.py
```

### Команда - Список ближайших станций
Запрос позволяет получить список станций, находящихся в указанном радиусе от указанной точки.  
Максимальное количество возвращаемых станций — 30.  
Точка определяется географическими координатами (широтой и долготой)

<img src="images/com-ls-stat-01.jpg" width="500">
<img src="images/com-ls-stat-02.jpg" width="500">
<img src="images/com-ls-stat-03.jpg" width="500">

#### Модули отвечающие за работу команды:

```
commands/
    list_nearest_stations.py
    
api/
    get_list_nearest_stations.py
        
keyboard/
    list_nearest_buttons.py
```

### Команда - Список станций в населенном пункте
Выводит список станций в населенном пункте.  
Используется в команде - ***Расписание рейсов по станции***.  
Максимальное количество возвращаемых станций — 30.

<img src="images/com-sch-stat-02.jpg" width="500">

```
commands/
    station_timetable.py
```
```python
response = await Select.list_station(settlement_code=c_code, transport=tr_code)
```
```
database/
    select_data_for_command/
                station_timetable.py 
```
```python
async def list_station(cls, settlement_code: str, transport: str) -> Optional[str]
```








