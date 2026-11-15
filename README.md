# Host-Ad-Block

OS-level ad-blocking and anti-tracking `hosts` file collection for **Windows**, **macOS**, **Linux**, **Android**, **iOS**, and network-wide DNS blockers (**AdGuard Home**, **Pi-hole**).

---

## Overview

- **Repository:** [`LamPPKK/Host-Ad-Block`](https://github.com/LamPPKK/Host-Ad-Block)
- **Blocklist File:** [`Block Ad.txt`](Block%20Ad.txt)
- **Direct Raw URL:**
  ```text
  https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt
  ```
- **List Size:** **162,594 block entries** (162,579 unique domains, ~5.16 MB).
- **Coverage:** Display ads (banners, pop-ups), trackers, telemetry, analytics (Google Analytics, DoubleClick, Facebook Ads, Coc Coc ads, and third-party ad networks).
- **How It Works:** Redirects (sinkholes) ad and tracker domains to `127.0.0.1` directly at the operating system's `hosts` layer. It works system-wide across all browsers and apps with zero background processes, RAM, or CPU overhead.

### Default `hosts` File Locations by OS

| Operating System | `hosts` File Path | Required Privilege |
| :--- | :--- | :--- |
| **Windows (10 / 11)** | `C:\Windows\System32\drivers\etc\hosts` | Administrator |
| **macOS** | `/etc/hosts` | `sudo` (root) |
| **Linux** | `/etc/hosts` | `sudo` (root) |
| **Android (Root / Magisk)** | `/data/adb/modules/hosts/system/etc/hosts` or `/system/etc/hosts` | `su` (root) |
| **Android (Non-Root)** | Applied via Local VPN/DNS (AdAway, RethinkDNS, DNS66, etc.) | No Root required |
| **iOS / iPadOS** | DNS/VPN apps (AdGuard, Shadowrocket, etc.) or `/etc/hosts` (Jailbreak) | Per app / Jailbreak |

> [!NOTE]
> Every one-line installer below **automatically backs up your existing `hosts` file to `hosts.bak`** before overwriting it and immediately flushes the system DNS cache. If you have custom local domain mappings (e.g., Docker, local dev hosts, `127.0.1.1`), inspect your `.bak` file and merge those custom lines back as needed.

---

## One-Line Auto Install

Copy the single command for your operating system and run it in an elevated Terminal or Shell.

### 1. Windows (Windows 10 / 11)

#### Option A: PowerShell (Recommended)
Open **PowerShell** (or **Windows Terminal**) as **Administrator**, paste the command below, and press `Enter`:

```powershell
$h="$env:SystemRoot\System32\drivers\etc\hosts"; Copy-Item $h "$h.bak" -Force; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" -UseBasicParsing -OutFile $h; ipconfig /flushdns; Write-Host "Host-Ad-Block installed successfully!" -ForegroundColor Green
```

#### Option B: Command Prompt (CMD)
Open **Command Prompt (CMD)** as **Administrator**, paste the command below, and press `Enter`:

```cmd
copy /Y "%SystemRoot%\System32\drivers\etc\hosts" "%SystemRoot%\System32\drivers\etc\hosts.bak" && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" -o "%SystemRoot%\System32\drivers\etc\hosts" && ipconfig /flushdns
```

> [!TIP]
> On Windows 10/11, if you notice sluggish network resolution or browser delays after installing a large `hosts` file (~5 MB), consider disabling the `Dnscache` (DNS Client) service—though most modern systems handle it smoothly as-is.

---

### 2. macOS (Intel & Apple Silicon M1/M2/M3/M4)

Open **Terminal** (`zsh` or `bash`) and run (enter your macOS password when prompted):

```bash
sudo cp /etc/hosts /etc/hosts.bak && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d '\r' | sudo tee /etc/hosts > /dev/null && sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder && echo "Host-Ad-Block installed on macOS successfully!"
```

---

### 3. Linux (Ubuntu, Debian, Fedora, Arch, CentOS, RHEL, Linux Mint, Kali, etc.)

#### Using `curl` (Pre-installed on most distributions)
Open **Terminal** and run (backs up `/etc/hosts`, applies the blocklist, and flushes DNS caches across `systemd-resolved`, `NetworkManager`, or `nscd` if present):

```bash
sudo cp /etc/hosts /etc/hosts.bak && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d '\r' | sudo tee /etc/hosts > /dev/null && (sudo resolvectl flush-caches 2>/dev/null || sudo systemd-resolve --flush-caches 2>/dev/null || sudo systemctl restart NetworkManager 2>/dev/null || sudo service nscd restart 2>/dev/null || true) && echo "Host-Ad-Block installed on Linux successfully!"
```

#### Alternative using `wget` (if `curl` is not installed)

```bash
sudo cp /etc/hosts /etc/hosts.bak && wget -qO- "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d '\r' | sudo tee /etc/hosts > /dev/null && (sudo resolvectl flush-caches 2>/dev/null || sudo systemd-resolve --flush-caches 2>/dev/null || sudo systemctl restart NetworkManager 2>/dev/null || sudo service nscd restart 2>/dev/null || true) && echo "Host-Ad-Block installed on Linux successfully!"
```

---

### 4. Android

#### Option A: Non-Root (Recommended)
Install a local VPN/DNS ad-blocker such as **AdAway** (VPN mode), **RethinkDNS**, **DNS66**, or **PersonalDNSfilter**, then add the raw URL below under **Hosts Sources / Blocklists**:

```text
https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt
```

#### Option B: Rooted Devices (Magisk Systemless Hosts / Termux / ADB Shell)
> [!TIP]
> If you use Magisk, enable **Systemless hosts** in Magisk Settings before running this command.

Run the following command in **Termux** or `adb shell` on your rooted device:

```bash
su -c 'TARGET="/data/adb/modules/hosts/system/etc/hosts"; [ ! -d "/data/adb/modules/hosts/system/etc" ] && TARGET="/system/etc/hosts" && mount -o rw,remount /system; cp "$TARGET" "$TARGET.bak" 2>/dev/null; curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d "\r" > "$TARGET" && chmod 644 "$TARGET" && echo "Host-Ad-Block installed on Android successfully!"'
```

*(Reboot your device or toggle Airplane Mode on/off afterward to clear Android's DNS cache.)*

---

### 5. iOS / iPadOS & Network Devices (Pi-hole, AdGuard Home, Routers)

#### AdGuard Home / Pi-hole / Routers (OpenWrt, Asuswrt-Merlin, etc.)
- **AdGuard Home:** Go to **Filters** → **DNS blocklists** → **Add blocklist** → **Add a custom list**, paste the URL below, and save:
  ```text
  https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt
  ```
- **Pi-hole:** Go to **Adlists** (or **Lists** on Pi-hole v6) → paste the URL above → click **Add**, then run `pihole -g` (or go to **Tools** → **Update Gravity**).

#### iOS / iPadOS
- **Non-Jailbroken:** Use rule/hosts-capable DNS or VPN apps such as **Shadowrocket**, **Surge**, **Quantumult X**, or **AdGuard Pro** and subscribe directly to the Raw URL above.
- **Jailbroken:** Open an iOS terminal (NewTerm / SSH) and run:
  ```bash
  sudo cp /etc/hosts /etc/hosts.bak && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d '\r' | sudo tee /etc/hosts > /dev/null && sudo killall -HUP mDNSResponder && echo "Host-Ad-Block installed on iOS successfully!"
  ```

---

## Automatic Weekly Updates

Schedule your system to automatically pull the latest blocklist every Sunday:

### Windows (Task Scheduler — Sundays at 09:00 AM)
Open **PowerShell (Run as Administrator)** and run:

```powershell
$cmd = '$h="$env:SystemRoot\System32\drivers\etc\hosts"; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" -UseBasicParsing -OutFile $h; ipconfig /flushdns'; $enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd)); $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -EncodedCommand $enc"; $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 9am; Register-ScheduledTask -TaskName "UpdateHostAdBlock" -Action $action -Trigger $trigger -User "SYSTEM" -RunLevel Highest -Force
```

*(To remove the scheduled task on Windows: `Unregister-ScheduledTask -TaskName "UpdateHostAdBlock" -Confirm:$false`)*

### macOS (`crontab` — Sundays at 03:00 AM)

```bash
(sudo crontab -l 2>/dev/null | grep -v 'Host-Ad-Block'; printf '%s\n' '0 3 * * 0 t=$(mktemp) && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block\%20Ad.txt" -o "$t" && tr -d "\r" < "$t" > /etc/hosts && chmod 644 /etc/hosts && rm -f "$t" && dscacheutil -flushcache && killall -HUP mDNSResponder') | sudo crontab -
```

### Linux (`crontab` — Sundays at 03:00 AM)

```bash
(sudo crontab -l 2>/dev/null | grep -v 'Host-Ad-Block'; printf '%s\n' '0 3 * * 0 t=$(mktemp) && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block\%20Ad.txt" -o "$t" && tr -d "\r" < "$t" > /etc/hosts && chmod 644 /etc/hosts && rm -f "$t" && (resolvectl flush-caches 2>/dev/null || systemd-resolve --flush-caches 2>/dev/null || systemctl restart NetworkManager 2>/dev/null || service nscd restart 2>/dev/null || true)') | sudo crontab -
```

*(Note: Inside `crontab` entries, `%` must be escaped as `\%20` because `cron` treats unescaped `%` characters as newlines.)*

---

## Verification

Test resolution against a blocked ad/tracker domain using `ping`:

- **Windows:**
  ```cmd
  ping -n 1 google-analytics.com
  ```
- **macOS / Linux:**
  ```bash
  ping -c 1 google-analytics.com
  ```

If the domain resolves to **`127.0.0.1`**, the ad-blocking `hosts` file is active and working.

> [!NOTE]
> If ads still appear inside a browser (Chrome, Edge, Firefox, etc.), check whether **Secure DNS / DNS-over-HTTPS (DoH)** is enabled in browser settings, as DoH can bypass the OS `hosts` file depending on configuration.

---

## Restore Default `hosts` File (Uninstall)

### Restore from `.bak` Backup

- **Windows (PowerShell - Administrator):**
  ```powershell
  $h="$env:SystemRoot\System32\drivers\etc\hosts"; Copy-Item "$h.bak" $h -Force; ipconfig /flushdns
  ```
- **Windows (CMD - Administrator):**
  ```cmd
  copy /Y "%SystemRoot%\System32\drivers\etc\hosts.bak" "%SystemRoot%\System32\drivers\etc\hosts" && ipconfig /flushdns
  ```
- **macOS:**
  ```bash
  sudo cp /etc/hosts.bak /etc/hosts && sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder
  ```
- **Linux:**
  ```bash
  sudo cp /etc/hosts.bak /etc/hosts && (sudo resolvectl flush-caches 2>/dev/null || sudo systemd-resolve --flush-caches 2>/dev/null || sudo systemctl restart NetworkManager 2>/dev/null || true)
  ```
- **Android (Root):**
  ```bash
  su -c 'TARGET="/data/adb/modules/hosts/system/etc/hosts"; [ ! -f "$TARGET.bak" ] && TARGET="/system/etc/hosts" && mount -o rw,remount /system; cp "$TARGET.bak" "$TARGET" && chmod 644 "$TARGET"'
  ```

### Standard Default `hosts` Contents (if `.bak` is unavailable)

<details>
<summary>View default hosts file templates for Windows, macOS, Linux, and Android</summary>

**Windows (`C:\Windows\System32\drivers\etc\hosts`):**
```text
127.0.0.1       localhost
::1             localhost
```

**macOS (`/etc/hosts`):**
```text
127.0.0.1	localhost
255.255.255.255	broadcasthost
::1             localhost
```

**Linux (`/etc/hosts`):**
```text
127.0.0.1	localhost
127.0.1.1	your-hostname

::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

**Android (`/system/etc/hosts`):**
```text
127.0.0.1       localhost
::1             ip6-localhost
```

</details>
