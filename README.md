## Измерительно-вычислительная система для оценки вертикального профиля двуокиси азота в атмосфере
`plan_no2_v1.pdf` - [План по NO_2](plan_no2_v1.pdf)
##### scripts:
* `src/prepare_profile.py` - [Получение данных реального профиля из изображений](src/prepare_profile.py)
* `src/msbgraph_to_csv.py` - [Получение датасетов послойных воздушных масс из msbgraph.txt программы МПИ](src/msbgraph_to_csv.py)
* `src/direct_measurements.py` - [Прямые измерения(наклонное содержание)](src/direct_measurements.py)
* `src/profile_recovery.py` - [Восстановление методом ЛП](src/profile_recovery.py) (планируется запустить туда, отнаследовавшись от `src/bayesian.py`, для сохранения логики структуры)
* `src/bayesian.py` - [Восстановление методом ОСЦ](src/bayesian.py)
* `src/create_dataset_3.py` - [Создание датасета с учётом приземного слоя](src/create_dataset_3.py)
* `src/draw_profiles.py` - [Построение графики](src/draw_profiles.py)
* `src/drawing/draw_ose.py` - [Класс для восстановления методом ОСЦ](src/drawing/draw_ose.py) (наследуется в `src/drawing/draw_ose.py`)
* `src/drawing/draw_linear_prog.py` - [Класс для восстановления методом ЛП](src/drawing/draw_linear_prog.py) (наследуется в `src/drawing/draw_ose.py`)
* `src/drawing/common_drawing_methods.py` - [Общие настройки графиков](src/drawing/common_drawing_methods.py) (наследуется в `draw_ose.py` и `draw_linear_prog.py`)
##### Результаты восстановления:
* [Восстановление 4-х модельных](output_4)
I четверть - ЛП 2 максимума
II четверть - ЛП 1 максимума
III четверть - ОСО 50м. радиус корреляции
IV четверть - ОСО 200м. радиус корреляции
##### Установка зависимостей
```pip install -r requirements.txt```
##### Codestyle
```black .``` ('pyproject.toml' конфигурирует максимальную длину строк)