# Anti-Leecher-for-Nicotine-ProveIt

A Nicotine+ plugin that bans and ignores users who think file sharing is optional. Spoiler: it’s not.  

This fork adds "ProveIT", which is meant to curb automated downloads from leechers who fake file shares, etc (often times vibe coded streaming clients).

---

## What is this?  

A **personal plugin** for [Nicotine+](https://github.com/Nicotine-Plus/nicotine-plus).  
It does exactly what it says:

- Users who don't share enough files and folders? Banned and ignored.  
- If the user's IP has resolved, they can be banned. If it's unresolved, they won't be IP banned.  
- Optionally, send them a message telling them to stop leeching — or not.
- Block Suspicious Users with certain File Share numbers
- Unban users who are now sharing - In Testing  

---

## ProveIt Addon

ProveIt is a lightweight “captcha” layer for **uploads**. It is aimed at **bots** and **headless / streaming-style clients** that queue many files but are not able to interact in chat, while still letting real users through aftee verification.

### What it does

- **Non-buddies** who are not on your **ProveIt verified whitelist** get their queued upload **removed** when they try to download from you.
- They receive a **private message** you can edit (eg: ask them to type a word such as `download` in PM to be whitelisted).
- When they send that **exact word** (case-insensitive), they are **added to the whitelist** and get a **second editable message**.
- By default, ProveIt will try to **auto-retry previously denied queued uploads** right after successful verification.
- If auto-retry does not restart every download (client/network timing can vary), users should still **retry manually**.
- **Buddies** are **not** asked to prove anything.
- A **cooldown** (default: several minutes) limits how often the “first download” reminder is sent to the same user, so rapid retries do not spam their PM.

### Options (plugin settings)

- Turn ProveIt on or off.
- Edit the **first PM** and **success PM**, the **captcha word**, **cooldown seconds**, and view or manage the **verified users** list.
- Toggle **auto-retry uploads after verification** (enabled by default).
- **Hide messages from plugin** (hides PM tabs/messages triggered by the plugin and hides exact captcha replies, while still allowing normal chat messages).

---

## Why?  

Because this is **Soulseek, not Soul-take**.  
If you're here just to download and not contribute, go use Spotify or rip YouTube.  

ProveIt: Soulseekers on [r/Soulseek](https://www.reddit.com/r/Soulseek/) have been looking for ways to curb **“leech-slop”**, which are low-effort, often automated accounts that leech without behaving like real participants (see [vibecoded slop accounts](https://www.reddit.com/r/Soulseek/comments/1s1yh55/vibecoded_slop_accounts/) and [vibe coded leech slop is rising](https://www.reddit.com/r/Soulseek/comments/1rzsds8/vibe_coded_leech_slop_is_rising_how_do_we_stop_it/)). This plugin (especially with ProveIt) is made to remedy this, while still allowing real users to use Soulseek.

---

## Installation  

1. Drop the plugin into your Nicotine+ `plugins` folder.  
2. Go to **Plugins → Enable** it.  
3. Configure it: set minimum files/folders shared, and the optional warning message.  
4. Done.  

<img width="597" height="735" alt="image" src="https://github.com/user-attachments/assets/0de0a5d3-5f1a-405a-b004-b9abbb2fb3ee" />

---

## FAQ  

**Q: Isn’t this gatekeeping?**  
**A:** It’s designed to encourage sharing in the community. Many users do share generously, and this plugin helps prioritize those connections.

**Q: But I only share 1 file because I’m shy… or have no bandwidth, storage etc...**  
**A:** Understood. But this plugin prioritizes people who share. If not, the people who share get punished. 

**Q: Do downloaders need to install this plugin?**  
**A:** No. It only needs to run on your side (Nicotine) People downloading from you do not need the plugin for it to apply to your shares / for them to respond to the captcha.

**ProveIt: Q: What if these tools catch on?**  
**A:** If lots of people run the same fixed captcha word, scripted clients could eventually automate answering it. A **randomized captcha** (different challenge per user or per session) would help. I’m looking into how to do that sensibly in Nicotine+ but don’t really have a solid dapproach yet. **Contributions are welcome**, if you have a clean way to do this, feel free to add it.

**ProveIt: Q: Can I hide or mute messages from this plugin?**  
**A:** Yes. **Hide messages from plugin** is now enabled by default, it hides plugin-triggered messages  while keeping normal chat messages visible.

---

## License  

GPLv3. Do whatever you want.
