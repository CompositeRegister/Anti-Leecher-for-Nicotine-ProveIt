# This software is provided "as-is", without any express or implied warranty.
# You can use it, modify it, and distribute it freely for any purpose.


from pynicotine.pluginsystem import BasePlugin

class Plugin(BasePlugin):

    PLACEHOLDERS = {
        "%files%": "num_files",
        "%folders%": "num_folders",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = {
            "message": "Please consider not being a leecher. Thanks",
            "open_private_chat": False,
            "num_files": 1010,
            "num_folders": 51,
            "send_message_to_leechers": False,
            "ban_leechers": True,
            "ignore_leechers": True,
            "ban_block_ip": False,
            "enable_sus_detector": True,
            "sus_pattern_500_25": False,
            "sus_pattern_1000_50": True,
            "sus_pattern_1500_75": False,
            "sus_pattern_2000_100": False,
            "auto_unban": True,           # GUI toggle for auto unban/unignore
            "detected_leechers": []
        }

        self.metasettings = {
            "message": {
                "description": ("Private chat message to send to leechers."),
                "type": "textview"
            },
            "open_private_chat": {
                "description": "Open chat tabs when sending private messages",
                "type": "bool"
            },
            "num_files": {"description": "Minimum shared files", "type": "int", "minimum": 0},
            "num_folders": {"description": "Minimum shared folders", "type": "int", "minimum": 1},
            "send_message_to_leechers": {"description": "Send PM to leechers", "type": "bool"},
            "ban_leechers": {"description": "Ban leechers", "type": "bool"},
            "ignore_leechers": {"description": "Ignore leechers", "type": "bool"},
            "enable_sus_detector": {"description": "Detect suspicious sharing patterns", "type": "bool"},
            "sus_pattern_500_25": {"description": "500 files / 25 folders", "type": "bool"},
            "sus_pattern_1000_50": {"description": "1000 files / 50 folders", "type": "bool"},
            "sus_pattern_1500_75": {"description": "1500 files / 75 folders", "type": "bool"},
            "sus_pattern_2000_100": {"description": "2000 files / 100 folders", "type": "bool"},
            "ban_block_ip": {"description": "Block leecher IP (if known)", "type": "bool"},
            "auto_unban": {
                "description": "Automatically unban/unignore users when they start sharing enough",
                "type": "bool",
                "default": True
            }
        }

        self.probed_users = {}

    def loaded_notification(self):
        # Enforce minimum requirements
        self.settings["num_files"] = max(
            self.settings["num_files"],
            self.metasettings["num_files"]["minimum"]
        )
        self.settings["num_folders"] = max(
            self.settings["num_folders"],
            self.metasettings["num_folders"]["minimum"]
        )

        # Load suspicious patterns
        self.settings["sus_patterns"] = []
        if self.settings["sus_pattern_1000_50"]:
            self.settings["sus_patterns"].append((1000, 50))
        if self.settings["sus_pattern_2000_100"]:
            self.settings["sus_patterns"].append((2000, 100))
        if self.settings["sus_pattern_1500_75"]:
            self.settings["sus_patterns"].append((1500, 75))
        if self.settings["sus_pattern_500_25"]:
            self.settings["sus_patterns"].append((500, 25))

        self.log("Suspicious patterns loaded: %s", self.settings["sus_patterns"])

    def send_pm(self, user):
        if not self.settings.get("send_message_to_leechers") or not self.settings.get("message"):
            return

        for line in self.settings["message"].splitlines():
            for placeholder, option_key in self.PLACEHOLDERS.items():
                line = line.replace(placeholder, str(self.settings.get(option_key, 0)))

            try:
                self.send_private(
                    user,
                    line,
                    show_ui=self.settings.get("open_private_chat", False),
                    switch_page=False
                )
            except Exception as e:
                self.log("Failed to send PM to %s: %s", (user, e))

    def block_ip(self, user):
        stats = getattr(self.core.users, "watched", {}).get(user)
        if stats and getattr(stats, "ip_address", None):
            ip = stats.ip_address
            ip_list = getattr(self.core.config.sections.get("server", {}), "ipblocklist", {})
            ip_list[ip] = user
            self.log("Blocked IP: %s", ip)
        else:
            self.log("IP block failed: No IP for %s", user)

    def unban_and_unignore_if_okay(self, user, num_files, num_folders):
        """
        Automatically unban/unignore users if they meet the sharing requirements.
        Controlled by the 'auto_unban' GUI setting.
        """
        if not self.settings.get("auto_unban", True):
            return

        is_okay = (
            num_files >= self.settings["num_files"]
            and num_folders >= self.settings["num_folders"]
        )

        if not is_okay and user not in self.core.buddies.users:
            return

        if self.core.network_filter.is_user_banned(user):
            self.core.network_filter.unban_user(user)
            self.log("User '%s' was banned but now meets requirements. Unbanned.", user)

        if self.core.network_filter.is_user_ignored(user):
            self.core.network_filter.unignore_user(user)
            self.log("User '%s' was ignored but now meets requirements. Unignored.", user)

    def check_user(self, user, num_files, num_folders):
        num_files = num_files or 0
        num_folders = num_folders or 0

        if user not in self.probed_users:
            return

        if self.probed_users[user] == "okay":
            return

        # Suspicious pattern detector
        if self.settings.get("enable_sus_detector"):
            for pf, pd in self.settings["sus_patterns"]:
                if num_files == pf and num_folders == pd:
                    actions = []
                    if self.settings["ban_leechers"]:
                        self.core.network_filter.ban_user(user)
                        actions.append("banned")
                    if self.settings["ignore_leechers"]:
                        self.core.network_filter.ignore_user(user)
                        actions.append("ignored")
                    if self.settings["ban_block_ip"]:
                        self.block_ip(user)
                        actions.append("IP blocked")
                    if self.settings["send_message_to_leechers"]:
                        self.send_pm(user)
                        actions.append("messaged")

                    self.probed_users[user] = "processed_leecher"
                    self.settings["detected_leechers"].append(user)

                    self.log(
                        "Suspicious user %s: %d files, %d folders. %s",
                        (user, pf, pd, ", ".join(actions))
                    )
                    return

        # Normal share check
        is_okay = (
            num_files >= self.settings["num_files"]
            and num_folders >= self.settings["num_folders"]
        )

        if is_okay or user in self.core.buddies.users:

            if user in self.settings["detected_leechers"]:
                self.settings["detected_leechers"].remove(user)

            self.probed_users[user] = "okay"

            self.log("User %s meets requirements (%d files, %d folders).",
                     (user, num_files, num_folders))

            # Auto unban/unignore if enabled
            self.unban_and_unignore_if_okay(user, num_files, num_folders)
            return

        # Not OK → check next state
        if not self.probed_users[user].startswith("requesting"):
            return

        if user in self.settings["detected_leechers"]:
            self.probed_users[user] = "processed_leecher"
            return

        if (num_files <= 0 or num_folders <= 0) and self.probed_users[user] != "requesting_shares":
            self.log("User %s shows 0 shares; requesting full share list…", user)
            self.probed_users[user] = "requesting_shares"
            self.core.userbrowse.request_user_shares(user)
            return

        actions = []

        if self.settings["ban_leechers"]:
            self.core.network_filter.ban_user(user)
            actions.append("banned")

        if self.settings["ignore_leechers"]:
            self.core.network_filter.ignore_user(user)
            actions.append("ignored")

        if self.settings["ban_block_ip"]:
            self.block_ip(user)
            actions.append("IP blocked")

        if self.settings["send_message_to_leechers"]:
            self.send_pm(user)
            actions.append("messaged")

        self.probed_users[user] = "pending_leecher"
        self.settings["detected_leechers"].append(user)

        self.log(
            "Leecher detected: %s — %d files / %d folders. %s.",
            (user, num_files, num_folders, ", ".join(actions))
        )

    def upload_queued_notification(self, user, virtual_path, real_path):
        if user in self.probed_users:
            return

        self.probed_users[user] = "requesting_stats"
        stats = self.core.users.watched.get(user)

        if stats:
            self.check_user(user,
                            num_files=getattr(stats, "files", 0),
                            num_folders=getattr(stats, "folders", 0))

    def user_stats_notification(self, user, stats):
        self.check_user(
            user,
            num_files=stats.get("files", 0),
            num_folders=stats.get("dirs", 0)
        )

    def upload_finished_notification(self, user, *_):
        if user not in self.probed_users:
            return
        if self.probed_users[user] != "pending_leecher":
            return
        self.probed_users[user] = "processed_leecher"
