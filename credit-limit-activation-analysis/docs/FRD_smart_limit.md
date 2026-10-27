ENG:



FRD: "Smart Limit" feature



1\. Objective

Increase the credit limit activation rate from 50% to 65% through personalized communications.



2\. The Problem

Customers who receive approval at a branch activate their credit limit half as often as those who do so via the app.

The primary reasons are the lack of a digital reminder and a failure to clearly understand the benefits.



3\. Solution

The "Smart Limit" feature: the system analyzes a client's transaction history and sends a personalized push notification suggesting a category where a limit would be most beneficial.



4\. Functional requirements

| ID   | Requirement                                                                                   | Приоритет |

|------|-----------------------------------------------------------------------------------------------|-----------|

| FR-1 | The system analyzes the client's transaction history for the last 3 months.                   | Must      |

| FR-2 | The system identifies the customer's top spending category.                                   | Must      |

| FR-3 | 24 hours after approval, a push notification is sent with a cashback offer for this category. | Must      |

| FR-4 | If there is no activation after 7 days, a second reminder is sent with a different offer.     | Should    |

| FR-5 | The client can disable notifications in the app settings.                                     | Must      |



5\. Non-functional requirements

The notification must be sent no later than 24 hours after approval.

The system must not send notifications to clients who have disabled push notifications.



6\. Success metrics

Activation rate (target: +15 percentage points)

Conversion from push notification to activation (target: 20%)

Churn rate among customers who have been granted a credit limit (target: 10% reduction)





RU:



FRD: Фича «Умный лимит»



1\. Цель

Повысить долю активаций кредитного лимита с 50% до 65% за счет персонализированных коммуникаций.



2\. Проблема

Клиенты, получившие одобрение в отделении, активируют лимит в 2 раза реже, чем в приложении.

Основная причина — отсутствие цифрового напоминания и непонятная выгода.



3\. Решение

Фича «Умный лимит» — система анализирует историю транзакций клиента и отправляет

персонализированное push-уведомление с категорией, где лимит будет наиболее выгоден.



4\. Функциональные требования

| ID   | Требование                                                                              | Приоритет |

|------|-----------------------------------------------------------------------------------------|-----------|

| FR-1 | Система анализирует историю транзакций клиента за последние 3 месяца                    | Must      |

| FR-2 | Система определяет топ-1 категорию трат клиента                                         | Must      |

| FR-3 | Через 24 часа после одобрения отправляется push с предложением кэшбэка в этой категории | Must      |

| FR-4 | Если активации нет через 7 дней, отправляется второе напоминание с другим предложением  | Should    |

| FR-5 | Клиент может отключить уведомления в настройках приложения                              | Must      |



5\. Нефункциональные требования

\- Уведомление должно отправляться не позднее 24 часов после одобрения.

\- Система не должна отправлять уведомления клиентам, отключившим push-уведомления.



6\. Метрики успеха

\- Доля активаций (цель: +15 п.п.)

\- Конверсия из push в активацию (цель: 20%)

\- Отток клиентов, получивших лимит (цель: снизить на 10%)

