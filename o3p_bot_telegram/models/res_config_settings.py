from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    telegram_bot_token = fields.Char(
        string="Telegram Bot Token",
        config_parameter="o3p_bot_telegram.bot_token",
        groups="base.group_system",
    )
