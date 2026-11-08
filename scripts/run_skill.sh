#!/bin/zsh
# Usage: scripts/run_skill.sh <skill-name>   (e.g. carsale-load-olx). Called by launchd.
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"
cd "$HOME/ClaudeProjects/CarSale" || exit 1
mkdir -p logs
echo "=== $(date '+%F %T %Z') start $1" >> "logs/$1.log"
claude -p "Выполни скилл $1 из .claude/skills: следуй его шагам и выдай краткий отчёт." \
  --permission-mode acceptEdits \
  --allowedTools "Read" "Edit" "Write" "mcp__claude-in-chrome" \
  >> "logs/$1.log" 2>&1
echo "=== $(date '+%F %T %Z') end $1 (exit $?)" >> "logs/$1.log"
