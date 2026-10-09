# o3p-bot-telegram

Odoo 19 addon for configuring a Telegram bot token and testing Telegram Bot API access from Odoo.

## Features

- Adds a Telegram Bot app menu with a Settings entry and Test Console.
- Adds a Telegram Bot section to Odoo Settings for the BotFather token.
- Provides a transient test form to fetch recent chats from `getUpdates`.
- Provides a transient test form to send a message with `sendMessage`.

The test console is intended for operational checks and does not create persistent bot chat records.
