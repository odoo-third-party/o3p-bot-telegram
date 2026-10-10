{
    "name": "o3p - bot telegram",
    "summary": "Telegram bot settings and test tools for Odoo.",
    "description": (
        "O3P Bot Telegram adds Telegram bot configuration and a transient test console "
        "for reading recent chats and sending test messages through the Telegram Bot API."
    ),
    "version": "20.0.1.0.0",
    "category": "Productivity/Discuss",
    "author": "O3P",
    "website": "https://github.com/odoo-third-party/o3p-bot-telegram",
    "license": "LGPL-3",
    "sequence": 21,
    "depends": ["base_setup", "mail"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "data/discuss_channel_data.xml",
        "security/ir.access.csv",
        "views/res_config_settings_views.xml",
        "views/telegram_tester_views.xml",
        "views/menu_views.xml",
    ],
    "images": [
        "thumb.png",
        "static/description/thumbnail.svg",
        "static/description/banner.svg",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
