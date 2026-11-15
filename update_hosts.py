#!/usr/bin/env python3
"""Sync and merge ad-blocking domains into Block Ad.txt from 24 upstream repositories."""

from __future__ import annotations

import argparse
import concurrent.futures
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
import urllib.request

UPSTREAM_SOURCES: list[tuple[str, str]] = [
    ("StevenBlack/hosts", "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"),
    ("bigdargon/hostsVN", "https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts"),
    ("AdAway/adaway.github.io", "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt"),
    ("anudeepND/blacklist", "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt"),
    ("Lightswitch05/hosts (Ads & Tracking)", "https://www.github.developerdan.com/hosts/lists/ads-and-tracking-extended.txt"),
    ("PolishFiltersTeam/KADhosts", "https://raw.githubusercontent.com/PolishFiltersTeam/KADhosts/master/KADhosts.txt"),
    ("SomeoneWhoCares (Dan Pollock)", "https://someonewhocares.org/hosts/zero/hosts"),
    ("Frogeye Multiparty Trackers", "https://hostfiles.frogeye.fr/multiparty-trackers-hosts.txt"),
    ("Frogeye First-Party Trackers", "https://hostfiles.frogeye.fr/firstparty-trackers-hosts.txt"),
    ("winhelp2002 MVPS", "https://winhelp2002.mvps.org/hosts.txt"),
    ("VeleSila/yhosts", "https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts"),
    ("neoFelhz/neohosts", "https://cdn.jsdelivr.net/gh/neoFelhz/neohosts@gh-pages/full/hosts"),
    ("Peter Lowe (yoyo.org)", "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext"),
    ("FadeMind/hosts.extras (add.Risk)", "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Risk/hosts"),
    ("FadeMind/hosts.extras (add.2o7Net)", "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.2o7Net/hosts"),
    ("FadeMind/hosts.extras (add.Spam)", "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/add.Spam/hosts"),
    ("FadeMind/hosts.extras (UncheckyAds)", "https://raw.githubusercontent.com/FadeMind/hosts.extras/master/UncheckyAds/hosts"),
    ("tiuxo/hosts (Ads)", "https://raw.githubusercontent.com/tiuxo/hosts/master/ads"),
    ("jdlingyu/ad-wars", "https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts"),
    ("mitchellkrogza/Badd-Boyz-Hosts", "https://raw.githubusercontent.com/mitchellkrogza/Badd-Boyz-Hosts/master/hosts"),
    ("Perflyst/PiHoleBlocklist (SmartTV)", "https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV.txt"),
    ("Perflyst/PiHoleBlocklist (AmazonFireTV)", "https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/AmazonFireTV.txt"),
    ("crazy-max/WindowsSpyBlocker", "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt"),
    ("DandelionSprout/adfilt (GameConsole)", "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/GameConsoleAdblockList.txt"),
]

RESERVED_HOSTS: frozenset[str] = frozenset(
    {
        "localhost",
        "localhost.localdomain",
        "local",
        "broadcasthost",
        "ip6-localhost",
        "ip6-loopback",
        "ip6-localnet",
        "ip6-mcastprefix",
        "ip6-allnodes",
        "ip6-allrouters",
        "ip6-allhosts",
        "0.0.0.0",
        "127.0.0.1",
        "::1",
        "view-localhost",
    }
)

VALID_DOMAIN_RE = re.compile(r"^[a-z0-9._-]+$")
IPV4_RE = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "Block Ad.txt"


def is_valid_domain(domain: str) -> bool:
    """Return True if domain is a valid, non-reserved blockable hostname."""
    if not domain or domain in RESERVED_HOSTS or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    if IPV4_RE.match(domain):
        return False
    return bool(VALID_DOMAIN_RE.match(domain))


def extract_domains(text: str) -> set[str]:
    """Extract normalized ad-blocking domains from hosts, plain-domain, or pure Adblock DNS rules."""
    domains: set[str] = set()
    for raw_line in text.splitlines():
        stripped = raw_line.lstrip("\ufeff").strip()
        if not stripped or stripped.startswith(("#", "!", "[", "@@", "/")):
            continue
        # Ignore cosmetic / element-hiding Adblock filters (e.g. example.com##.ad)
        if "##" in stripped or "#@#" in stripped or "#?#" in stripped or "#$#" in stripped:
            continue

        line = stripped.split("#", 1)[0].strip()
        if not line:
            continue

        # Pure Adblock DNS rule: ||domain.com^ (optionally $important or $all)
        if line.startswith("||") and "^" in line:
            candidate, _, rest = line[2:].partition("^")
            rest_lower = rest.strip().lower()
            if rest_lower in ("", "$important", "$all"):
                domain = candidate.strip().lower()
                if is_valid_domain(domain):
                    domains.add(domain)
            continue

        parts = line.split()
        if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"):
            for candidate in parts[1:]:
                domain = candidate.strip().lower()
                if is_valid_domain(domain):
                    domains.add(domain)
        elif len(parts) == 1:
            domain = parts[0].strip().lower()
            if is_valid_domain(domain):
                domains.add(domain)
    return domains


def fetch_source(name: str, url: str, timeout: int = 30) -> tuple[str, set[str] | None, str | None]:
    """Download and extract domains from an upstream list, returning (name, domains, error)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="ignore")
        return name, extract_domains(text), None
    except Exception as exc:  # noqa: BLE001 - continue merging remaining sources on transient fetch failures
        return name, None, str(exc)


def render_hosts_file(domains: list[str], updated_at: str) -> str:
    """Render the complete Block Ad.txt file with header, localhost entries, and sorted rules."""
    source_lines = "\n".join(f"#   - {name}: {url}" for name, url in UPSTREAM_SOURCES)
    header = (
        "# Host-Ad-Block\n"
        "# Repository: https://github.com/LamPPKK/Host-Ad-Block\n"
        f"# Last updated (UTC): {updated_at}\n"
        f"# Total unique domains: {len(domains):,}\n"
        "# Sources:\n"
        "#   - Existing Host-Ad-Block (GocMod collection)\n"
        f"{source_lines}\n"
        "#\n"
        "# Standard localhost entries\n"
        "127.0.0.1 localhost\n"
        "::1 localhost\n"
        "255.255.255.255 broadcasthost\n"
        "127.0.0.1 view-localhost\n"
        "\n"
        "# Blocked ad and tracker domains\n"
    )
    body = "\n".join(f"127.0.0.1 {domain}" for domain in domains)
    return f"{header}{body}\n"


def update_hosts(output_path: Path, include_existing: bool = True, timeout: int = 30) -> int:
    """Fetch upstream sources concurrently, merge with existing domains, and write output_path."""
    all_domains: set[str] = set()

    if include_existing and output_path.exists():
        existing_text = output_path.read_text(encoding="utf-8-sig", errors="ignore")
        all_domains = extract_domains(existing_text)
        print(f"Existing domains loaded: {len(all_domains):,}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(
            executor.map(lambda item: fetch_source(item[0], item[1], timeout), UPSTREAM_SOURCES)
        )

    succeeded = 0
    for name, fetched, error in results:
        if error is not None or fetched is None:
            print(f"[WARN] Failed to fetch {name}: {error}", file=sys.stderr)
            continue
        succeeded += 1
        added = len(fetched - all_domains)
        all_domains.update(fetched)
        print(f"Fetched {name}: {len(fetched):,} domains ({added:,} new)")

    if succeeded == 0 and not all_domains:
        raise RuntimeError("All upstream sources failed and no existing domains were loaded.")

    sorted_domains = sorted(all_domains)
    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    rendered = render_hosts_file(sorted_domains, updated_at)

    with output_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(rendered)

    print(
        f"Wrote {len(sorted_domains):,} unique domains to {output_path} "
        f"({succeeded}/{len(UPSTREAM_SOURCES)} sources succeeded)"
    )
    return len(sorted_domains)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Update Block Ad.txt from upstream hosts repositories.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path to the output hosts file (default: Block Ad.txt).",
    )
    parser.add_argument(
        "--no-existing",
        action="store_true",
        help="Rebuild strictly from upstream sources without merging existing entries.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP request timeout in seconds per source (default: 30).",
    )
    args = parser.parse_args()
    update_hosts(args.output, include_existing=not args.no_existing, timeout=args.timeout)


if __name__ == "__main__":
    main()
