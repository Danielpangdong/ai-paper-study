#!/usr/bin/env bash
# ============================================================
# 站点每日更新脚本：重建索引 → 提交 → 推送到 GitHub（自动触发 Pages 部署）
# 用法：
#   bash tools/site-update.sh          # 手动执行一次
#   crontab 每日 09:30 自动执行（见 README「发布上线」）
# ============================================================
set -u
cd "$(dirname "$0")/.." || exit 1
LOG="tools/logs/site-update.log"
mkdir -p tools/logs

say() { echo "[$(date '+%F %T')] $*"; }
log() { say "$@" >> "$LOG"; echo "$(say "$@")"; }

log "======== 站点更新开始 ========"

# 1) 重建文章索引
if ! python3 tools/build.py >> "$LOG" 2>&1; then
  log "✗ 索引构建失败，终止（详见日志）"
  exit 1
fi
log "✓ 索引构建完成"

# 2) 有变化才提交（build 是确定性的，无新文章时无 diff；用 porcelain 判断以涵盖未跟踪文件）
if ! git status --porcelain | grep -q .; then
  log "· 无新文章/无变化，跳过提交与推送"
  exit 0
fi

git add -A
git commit -m "chore: 每日站点更新 $(date '+%Y-%m-%d %H:%M')" >> "$LOG" 2>&1 \
  && log "✓ 已提交" || log "✗ 提交失败（检查 git 身份配置）"

# 3) 推送（未配置远端/未登录时静默失败，不影响下次）
if git remote | grep -q origin; then
  if git push origin HEAD >> "$LOG" 2>&1; then
    log "✓ 已推送到 GitHub，Pages 将自动部署"
  else
    log "✗ push 失败：可能未执行 gh auth login / gh auth setup-git"
  fi
else
  log "· 尚未配置远程仓库 origin，跳过推送"
fi
log "======== 完成 ========"
