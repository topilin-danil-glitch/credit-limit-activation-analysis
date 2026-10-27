EN:

Analysis of Credit Limit Activation

Business Problem

Customers are granted an approved credit limit but fail to activate it.

The bank incurs costs associated with the approval process without generating any interest income.

Data

A synthetic dataset (300 customers) is provided in /data/clients.csv.

Columns include: issuance channel, activation status, days since approval, and category of the first purchase.

SQL Analysis

The /sql/ directory contains three queries:

1. Activation by issuance channel (findings: branch - 32.6%, mobile app - 64.8%).

2. Time to first purchase (findings: activation rates drop to 18% after 14 days).

3. Impact of the first purchase category (findings: "groceries" is the most active category).

Documentation

Located in /docs/:

- user\_stories.md — 3 User Stories with acceptance criteria.

- FRD\_smart\_limit.md — Functional Requirements Document for the "Smart Limit" feature.

Diagrams

The /diagrams/ directory contains process flows: AS-IS (without reminders) and TO-BE (incorporating personalized push notifications).

Results

/results/executive\_summary.md provides a summary, including the hypothesis, the proposed solution, and the expected impact (a 15 percentage point increase in activation).

Limitations

The data is synthetic and was created solely to demonstrate the business analysis approach.

RU:

Анализ активации кредитного лимита

Бизнес-проблема

Клиенты получают одобренный кредитный лимит, но не активируют его.

Банк несет затраты на одобрение, но не получает процентный доход.

Данные

Синтетический датасет (300 клиентов) в /data/clients.csv.

Колонки: канал выдачи, статус активации, дни с одобрения, категория первой покупки.

SQL-анализ

В /sql/ — три запроса:

1. Активация по каналам выдачи (выявлено: отделение - 32.6%, приложение - 64.8%).

2. Время до первой покупки (выявлено: после 14 дней активация падает до 18%).

3. Влияние категории первой покупки (выявлено: «продукты» - самая активная категория).

Документация

В /docs/:

- user\_stories.md - 3 User Stories с критериями приемки.

- FRD\_smart\_limit.md - функциональные требования к фиче «Умный лимит».

Схемы

В /diagrams/ — процессы AS-IS (без напоминаний) и TO-BE (с персонализированным push).

Результат

В /results/executive\_summary.md — выжимка: гипотеза, предложение, ожидаемый эффект (+15 п.п. к активации).

Ограничения

Данные синтетические, созданы для демонстрации подхода бизнес-анализа.
