#!/bin/zsh
# Daily report: update summary + chart, analyse changes, send the CarSaleBot e-mail. Called by launchd at 09:15.
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"
cd "$HOME/ClaudeProjects/CarSale" || exit 1
mkdir -p logs
echo "=== $(date '+%F %T %Z') start report" >> logs/carsale-report.log
claude -p "Выполни по порядку скиллы из .claude/skills: 1) carsale-update-summary, 2) carsale-price-chart, 3) carsale-email-report. Проанализируй изменения (новые машины, изменения цен) и отправь письмо через Gmail-коннектор по правилам скилла carsale-email-report. Если сводка не изменилась — письмо не отправляй. В конце выдай краткий отчёт." \
  --permission-mode acceptEdits \
  --allowedTools "Read" "Edit" "Write" "Bash(.venv/bin/python update_summary.py)" "mcp__claude_ai_Gmail__send_message" \
  >> logs/carsale-report.log 2>&1
echo "=== $(date '+%F %T %Z') end report (exit $?)" >> logs/carsale-report.log
