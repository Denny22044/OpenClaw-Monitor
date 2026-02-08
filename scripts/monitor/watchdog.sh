#!/bin/bash
#
# OpenClaw Watchdog - Überwacht Gateway & TUI
# Location: ~/.openclaw/scripts/watchdog.sh
#
# Usage:
#   ./watchdog.sh start    - Startet Watchdog im Hintergrund
#   ./watchdog.sh stop     - Stoppt Watchdog
#   ./watchdog.sh status   - Zeigt Status
#   ./watchdog.sh check    - Einmaliger Check (für Cron)
#

set -euo pipefail

# === CONFIGURATION ===
OPENCLAW_DIR="/Users/ccc/clawdbot"
CONFIG_FILE="/Users/ccc/.openclaw/openclaw.json"
LOG_DIR="/Users/ccc/.openclaw/logs"
WATCHDOG_LOG="$LOG_DIR/watchdog.log"
WATCHDOG_PID="$LOG_DIR/watchdog.pid"
GATEWAY_LOG="/tmp/openclaw-gateway.log"

# Gateway settings (aus Config auslesen)
GATEWAY_PORT=$(jq -r '.gateway.port // 18789' "$CONFIG_FILE" 2>/dev/null || echo "18789")
GATEWAY_TOKEN=$(jq -r '.gateway.auth.token // ""' "$CONFIG_FILE" 2>/dev/null || echo "")

# Thresholds
CHECK_INTERVAL=30          # Sekunden zwischen Checks
STALE_LOG_THRESHOLD=300    # Log älter als 5 Min = potenziell stuck
MAX_RESTART_ATTEMPTS=3     # Max Neustarts bevor Pause
RESTART_COOLDOWN=600       # 10 Min Pause nach Max-Restarts

# State tracking
RESTART_COUNT=0
LAST_RESTART=0
LAST_CHECK_TIME=0

# Wake detection threshold (if gap > 2x interval, we probably woke from sleep)
WAKE_THRESHOLD=$((CHECK_INTERVAL * 2))

# === FUNCTIONS ===

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$WATCHDOG_LOG"
}

ensure_log_dir() {
    mkdir -p "$LOG_DIR"
}

# Check if gateway process is running
is_gateway_running() {
    pgrep -f "openclaw-gateway" >/dev/null 2>&1
}

# Check if TUI process is running
is_tui_running() {
    pgrep -f "openclaw.*tui" >/dev/null 2>&1
}

# Check if TUI has active WebSocket connection to gateway
is_tui_connected() {
    lsof -i ":$GATEWAY_PORT" 2>/dev/null | grep -q "ESTABLISHED"
}

# Get TUI process info
get_tui_pid() {
    pgrep -f "openclaw.*tui" | head -1
}

# Restart TUI in new Terminal window (Homebrew profile)
restart_tui() {
    log "🖥️  TUI wird neugestartet..."

    # Kill existing TUI
    pkill -9 -f "openclaw.*tui" 2>/dev/null || true
    sleep 1

    # Start new TUI in Terminal with Homebrew profile
    osascript -e '
        tell application "Terminal"
            activate
            do script "cd /Users/ccc/clawdbot && pnpm openclaw tui"
            set current settings of front window to settings set "Homebrew"
        end tell
    ' 2>/dev/null

    sleep 4

    if is_tui_running; then
        log "✅ TUI erfolgreich neugestartet (PID: $(get_tui_pid))"
        return 0
    else
        log "❌ TUI-Neustart fehlgeschlagen - bitte manuell starten: cd $OPENCLAW_DIR && pnpm openclaw tui"
        return 1
    fi
}

# Check if gateway port is responding
is_gateway_responsive() {
    # Simple TCP check
    nc -z 127.0.0.1 "$GATEWAY_PORT" 2>/dev/null
}

# Check if logs are being updated (not stale)
is_log_fresh() {
    local log_file="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    if [[ -f "$log_file" ]]; then
        local last_mod=$(stat -f %m "$log_file" 2>/dev/null || stat -c %Y "$log_file" 2>/dev/null)
        local now=$(date +%s)
        local age=$((now - last_mod))
        [[ $age -lt $STALE_LOG_THRESHOLD ]]
    else
        # No log file yet today - check gateway log
        if [[ -f "$GATEWAY_LOG" ]]; then
            local last_mod=$(stat -f %m "$GATEWAY_LOG" 2>/dev/null || stat -c %Y "$GATEWAY_LOG" 2>/dev/null)
            local now=$(date +%s)
            local age=$((now - last_mod))
            [[ $age -lt $STALE_LOG_THRESHOLD ]]
        else
            return 1
        fi
    fi
}

# Check for error patterns in recent logs
check_for_errors() {
    local errors=""

    # Check gateway log for critical errors
    if [[ -f "$GATEWAY_LOG" ]]; then
        errors=$(tail -50 "$GATEWAY_LOG" 2>/dev/null | grep -iE "fatal|crash|panic|ECONNREFUSED|credit.*(low|insufficient)" | tail -3 || true)
    fi

    if [[ -n "$errors" ]]; then
        echo "$errors"
        return 1
    fi
    return 0
}

# Check for stuck sessions (processing for too long)
check_stuck_sessions() {
    local log_file="/tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
    if [[ -f "$log_file" ]]; then
        # Look for sessions stuck in "processing" state for > 2 minutes
        local stuck=$(tail -100 "$log_file" 2>/dev/null | \
            grep "session state.*processing" | \
            head -1 | \
            grep -oE '"date":"[^"]+' | \
            sed 's/"date":"//' || true)

        if [[ -n "$stuck" ]]; then
            local stuck_time=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${stuck:0:19}" +%s 2>/dev/null || echo "0")
            local now=$(date +%s)
            local age=$((now - stuck_time))

            if [[ $age -gt 120 ]]; then
                echo "Session stuck for ${age}s"
                return 1
            fi
        fi
    fi
    return 0
}

# Restart gateway
restart_gateway() {
    local now=$(date +%s)

    # Check cooldown
    if [[ $RESTART_COUNT -ge $MAX_RESTART_ATTEMPTS ]]; then
        local cooldown_remaining=$((LAST_RESTART + RESTART_COOLDOWN - now))
        if [[ $cooldown_remaining -gt 0 ]]; then
            log "⏳ Cooldown aktiv - noch ${cooldown_remaining}s warten (zu viele Restarts)"
            return 1
        else
            RESTART_COUNT=0
        fi
    fi

    log "🔄 Gateway wird neugestartet..."

    # Kill existing gateway processes
    pkill -9 -f "openclaw-gateway" 2>/dev/null || true
    pkill -9 -f "node.*gateway.*$GATEWAY_PORT" 2>/dev/null || true
    sleep 2

    # Start new gateway
    cd "$OPENCLAW_DIR"
    nohup pnpm openclaw gateway run --bind loopback --port "$GATEWAY_PORT" --token "$GATEWAY_TOKEN" \
        > "$GATEWAY_LOG" 2>&1 &

    sleep 5

    # Verify it started
    if is_gateway_running && is_gateway_responsive; then
        log "✅ Gateway erfolgreich neugestartet (PID: $(pgrep -f openclaw-gateway | head -1))"
        RESTART_COUNT=$((RESTART_COUNT + 1))
        LAST_RESTART=$now
        return 0
    else
        log "❌ Gateway-Neustart fehlgeschlagen!"
        RESTART_COUNT=$((RESTART_COUNT + 1))
        LAST_RESTART=$now
        return 1
    fi
}

# Main health check
do_health_check() {
    local status="OK"
    local issues=""

    # Check 1: Is gateway process running?
    if ! is_gateway_running; then
        issues="${issues}Gateway-Prozess nicht gefunden. "
        status="CRITICAL"
    fi

    # Check 2: Is port responding?
    if ! is_gateway_responsive; then
        issues="${issues}Port $GATEWAY_PORT antwortet nicht. "
        status="CRITICAL"
    fi

    # Check 3: Are logs fresh?
    if ! is_log_fresh; then
        issues="${issues}Logs sind veraltet (>5 Min). "
        if [[ "$status" != "CRITICAL" ]]; then
            status="WARNING"
        fi
    fi

    # Check 4: Any critical errors?
    local errors
    if ! errors=$(check_for_errors); then
        issues="${issues}Fehler in Logs: ${errors:0:100}. "
        status="WARNING"
    fi

    # Check 5: Stuck sessions?
    local stuck
    if ! stuck=$(check_stuck_sessions); then
        issues="${issues}$stuck. "
        if [[ "$status" != "CRITICAL" ]]; then
            status="WARNING"
        fi
    fi

    # Check 6: TUI health (only if TUI was running)
    local tui_status="OK"
    if is_tui_running; then
        if ! is_tui_connected; then
            issues="${issues}TUI läuft aber nicht verbunden. "
            tui_status="DISCONNECTED"
        fi
    fi

    # Take action based on status
    case "$status" in
        "OK")
            # Reset restart counter on healthy check
            if [[ $RESTART_COUNT -gt 0 ]]; then
                local now=$(date +%s)
                if [[ $((now - LAST_RESTART)) -gt 300 ]]; then
                    RESTART_COUNT=0
                fi
            fi
            ;;
        "WARNING")
            log "⚠️  Warning: $issues"
            ;;
        "CRITICAL")
            log "🚨 Critical: $issues"
            restart_gateway
            # Also restart TUI after gateway restart
            sleep 3
            if is_tui_running; then
                restart_tui
            fi
            ;;
    esac

    # Handle TUI issues - notify instead of auto-restart (TUI needs proper terminal)
    if [[ "$tui_status" == "DISCONNECTED" ]]; then
        log "🖥️  TUI nicht verbunden - bitte manuell starten: ~/Desktop/Start-TUI.command"
        # Send macOS notification
        osascript -e 'display notification "TUI disconnected - bitte manuell starten" with title "OpenClaw Monitor"' 2>/dev/null || true
    fi

    echo "$status"
}

# Status display
show_status() {
    echo "=== OpenClaw Watchdog Status ==="
    echo ""

    # Watchdog running?
    if [[ -f "$WATCHDOG_PID" ]] && kill -0 "$(cat "$WATCHDOG_PID")" 2>/dev/null; then
        echo "Watchdog:  🟢 Running (PID: $(cat "$WATCHDOG_PID"))"
    else
        echo "Watchdog:  🔴 Not running"
    fi

    # Gateway running?
    if is_gateway_running; then
        local pid=$(pgrep -f "openclaw-gateway" | head -1)
        echo "Gateway:   🟢 Running (PID: $pid)"
    else
        echo "Gateway:   🔴 Not running"
    fi

    # Port responding?
    if is_gateway_responsive; then
        echo "Port:      🟢 $GATEWAY_PORT responding"
    else
        echo "Port:      🔴 $GATEWAY_PORT not responding"
    fi

    # Logs fresh?
    if is_log_fresh; then
        echo "Logs:      🟢 Fresh"
    else
        echo "Logs:      🟡 Stale (>5 min)"
    fi

    # Recent errors?
    if check_for_errors >/dev/null 2>&1; then
        echo "Errors:    🟢 None recent"
    else
        echo "Errors:    🟡 Found in logs"
    fi

    # TUI status
    if is_tui_running; then
        local tui_pid=$(get_tui_pid)
        if is_tui_connected; then
            echo "TUI:       🟢 Running (PID: $tui_pid, connected)"
        else
            echo "TUI:       🟡 Running (PID: $tui_pid, disconnected)"
        fi
    else
        echo "TUI:       ⚪ Not running"
    fi

    echo ""
    echo "Log: $WATCHDOG_LOG"
}

# Post-wake recovery check
do_wake_recovery() {
    log "😴→🌅 Wake detected! Running recovery check..."

    # Give system a moment to restore network
    sleep 3

    # Check gateway status
    if ! is_gateway_running; then
        log "🔄 Gateway not running after wake - starting..."
        restart_gateway
        return
    fi

    if ! is_gateway_responsive; then
        log "🔄 Gateway not responsive after wake - restarting..."
        restart_gateway
        return
    fi

    # Check if connections need time to reconnect
    sleep 5

    # Final health check
    local status=$(do_health_check)
    if [[ "$status" == "OK" ]]; then
        log "✅ Wake recovery complete - all systems OK"
    else
        log "⚠️  Wake recovery: status=$status - monitoring..."
    fi
}

# Run as daemon
run_daemon() {
    ensure_log_dir

    # Check if already running
    if [[ -f "$WATCHDOG_PID" ]] && kill -0 "$(cat "$WATCHDOG_PID")" 2>/dev/null; then
        echo "Watchdog already running (PID: $(cat "$WATCHDOG_PID"))"
        exit 1
    fi

    # Write PID
    echo $$ > "$WATCHDOG_PID"
    log "🐕 Watchdog gestartet (PID: $$, Interval: ${CHECK_INTERVAL}s)"

    # Trap for cleanup
    trap 'log "🛑 Watchdog gestoppt"; rm -f "$WATCHDOG_PID"; exit 0' SIGTERM SIGINT

    # Initialize last check time
    LAST_CHECK_TIME=$(date +%s)

    # Main loop
    while true; do
        local now=$(date +%s)
        local time_since_last=$((now - LAST_CHECK_TIME))

        # Detect wake from sleep (gap much larger than expected)
        if [[ $LAST_CHECK_TIME -gt 0 ]] && [[ $time_since_last -gt $WAKE_THRESHOLD ]]; then
            log "⏰ Time gap detected: ${time_since_last}s (expected ~${CHECK_INTERVAL}s)"
            do_wake_recovery
        else
            do_health_check >/dev/null
        fi

        LAST_CHECK_TIME=$(date +%s)
        sleep "$CHECK_INTERVAL"
    done
}

# Stop daemon
stop_daemon() {
    if [[ -f "$WATCHDOG_PID" ]]; then
        local pid=$(cat "$WATCHDOG_PID")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            rm -f "$WATCHDOG_PID"
            echo "Watchdog stopped (was PID: $pid)"
        else
            rm -f "$WATCHDOG_PID"
            echo "Watchdog was not running (stale PID file removed)"
        fi
    else
        echo "Watchdog is not running"
    fi
}

# === MAIN ===

ensure_log_dir

case "${1:-status}" in
    start)
        echo "Starting watchdog in background..."
        nohup "$0" daemon >> "$WATCHDOG_LOG" 2>&1 &
        sleep 1
        show_status
        ;;
    daemon)
        run_daemon
        ;;
    stop)
        stop_daemon
        ;;
    status)
        show_status
        ;;
    check)
        # Single check (for cron)
        result=$(do_health_check)
        echo "Health: $result"
        ;;
    restart-gateway)
        restart_gateway
        ;;
    restart-tui)
        restart_tui
        ;;
    restart-all)
        echo "Restarting Gateway and TUI..."
        restart_gateway
        sleep 3
        restart_tui
        ;;
    *)
        echo "Usage: $0 {start|stop|status|check|restart-gateway|restart-tui|restart-all}"
        exit 1
        ;;
esac
