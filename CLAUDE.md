# CarSale — мониторинг объявлений Volkswagen Cross Polo

Цель: ежедневно собирать объявления с OLX.ua и AUTO.RIA, вести сводку, строить график цен и отправлять письмо CarSaleBot.

## Файлы (точные имена, в корне проекта)
- `cross-polo_olx-ua.md` — снимки OLX.ua (ключ: ID объявления).
- `cross-polo_avto-riа-com.md` — снимки AUTO.RIA (ключ: госномер). Буква «а» в «riа» кириллическая!
- `cross-polo-summary.md` — общая сводка, новые строки сверху, сортировка: дата ↓, затем AUTO.RIA выше OLX.ua.
- `cross-polo-2weeks.png` — график цен за 14 дней.
- `report.json` — результат `update_summary.py` (добавленные строки и их класс).
- `update_summary.py` — слияние в сводку + классификация + график. Запуск: `.venv/bin/python update_summary.py` (в `.venv` стоит matplotlib; создать: `python3.14 -m venv .venv && .venv/bin/pip install matplotlib`).

## Конвейер (скиллы в `.claude/skills/`)
1. `carsale-load-olx`, `carsale-load-autoria` — загрузка страниц поиска в md-файлы.
2. `carsale-update-summary` — `.venv/bin/python update_summary.py`.
3. `carsale-price-chart` — график (делает тот же скрипт, если сводка изменилась).
4. `carsale-email-report` — письмо.

## Правила
- Ключ машины = госномер / ID. Ссылка и пробег в ключ не входят.
- Письмо: кому anatolii.zinhan.pl@gmail.com, тема `CarSaleBot`, HTML. Новая машина — зелёный, изменилась цена — оранжевый.
- Письмо отправляется без вложений (Gmail-коннектор не умеет прикладывать файлы по пути). Отправка: Gmail-коннектор или `.venv/bin/python send_report.py`.
- Не выдумывать данные; пустое поле = «—».
- Секреты — только в `.env` (в git не попадает).

## TODO
- Расписание (launchd). Отправка: `.venv/bin/python send_report.py` (SMTP, нужен пароль приложения Google в `.env`; `--dry-run` — только предпросмотр в `out/`).
