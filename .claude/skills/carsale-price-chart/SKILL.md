---
name: carsale-price-chart
description: Build one price-over-time chart (last 14 days) for every Cross Polo car from cross-polo-summary.md and save it as cross-polo-2weeks.png. Only when the summary changed.
---

# CarSale: график цен за 2 недели

Выполнять только если `carsale-update-summary` добавил хотя бы одну строку (`report.json` → `chart: true`). Реализация — внутри `update_summary.py` (matplotlib).

## Требования к графику
- Один общий график, одна линия на машину (ключ = Госномер/ID), данные за последние 14 дней по всей сводке.
- X — дата (дд.мм), Y — цена в $, подписи точек со значением цены.
- Легенда: «Город, год, источник». Маркеры на точках; если у машины одна точка — только маркер.
- Размер ~1400×800, светлый фон, читаемые шрифты.
- Сохранить как `cross-polo-2weeks.png` (перезаписать). Строить скриптом, чтобы результат был воспроизводим.

Дополнительно: скилл `autoria-price-history` (Claude Desktop) умеет строить интерактивный HTML-график по таблице AUTO.RIA и помечает проблемы данных (л.с. = объём × 100, меняющийся пробег).
