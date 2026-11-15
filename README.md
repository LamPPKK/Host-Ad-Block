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
- **List Size:** **670,902 unique domains** (~21.98 MiB / ~23.05 MB).
- **Integrated Upstream Sources:** Merges and deduplicates the original GocMod collection with **24 curated upstream repositories** covering Vietnamese & global ads, first/third-party trackers, malware/scams, Windows telemetry, Smart TVs, and game consoles.
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
> On Windows 10/11, if you notice sluggish network resolution or browser delays after installing a large `hosts` file (~23 MB), consider disabling the `Dnscache` (DNS Client) service—though most modern systems handle it smoothly as-is.

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

## Auto-Sync from Upstream Repositories

[`Block Ad.txt`](Block%20Ad.txt) is built and kept up to date by concurrently fetching, normalizing, and deduplicating entries from **24 upstream repositories** alongside the base collection:

| # | Source Repository | Focus | Raw URL |
| :-: | :--- | :--- | :--- |
| 1 | **StevenBlack/hosts** | Unified ads & malware | `https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts` |
| 2 | **bigdargon/hostsVN** | Vietnamese & global ads | `https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts` |
| 3 | **AdAway/adaway.github.io** | Mobile ad servers | `https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt` |
| 4 | **anudeepND/blacklist** | Ad servers & trackers | `https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt` |
| 5 | **Lightswitch05/hosts (Ads & Tracking)** | Extended ads & tracking | `https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt` |
| 6 | **PolishFiltersTeam/KADhosts** | Scam, malware & phishing | `https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt` |
| 7 | **SomeoneWhoCares (Dan Pollock)** | Ads, shock & tracking | `https://someonewhocares.org/hosts/zero/hosts` |
| 8 | **Frogeye Multiparty Trackers** | Third-party trackers | `https://hostfiles.frogeye.fr/multiparty-trackers-hosts.txt` |
| 9 | **Frogeye First-Party Trackers** | First-party trackers | `https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt` |
| 10 | **winhelp2002 MVPS** | Classic ad/malware hosts | `https://winhelp2002.mvps.org/hosts.txt` |
| 11 | **VeleSila/yhosts** | Chinese & global ads | `https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts` |
| 12 | **neoFelhz/neohosts** | Ads & privacy trackers | `https://cdn.jsdelivr.net/gh/neoFelhz/neohosts@gh-pages/full/hosts` |
| 13 | **Peter Lowe (yoyo.org)** | Ad & tracking servers | `https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext` |
| 14 | **FadeMind/hosts.extras (add.Risk)** | Riskware & adware | `https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts` |
| 15 | **FadeMind/hosts.extras (add.2o7Net)** | Adobe/Omniture trackers | `https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts` |
| 16 | **FadeMind/hosts.extras (add.Spam)** | Spam & shady domains | `https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts` |
| 17 | **FadeMind/hosts.extras (UncheckyAds)** | Installer bundleware ads | `https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts` |
| 18 | **tiuxo/hosts (Ads)** | General ad networks | `https://raw.githubusercontent.com/tiuxo/hosts/master/ads` |
| 19 | **jdlingyu/ad-wars** | Mobile & video ads | `https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts` |
| 20 | **mitchellkrogza/Badd-Boyz-Hosts** | Malicious & ad hosts | `https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts` |
| 21 | **Perflyst/PiHoleBlocklist (SmartTV)** | Smart TV telemetry & ads | `https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt` |
| 22 | **Perflyst/PiHoleBlocklist (AmazonFireTV)** | Fire TV telemetry & ads | `https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/AmazonFireTV.txt` |
| 23 | **crazy-max/WindowsSpyBlocker** | Windows spy & telemetry | `https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt` |
| 24 | **DandelionSprout/adfilt (GameConsole)** | Console menu ads | `https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt` |
| — | **Host-Ad-Block (Base)** | Existing GocMod collection | `https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt` |

### Method 1: Update Repository via [`update_hosts.py`](update_hosts.py) (Local CLI One-Liner)
Run inside a cloned copy of this repo to fetch all 24 upstream repositories concurrently, normalize & deduplicate rules, commit, and push the updated `Block Ad.txt`:

```bash
python3 update_hosts.py && git add "Block Ad.txt" && git commit -m "chore(hosts): sync blocklist from upstream repos" && git push
```

*(Pass `--no-existing` to rebuild strictly from the 24 upstream sources without retaining older entries in `Block Ad.txt`.)*

### Method 2: Automated Cloud Sync via GitHub Actions
This repository includes [`.github/workflows/update-hosts.yml`](.github/workflows/update-hosts.yml), which automatically runs `python3 update_hosts.py` every **Sunday at 00:00 UTC** and commits updates directly to `main`. You can also trigger it manually at any time from the GitHub **Actions** tab or via GitHub CLI:

```bash
gh workflow run update-hosts.yml
```

### Method 3: Direct Multi-Repo Merge One-Liner (No Cloning Required)
Pull, normalize, and deduplicate directly from all 24 upstream repositories plus the base list straight into your OS `hosts` file:

- **macOS (`curl` + `awk` + `sort -u`):**
  ```bash
  sudo cp /etc/hosts /etc/hosts.bak && t=$(mktemp) && { printf '127.0.0.1 localhost\n::1 localhost\n255.255.255.255 broadcasthost\n'; curl -fsSL --max-time 30 "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts" "https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts" "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt" "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt" "https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt" "https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt" "https://someonewhocares.org/hosts/zero/hosts" "https://hostfiles.frogeye.fr/multiparty-trackers-hosts.txt" "https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt" "https://winhelp2002.mvps.org/hosts.txt" "https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts" "https://cdn.jsdelivr.net/gh/neoFelhz/neohosts@gh-pages/full/hosts" "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext" "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts" "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts" "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts" "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts" "https://raw.githubusercontent.com/tiuxo/hosts/master/ads" "https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts" "https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts" "https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt" "https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/AmazonFireTV.txt" "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt" "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt" | tr -d '\r' | awk 'BEGIN{split("localhost localhost.localdomain local broadcasthost ip6-localhost ip6-loopback ip6-localnet ip6-mcastprefix ip6-allnodes ip6-allrouters ip6-allhosts view-localhost 0.0.0.0 127.0.0.1",a); for(i in a) skip[a[i]]=1} /^[#!\[\/]|^@@|##|#@#|#\?#|#\$#/{next} {sub(/#.*/,"")} /^\|\|.*\^/{s=$0; sub(/^\|\|/,"",s); sub(/\^.*/,"",s); r=$0; sub(/.*\^/,"",r); gsub(/^[ \t]+|[ \t]+$/,"",r); r=tolower(r); if(r==""||r=="$important"||r=="$all"){d=tolower(s); if(d~/^[a-z0-9._-]+$/ && d~/\./ && d!~/^\.|\.$/ && d!~/\.\./ && d!~/^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ && !(d in skip)) print "127.0.0.1 " d} next} $1=="0.0.0.0"||$1=="127.0.0.1"{for(i=2;i<=NF;i++){d=tolower($i); if(d~/^[a-z0-9._-]+$/ && d~/\./ && d!~/^\.|\.$/ && d!~/\.\./ && d!~/^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ && !(d in skip)) print "127.0.0.1 " d} next} NF==1{d=tolower($1); if(d~/^[a-z0-9._-]+$/ && d~/\./ && d!~/^\.|\.$/ && d!~/\.\./ && d!~/^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ && !(d in skip)) print "127.0.0.1 " d}' | LC_ALL=C sort -u; } > "$t" && [ $(wc -l < "$t") -gt 10000 ] && sudo tee /etc/hosts < "$t" > /dev/null && rm -f "$t" && sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder && echo "Synced multi-repo hosts on macOS successfully!"
  ```

- **Linux (`curl` + `awk` + `sort -u`):**
  ```bash
  sudo cp /etc/hosts /etc/hosts.bak && t=$(mktemp) && { printf '127.0.0.1 localhost\n::1 localhost\n'; curl -fsSL --max-time 30 "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts" "https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts" "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt" "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt" "https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt" "https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt" "https://someonewhocares.org/hosts/zero/hosts" "https://hostfiles.frogeye.fr/multiparty-trackers-hosts.txt" "https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt" "https://winhelp2002.mvps.org/hosts.txt" "https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts" "https://cdn.jsdelivr.net/gh/neoFelhz/neohosts@gh-pages/full/hosts" "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext" "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts" "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts" "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts" "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts" "https://raw.githubusercontent.com/tiuxo/hosts/master/ads" "https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts" "https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts" "https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt" "https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/AmazonFireTV.txt" "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt" "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt" | tr -d '\r' | awk 'BEGIN{split("localhost localhost.localdomain local broadcasthost ip6-localhost ip6-loopback ip6-localnet ip6-mcastprefix ip6-allnodes ip6-allrouters ip6-allhosts view-localhost 0.0.0.0 127.0.0.1",a); for(i in a) skip[a[i]]=1} /^[#!\[\/]|^@@|##|#@#|#\?#|#\$#/{next} {sub(/#.*/,"")} /^\|\|.*\^/{s=$0; sub(/^\|\|/,"",s); sub(/\^.*/,"",s); r=$0; sub(/.*\^/,"",r); gsub(/^[ \t]+|[ \t]+$/,"",r); r=tolower(r); if(r==""||r=="$important"||r=="$all"){d=tolower(s); if(d~/^[a-z0-9._-]+$/ && d~/\./ && d!~/^\.|\.$/ && d!~/\.\./ && d!~/^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ && !(d in skip)) print "127.0.0.1 " d} next} $1=="0.0.0.0"||$1=="127.0.0.1"{for(i=2;i<=NF;i++){d=tolower($i); if(d~/^[a-z0-9._-]+$/ && d~/\./ && d!~/^\.|\.$/ && d!~/\.\./ && d!~/^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ && !(d in skip)) print "127.0.0.1 " d} next} NF==1{d=tolower($1); if(d~/^[a-z0-9._-]+$/ && d~/\./ && d!~/^\.|\.$/ && d!~/\.\./ && d!~/^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/ && !(d in skip)) print "127.0.0.1 " d}' | LC_ALL=C sort -u; } > "$t" && [ $(wc -l < "$t") -gt 10000 ] && sudo tee /etc/hosts < "$t" > /dev/null && rm -f "$t" && (sudo resolvectl flush-caches 2>/dev/null || sudo systemd-resolve --flush-caches 2>/dev/null || sudo systemctl restart NetworkManager 2>/dev/null || sudo service nscd restart 2>/dev/null || true) && echo "Synced multi-repo hosts on Linux successfully!"
  ```

- **Windows PowerShell (Run as Administrator):**
  ```powershell
  $h="$env:SystemRoot\System32\drivers\etc\hosts"; Copy-Item $h "$h.bak" -Force; $urls=@("https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt","https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts","https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts","https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt","https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt","https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt","https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt","https://someonewhocares.org/hosts/zero/hosts","https://hostfiles.frogeye.fr/multiparty-trackers-hosts.txt","https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt","https://winhelp2002.mvps.org/hosts.txt","https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts","https://cdn.jsdelivr.net/gh/neoFelhz/neohosts@gh-pages/full/hosts","https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext","https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts","https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts","https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts","https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts","https://raw.githubusercontent.com/tiuxo/hosts/master/ads","https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts","https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts","https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt","https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/AmazonFireTV.txt","https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt","https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt"); $skip=[System.Collections.Generic.HashSet[string]]::new([string[]]@("localhost","localhost.localdomain","local","broadcasthost","ip6-localhost","ip6-loopback","ip6-localnet","ip6-mcastprefix","ip6-allnodes","ip6-allrouters","ip6-allhosts","view-localhost","0.0.0.0","127.0.0.1"),[StringComparer]::OrdinalIgnoreCase); $set=[System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase); foreach($u in $urls){try{(Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 30).Content -split "`r?`n" | ForEach-Object {$s=$_.Trim().TrimStart([char]0xFEFF); if(!$s -or $s -match '^(#|!|\[|@@|/)' -or $s -match '##|#@#|#\?#|#\$#'){return}; $l=($s -replace '#.*','').Trim(); if(!$l){return}; if($l -match '^\|\|([^\^]+)\^(.*)$'){if($Matches[2].Trim() -in @('','$important','$all')){$d=$Matches[1].Trim().ToLower(); if($d -match '^[a-z0-9._-]+$' -and $d.Contains('.') -and !$d.StartsWith('.') -and !$d.EndsWith('.') -and !$d.Contains('..') -and $d -notmatch '^\d{1,3}(\.\d{1,3}){3}$' -and !$skip.Contains($d)){[void]$set.Add($d)}}; return}; if($l -match '^(?:0\.0\.0\.0|127\.0\.0\.1)\s+(.+)$'){foreach($d in ($Matches[1] -split '\s+')){$d=$d.ToLower(); if($d -match '^[a-z0-9._-]+$' -and $d.Contains('.') -and !$d.StartsWith('.') -and !$d.EndsWith('.') -and !$d.Contains('..') -and $d -notmatch '^\d{1,3}(\.\d{1,3}){3}$' -and !$skip.Contains($d)){[void]$set.Add($d)}}} elseif($l -notmatch '\s'){$d=$l.ToLower(); if($d -match '^[a-z0-9._-]+$' -and $d.Contains('.') -and !$d.StartsWith('.') -and !$d.EndsWith('.') -and !$d.Contains('..') -and $d -notmatch '^\d{1,3}(\.\d{1,3}){3}$' -and !$skip.Contains($d)){[void]$set.Add($d)}}}} catch {Write-Warning "Skipped $u : $_"}}; $out=@("127.0.0.1 localhost","::1 localhost")+($set | Sort-Object | ForEach-Object {"127.0.0.1 $_"}); [IO.File]::WriteAllLines($h,$out,[Text.UTF8Encoding]::new($false)); ipconfig /flushdns; Write-Host "Synced $($set.Count) unique domains!" -ForegroundColor Green
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
