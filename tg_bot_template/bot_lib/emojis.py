from dataclasses import dataclass


@dataclass
class Emojis:
    dangerous: str = "⚠️"
    on_off: tuple[str, str] = ("🔴️", "🟢")
    on: str = "🟢"
    off: str = "🔴️"
    none: str = "🚫"
    reload: str = "🔄"
    done: str = "✅"
    deny: str = "⛔️"
    pair: str = "👥"
    notes: str = "📝"
    gift: str = "🎁"
