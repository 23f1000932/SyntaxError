# Database Dump (`dev.db`)

This file contains a snapshot of the current data in your SQLite database.

## Table: `users`

| id | name | email | password_hash | role | city | budget_preference | preferred_sports | created_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Admin Boss | admin@example.com | scrypt:32768:8:1$LMyeyauUXFVEbR89$6d8561b84aeb37df69ba58b717946d8ae1053fe370a8b7ee66f6a91c2f768aecc16649eaf26a8ee3031c759431886a228271fc5124c9507ae680a157caf6bb07 | admin | Mumbai | mid | None | 2026-02-21 04:27:15 |
| 2 | Sports Authority | org1@example.com | scrypt:32768:8:1$lqaTvLYo7OM5p3xr$4951134442abce4bcd99e3579cf54e1a6ddf7e88f13d08e5a92f06a47f4131a7ee70c7e778b39aa0e5ffef7d0b25a783134d0569c2f3447c2d0c9366b5cdfa91 | organizer | Delhi | mid | None | 2026-02-21 04:27:15 |
| 3 | Active Life Org | org2@example.com | scrypt:32768:8:1$ceNIxiQFYJcYUN6H$b49a408707128a8a268e9135f7bbd1f90fe5634b8162c339c153af20092680e7bab5501968dcb922aab5756805f26526d9127aa0b5496f10f6975111a1791f1b | organizer | Bangalore | mid | None | 2026-02-21 04:27:15 |
| 4 | Rahul Sharma | user1@example.com | scrypt:32768:8:1$Ws0P7FMiD2VdvTdl$49b994422a3310d703cac2edf6cdcd520f998a49df05434318395007685c2d1938a5c699071bbddbe91b7f775c04f0325c5b91b7bf8b2f49dcd2903741d5b71b | user | Delhi | mid | ["Football", "Cricket"] | 2026-02-21 04:27:15 |
| 5 | Priya Patel | user2@example.com | scrypt:32768:8:1$SF63J0ukxLRNfC8s$d18ad1ccb98809c90a68d9c268eec3e4cae29a374080201317405ada3d9a9ee99bb7c46fab2b513b8b3213cb585180d9e98e179a2c6da76fee5ea0b926141fc5 | user | Mumbai | cheap | ["Running", "Cycling"] | 2026-02-21 04:27:15 |


## Table: `escalation_tickets`

| id | user_query | session_context | is_resolved | created_at |
| --- | --- | --- | --- | --- |
| 1 | hii | Internal User ID: 2 | 0 | 2026-02-21 04:41:18 |


## Table: `events`

| id | title | sport_category | description | venue_city | venue_address | event_date | capacity | price | price_tier | organizer_id | tags | banner_url | is_active | created_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Delhi Monsoon Marathon | Running | A 10k run through central Delhi. | Delhi | India Gate | 2026-03-03 04:27:15.197675 | 100 | 500.0 | mid | 2 | None | None | 1 | 2026-02-21 04:27:15 |
| 2 | Corporate Football League | Football | 5v5 tournament. | Delhi | Saket Sports Complex | 2026-02-26 04:27:15.197675 | 16 | 2500.0 | premium | 2 | None | None | 1 | 2026-02-21 04:27:15 |
| 3 | Mumbai Midnight Cycling | Cycling | Night ride through South Bombay. | Mumbai | Colaba | 2026-02-23 04:27:15.197675 | 50 | 300.0 | cheap | 3 | None | None | 1 | 2026-02-21 04:27:15 |
| 4 | Pro Tennis Workshop | Tennis | Weekend coaching clinic. | Bangalore | KSLTA Stadium | 2026-03-13 04:27:15.197675 | 20 | 5000.0 | premium | 3 | None | None | 1 | 2026-02-21 04:27:15 |


## Table: `registrations`

| id | user_id | event_id | status | created_at |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | confirmed | 2026-02-21 04:27:15 |
| 2 | 5 | 3 | confirmed | 2026-02-21 04:27:15 |
| 3 | 4 | 2 | confirmed | 2026-02-21 04:27:15 |


## Table: `payments`

| id | registration_id | razorpay_order_id | razorpay_payment_id | razorpay_signature | amount | platform_fee | organizer_payout | status | created_at |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | order_mock1 | pay_mock1 | sig1 | 500.0 | 75.0 | 425.0 | paid | 2026-02-21 04:27:15 |
| 2 | 2 | order_mock2 | pay_mock2 | sig2 | 300.0 | 45.0 | 255.0 | paid | 2026-02-21 04:27:15 |
| 3 | 3 | order_mock3 | pay_mock3 | sig3 | 2500.0 | 375.0 | 2125.0 | paid | 2026-02-21 04:27:15 |


