#!/usr/bin/env bash
set -euo pipefail

# 1. 進入專案資料夾
cd "${HOME}/coding"

# 2. 暫存所有變更
git add -A

# 3. 檢查是否有變更（無變更則正常退出）
if git diff --cached --quiet; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] No changes, skip."
  exit 0
fi

# 4. 提交與時間戳記
git commit -m "auto: $(date '+%Y-%m-%d %H:%M')"

# 5. 防禦性同步並推送
git pull --rebase origin main
git push origin main
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pushed successfully!"
