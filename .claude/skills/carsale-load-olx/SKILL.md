---
name: carsale-load-olx
description: Open the saved OLX.ua search for Volkswagen Cross Polo (2006–2009, automatic, 1–2 l), read the listings from the page and append a snapshot to cross-polo_olx-ua.md in the project folder.
---

# CarSale: загрузка OLX.ua


URL поиска: https://www.olx.ua/uk/transport/legkovye-avtomobili/volkswagen/?currency=UAH&search%5Bfilter_enum_model%5D%5B0%5D=polo&search%5Bfilter_enum_transmission_type%5D%5B0%5D=546&search%5Bfilter_float_motor_engine_size_litre%3Afrom%5D=1&search%5Bfilter_float_motor_engine_size_litre%3Ato%5D=2&search%5Bfilter_float_motor_year%3Afrom%5D=2006&search%5Bfilter_float_motor_year%3Ato%5D=2009
Фильтры (из заголовка файла): Volkswagen Cross Polo, 2006–2009, автомат, объём 1–2 л.

## Шаги
1. Открыть URL в браузере (Claude in Chrome / встроенный браузер), дождаться загрузки списка, при необходимости пролистать/пройти пагинацию.
2. Для каждого объявления собрать: модель, год, ID объявления (из ссылки, напр. `ID11cNUF`), л.с. (если нет — «—»), объём двигателя, пробег, цена в $, город, ссылка.
3. Добавить снимок в **начало** таблицы файла `~/ClaudeProjects/CarSale/cross-polo_olx-ua.md` (файл не пересоздавать, старые строки не менять). Дата и время — текущие UTC, формат `YYYY-MM-DD HH:MM`.
   Колонки: `| Дата и время (UTC) | Модель | Год | Госномер / ID | Л.с. | Объем двигателя | Пробег | Цена, $ | Город | Ссылка |`
4. Пропустить объявления, которых уже есть с той же датой и ID. Не выдумывать данные: если поле не видно на странице — «—».
5. Отчёт: сколько объявлений найдено, сколько добавлено.
