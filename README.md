# Host-Ad-Block

Bộ sưu tập file `hosts` chặn quảng cáo và trình theo dõi ở cấp độ hệ điều hành cho **Windows**, **macOS**, **Linux**, **Android**, **iOS** và các thiết bị mạng (**AdGuard Home**, **Pi-hole**).

---

## Tổng quan

- **Repository:** [`LamPPKK/Host-Ad-Block`](https://github.com/LamPPKK/Host-Ad-Block)
- **File danh sách chặn:** [`Block Ad.txt`](Block%20Ad.txt)
- **Raw URL trực tiếp:**
  ```text
  https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt
  ```
- **Quy mô bộ lọc:** **~162.594 dòng chặn** (~162.579 tên miền duy nhất, dung lượng ~5,16 MB).
- **Phạm vi chặn:** Quảng cáo hiển thị (banner, pop-up), trình theo dõi (trackers), telemetry, analytics (Google Analytics, DoubleClick, Facebook Ads, quảng cáo Cốc Cốc, mạng quảng cáo bên thứ 3...).
- **Cơ chế hoạt động:** Chuyển hướng (sinkhole) toàn bộ tên miền quảng cáo về địa chỉ cục bộ `127.0.0.1` trực tiếp qua file `hosts` của hệ điều hành. Hoạt động trên mọi trình duyệt và ứng dụng mà không cần cài thêm phần mềm chạy nền, không tiêu tốn RAM hay CPU.

### Đường dẫn file `hosts` theo từng Hệ điều hành

| Hệ điều hành | Đường dẫn file `hosts` | Quyền yêu cầu |
| :--- | :--- | :--- |
| **Windows (10 / 11)** | `C:\Windows\System32\drivers\etc\hosts` | Administrator |
| **macOS** | `/etc/hosts` | `sudo` (root) |
| **Linux** | `/etc/hosts` | `sudo` (root) |
| **Android (Root / Magisk)** | `/data/adb/modules/hosts/system/etc/hosts` hoặc `/system/etc/hosts` | `su` (root) |
| **Android (Không Root)** | Áp dụng qua Local VPN/DNS (AdAway, RethinkDNS, DNS66...) | Không cần Root |
| **iOS / iPadOS** | App DNS/VPN (AdGuard, Shadowrocket...) hoặc `/etc/hosts` (Jailbreak) | Theo ứng dụng / Jailbreak |

> [!NOTE]
> Tất cả các lệnh cài đặt tự động bên dưới đều **tự động sao lưu file `hosts` cũ sang `hosts.bak`** trước khi ghi đè và xóa bộ nhớ đệm DNS (flush DNS) ngay lập tức. Nếu bạn có cấu hình tên miền nội bộ riêng (như Docker, local dev, `127.0.1.1`...), hãy mở file `.bak` để giữ lại các dòng tùy chỉnh đó.

---

## Lệnh cài đặt tự động (One-Line Auto Install)

Chỉ cần sao chép **1 dòng lệnh** tương ứng với hệ điều hành của bạn và chạy trong Terminal/PowerShell với quyền quản trị.

### 1. Windows (Windows 10 / 11)

#### Cách 1: PowerShell (Khuyên dùng)
Mở **PowerShell** (hoặc **Windows Terminal**) bằng **Run as Administrator**, dán lệnh sau và nhấn `Enter`:

```powershell
$h="$env:SystemRoot\System32\drivers\etc\hosts"; Copy-Item $h "$h.bak" -Force; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" -UseBasicParsing -OutFile $h; ipconfig /flushdns; Write-Host "Cài đặt Host-Ad-Block thành công!" -ForegroundColor Green
```

#### Cách 2: Command Prompt (CMD)
Mở **Command Prompt (CMD)** bằng **Run as Administrator**, dán lệnh sau và nhấn `Enter`:

```cmd
copy /Y "%SystemRoot%\System32\drivers\etc\hosts" "%SystemRoot%\System32\drivers\etc\hosts.bak" && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" -o "%SystemRoot%\System32\drivers\etc\hosts" && ipconfig /flushdns
```

> [!TIP]
> Trên Windows 10/11, nếu thấy mạng chậm hoặc trình duyệt lag nhẹ sau khi thay file `hosts` dung lượng lớn, bạn có thể tắt bớt dịch vụ `Dnscache` (DNS Client) hoặc bỏ qua nếu máy chạy bình thường — đa số máy hiện đại xử lý tốt file ~5 MB.

---

### 2. macOS (Intel & Apple Silicon M1/M2/M3/M4)

Mở **Terminal** (`zsh` hoặc `bash`), chạy lệnh sau (nhập mật khẩu máy khi được hỏi):

```bash
sudo cp /etc/hosts /etc/hosts.bak && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d '\r' | sudo tee /etc/hosts > /dev/null && sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder && echo "Cài đặt Host-Ad-Block trên macOS thành công!"
```

---

### 3. Linux (Ubuntu, Debian, Fedora, Arch, CentOS, RHEL, Linux Mint, Kali...)

#### Dùng `curl` (Mặc định trên hầu hết các bản phân phối)
Mở **Terminal**, chạy lệnh sau (tự động sao lưu, cập nhật `/etc/hosts` và làm mới cache DNS cho `systemd-resolved`, `NetworkManager` hoặc `nscd` nếu hệ thống có dùng):

```bash
sudo cp /etc/hosts /etc/hosts.bak && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d '\r' | sudo tee /etc/hosts > /dev/null && (sudo resolvectl flush-caches 2>/dev/null || sudo systemd-resolve --flush-caches 2>/dev/null || sudo systemctl restart NetworkManager 2>/dev/null || sudo service nscd restart 2>/dev/null || true) && echo "Cài đặt Host-Ad-Block trên Linux thành công!"
```

#### Lệnh thay thế dùng `wget` (nếu máy chưa cài `curl`)

```bash
sudo cp /etc/hosts /etc/hosts.bak && wget -qO- "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d '\r' | sudo tee /etc/hosts > /dev/null && (sudo resolvectl flush-caches 2>/dev/null || sudo systemd-resolve --flush-caches 2>/dev/null || sudo systemctl restart NetworkManager 2>/dev/null || sudo service nscd restart 2>/dev/null || true) && echo "Cài đặt Host-Ad-Block trên Linux thành công!"
```

---

### 4. Android

#### Cách 1: Không cần Root (Khuyên dùng)
Sử dụng ứng dụng chặn quảng cáo qua Local VPN/DNS như **AdAway** (chế độ VPN), **RethinkDNS**, **DNS66** hoặc **PersonalDNSfilter**, sau đó thêm URL nguồn hosts sau vào phần **Hosts Sources / Blocklists**:

```text
https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt
```

#### Cách 2: Máy đã Root (Magisk Systemless Hosts / Termux / ADB Shell)
> [!TIP]
> Nếu dùng Magisk, hãy bật tùy chọn **Systemless hosts** trong phần Cài đặt của Magisk trước khi chạy lệnh.

Chạy lệnh sau trong **Termux** hoặc `adb shell` trên máy đã Root:

```bash
su -c 'TARGET="/data/adb/modules/hosts/system/etc/hosts"; [ ! -d "/data/adb/modules/hosts/system/etc" ] && TARGET="/system/etc/hosts" && mount -o rw,remount /system; cp "$TARGET" "$TARGET.bak" 2>/dev/null; curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d "\r" > "$TARGET" && chmod 644 "$TARGET" && echo "Cài đặt Host-Ad-Block trên Android thành công!"'
```

*(Sau khi chạy xong, khởi động lại máy hoặc bật/tắt Chế độ máy bay để xóa cache DNS trên Android.)*

---

### 5. iOS / iPadOS & Thiết bị mạng (Pi-hole, AdGuard Home, Router)

#### AdGuard Home / Pi-hole / Router (OpenWrt, Merlin...)
- **AdGuard Home:** Vào **Filters** → **DNS blocklists** → **Add blocklist** → **Add a custom list**, dán URL bên dưới và lưu lại:
  ```text
  https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt
  ```
- **Pi-hole:** Vào **Adlists** (hoặc **Lists** trên Pi-hole v6) → dán URL trên → nhấn **Add**, sau đó chạy `pihole -g` (hoặc vào **Tools** → **Update Gravity**).

#### iOS / iPadOS
- **Máy chưa Jailbreak:** Dùng các ứng dụng hỗ trợ chặn theo rule/hosts như **Shadowrocket**, **Surge**, **Quantumult X** hoặc **AdGuard Pro** và thêm trực tiếp Raw URL ở trên vào danh sách DNS Blocklist/Rule.
- **Máy đã Jailbreak:** Mở Terminal trên iOS (NewTerm / SSH) và chạy:
  ```bash
  sudo cp /etc/hosts /etc/hosts.bak && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" | tr -d '\r' | sudo tee /etc/hosts > /dev/null && sudo killall -HUP mDNSResponder && echo "Cài đặt Host-Ad-Block trên iOS thành công!"
  ```

---

## Tự động cập nhật định kỳ (Auto-Update Schedule)

Nếu bạn muốn hệ thống tự động tải bản mới nhất hàng tuần vào mỗi Chủ Nhật:

### Windows (Task Scheduler — mỗi Chủ Nhật lúc 09:00 sáng)
Mở **PowerShell (Run as Administrator)** và chạy:

```powershell
$cmd = '$h="$env:SystemRoot\System32\drivers\etc\hosts"; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block%20Ad.txt" -UseBasicParsing -OutFile $h; ipconfig /flushdns'; $enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd)); $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -WindowStyle Hidden -EncodedCommand $enc"; $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 9am; Register-ScheduledTask -TaskName "UpdateHostAdBlock" -Action $action -Trigger $trigger -User "SYSTEM" -RunLevel Highest -Force
```

*(Để gỡ lịch tự động trên Windows: `Unregister-ScheduledTask -TaskName "UpdateHostAdBlock" -Confirm:$false`)*

### macOS (`crontab` — mỗi Chủ Nhật lúc 03:00 sáng)

```bash
(sudo crontab -l 2>/dev/null | grep -v 'Host-Ad-Block'; printf '%s\n' '0 3 * * 0 t=$(mktemp) && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block\%20Ad.txt" -o "$t" && tr -d "\r" < "$t" > /etc/hosts && chmod 644 /etc/hosts && rm -f "$t" && dscacheutil -flushcache && killall -HUP mDNSResponder') | sudo crontab -
```

### Linux (`crontab` — mỗi Chủ Nhật lúc 03:00 sáng)

```bash
(sudo crontab -l 2>/dev/null | grep -v 'Host-Ad-Block'; printf '%s\n' '0 3 * * 0 t=$(mktemp) && curl -fsSL "https://raw.githubusercontent.com/LamPPKK/Host-Ad-Block/main/Block\%20Ad.txt" -o "$t" && tr -d "\r" < "$t" > /etc/hosts && chmod 644 /etc/hosts && rm -f "$t" && (resolvectl flush-caches 2>/dev/null || systemd-resolve --flush-caches 2>/dev/null || systemctl restart NetworkManager 2>/dev/null || service nscd restart 2>/dev/null || true)') | sudo crontab -
```

*(Lưu ý: Trong `crontab`, ký tự `%` bắt buộc phải được escape thành `\%20` để cron không hiểu nhầm là ký tự xuống dòng.)*

---

## Kiểm tra sau khi cài đặt (Verification)

Chạy lệnh `ping` thử một tên miền quảng cáo/theo dõi có trong danh sách:

- **Windows:**
  ```cmd
  ping -n 1 google-analytics.com
  ```
- **macOS / Linux:**
  ```bash
  ping -c 1 google-analytics.com
  ```

Nếu kết quả phân giải ra **`127.0.0.1`**, tức là file `hosts` chặn quảng cáo đã hoạt động chính xác.

> [!NOTE]
> Nếu trình duyệt (Chrome, Edge, Firefox...) vẫn hiện quảng cáo, hãy kiểm tra xem trình duyệt có đang bật **Secure DNS / DNS-over-HTTPS (DoH)** hay không, vì DoH có thể bỏ qua file `hosts` cục bộ trên một số cấu hình.

---

## Khôi phục file Hosts mặc định (Restore / Uninstall)

### Khôi phục từ bản sao lưu `.bak`

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

### Nội dung file `hosts` mặc định chuẩn (khi không còn file `.bak`)

<details>
<summary>Xem mẫu file hosts mặc định cho Windows, macOS, Linux và Android</summary>

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
