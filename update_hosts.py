#!/usr/bin/env python3
"""Sync and merge ad-blocking domains into Block Ad.txt from upstream hosts repositories."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re
import urllib.request

UPSTREAM_SOURCES: list[tuple[str, str]] = [
    ("StevenBlack/hosts", "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"),
    ("bigdargon/hostsVN", "https://raw.githubusercontent.com/bigdargon/hostsVN/master/hosts"),
    ("AdAway/adaway.github.io", "https://raw.githubusercontent.com/AdAway/adaway.github.io/master/hosts.txt"),
    ("anudeepND/blacklist", "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt"),
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
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "Block Ad.txt"


def is_valid_domain(domain: str) -> bool:
    """Return True if domain is a valid, non-reserved blockable hostname."""
    if not domain or domain in RESERVED_HOSTS or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    return bool(VALID_DOMAIN_RE.match(domain))


def extract_domains(text: str) -> set[str]:
    """Extract normalized ad-blocking domains mapped to 0.0.0.0 or 127.0.0.1."""
    domains: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2 or parts[0] not in ("0.0.0.0", "127.0.0.1"):
            continue
        for candidate in parts[1:]:
            domain = candidate.strip().lower()
            if is_valid_domain(domain):
                domains.add(domain)
    return domains


def fetch_source(url: str, timeout: int = 30) -> str:
    """Download an upstream hosts list as UTF-8 text."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


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
    """Fetch upstream sources, merge with existing domains, and write output_path."""
    all_domains: set[str] = set()

    if include_existing and output_path.exists():
        existing_text = output_path.read_text(encoding="utf-8-sig", errors="ignore")
        all_domains = extract_domains(existing_text)
        print(f"Existing domains loaded: {len(all_domains):,}")

    for name, url in UPSTREAM_SOURCES:
        text = fetch_source(url, timeout=timeout)
        fetched = extract_domains(text)
        added = len(fetched - all_domains)
        all_domains.update(fetched)
        print(f"Fetched {name}: {len(fetched):,} domains ({added:,} new)")

    sorted_domains = sorted(all_domains)
    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    rendered = render_hosts_file(sorted_domains, updated_at)

    with output_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(rendered)

    print(f"Wrote {len(sorted_domains):,} unique domains to {output_path}")
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
