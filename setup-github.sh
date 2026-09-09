#!/usr/bin/env bash
# GITHUB_KULLANICI yer tutucusunu gercek kullanici adiyla degistirir.
# Kullanim:  ./setup-github.sh kullanici-adin
set -euo pipefail
[ $# -eq 1 ] || { echo "Kullanim: $0 <github-kullanici-adi>"; exit 1; }
U="$1"
for f in .claude-plugin/marketplace.json LICENSE README.md; do
  sed -i.bak "s/GITHUB_KULLANICI/$U/g" "$f" && rm -f "$f.bak"
  echo "güncellendi: $f"
done
echo
echo "Sıradaki adımlar:"
echo "  git add -A && git commit -m 'chore: set owner to $U'"
echo "  gh repo create $U/roadmap-architect --public --source=. --push"
