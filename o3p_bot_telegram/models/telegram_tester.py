import json

import requests

from odoo import fields, models
from odoo.exceptions import UserError


class O3PBotTelegramTester(models.TransientModel):
    _name = "o3p.bot.telegram.tester"
    _description = "Telegram Bot Test Console"

    chat_id = fields.Char(string="Chat ID")
    message_text = fields.Text(string="Message")
    recent_chat_result = fields.Text(string="Recent Chats", readonly=True)
    send_result = fields.Text(string="Send Result", readonly=True)

    def action_get_recent_chats(self):
        self.ensure_one()
        payload = self._telegram_api("getUpdates")
        chats = self._extract_chats(payload)
        self.recent_chat_result = (
            "\n".join(chats)
            if chats
            else "No recent chats found. Send a message to the bot first, then try again."
        )
        return self._reload_action()

    def action_send_message(self):
        self.ensure_one()
        if not self.chat_id:
            raise UserError("Enter a Telegram chat ID.")
        if not self.message_text:
            raise UserError("Enter a message to send.")
        payload = self._telegram_api(
            "sendMessage",
            data={"chat_id": self.chat_id, "text": self.message_text},
            method="post",
        )
        message = payload.get("result", {})
        self.send_result = json.dumps(
            {
                "ok": payload.get("ok"),
                "message_id": message.get("message_id"),
                "chat_id": message.get("chat", {}).get("id"),
                "date": message.get("date"),
            },
            indent=2,
            sort_keys=True,
        )
        return self._reload_action()

    def _telegram_api(self, method_name, data=None, method="get"):
        token = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_str("o3p_bot_telegram.bot_token")
        )
        if not token:
            raise UserError("Configure the Telegram bot token in Settings first.")

        url = f"https://api.telegram.org/bot{token}/{method_name}"
        try:
            if method == "post":
                response = requests.post(url, data=data, timeout=20)
            else:
                response = requests.get(url, params=data, timeout=20)
            response.raise_for_status()
            payload = response.json()
        except requests.RequestException as error:
            raise UserError(f"Telegram API request failed: {error}") from error
        except ValueError as error:
            raise UserError("Telegram API returned a non-JSON response.") from error

        if not payload.get("ok"):
            description = payload.get("description") or "Unknown Telegram API error."
            raise UserError(description)
        return payload

    def _extract_chats(self, payload):
        chats = {}
        for update in payload.get("result", []):
            message = self._message_from_update(update)
            chat = message.get("chat") if message else None
            if not chat or chat.get("id") is None:
                continue
            chat_id = str(chat["id"])
            username = chat.get("username")
            title = chat.get("title")
            first_name = chat.get("first_name")
            last_name = chat.get("last_name")
            display = title or " ".join(part for part in [first_name, last_name] if part)
            handle = f"@{username}" if username else display or chat.get("type") or ""
            chats[chat_id] = f"{chat_id} {handle}".strip()
        return sorted(chats.values())

    def _message_from_update(self, update):
        for key in (
            "message",
            "edited_message",
            "channel_post",
            "edited_channel_post",
            "my_chat_member",
            "chat_member",
        ):
            value = update.get(key)
            if value:
                return value
        return {}

    def _reload_action(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Telegram Bot Test",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }
