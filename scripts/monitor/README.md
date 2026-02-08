# OpenClaw Monitor

A cross-platform GUI application for monitoring and managing OpenClaw Gateway and TUI.

![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## Features

- **Real-time Monitoring**: Track Gateway, TUI, and port status
- **Cross-Platform**: Works on macOS, Windows, and Linux
- **Multi-Language**: English, Deutsch, Français, Italiano, Español
- **AI Model Selection**: Switch between Claude, Groq, and OpenAI models
- **Watchdog Mode**: Automatic restart on failures (macOS/Linux)
- **Update Management**: Check for updates with AI-powered security scanning
- **Wake Detection**: Auto-recovery after system sleep (macOS)

## Screenshots

```
┌─────────────────────────────────────────┐
│        🐾 OpenClaw Monitor              │
│  Platform: Darwin    Language: [DE ▼]  │
├─────────────────────────────────────────┤
│  Status                                 │
│  🟢 Watchdog      Running               │
│  🟢 Gateway       Running               │
│  🟢 Port 18789    Responding            │
│  🟢 TUI           Connected             │
│  🟢 Logs          Fresh                 │
│  🟢 Updates       Up to date            │
├─────────────────────────────────────────┤
│  AI Model                               │
│  [Claude Opus 4.5 (Best) ▼] [Apply]     │
├─────────────────────────────────────────┤
│  Watchdog Auto-Mode                     │
│  Automatic Monitoring           [ON]    │
├─────────────────────────────────────────┤
│  Manual Control                         │
│  [🔄 Gateway] [🖥️ TUI] [⚡ All]         │
├─────────────────────────────────────────┤
│  Software Update                        │
│  [🔍 Check]  [⬇️ Install]               │
└─────────────────────────────────────────┘
```

## Installation

### Requirements

- Python 3.8 or higher
- Tkinter (usually included with Python)
- OpenClaw installed and configured

### Quick Start

```bash
# Copy to your OpenClaw scripts directory
mkdir -p ~/.openclaw/scripts
cp openclaw-monitor.py ~/.openclaw/scripts/
cp watchdog.sh ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/watchdog.sh

# Run the monitor
python3 ~/.openclaw/scripts/openclaw-monitor.py
```

### macOS App Bundle (Optional)

Create a clickable app:

```bash
# Create app structure
mkdir -p ~/Applications/OpenClaw\ Monitor.app/Contents/MacOS
mkdir -p ~/Applications/OpenClaw\ Monitor.app/Contents/Resources

# Create launcher script
cat > ~/Applications/OpenClaw\ Monitor.app/Contents/MacOS/OpenClaw\ Monitor << 'EOF'
#!/bin/bash
cd ~/.openclaw/scripts
exec python3 openclaw-monitor.py
EOF
chmod +x ~/Applications/OpenClaw\ Monitor.app/Contents/MacOS/OpenClaw\ Monitor

# Create Info.plist
cat > ~/Applications/OpenClaw\ Monitor.app/Contents/Info.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>OpenClaw Monitor</string>
    <key>CFBundleIdentifier</key>
    <string>com.openclaw.monitor</string>
    <key>CFBundleName</key>
    <string>OpenClaw Monitor</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF
```

## Configuration

### Environment Variables

| Variable       | Description                     | Default       |
| -------------- | ------------------------------- | ------------- |
| `OPENCLAW_DIR` | OpenClaw installation directory | Auto-detected |

### Config Files

The monitor stores its settings in `~/.openclaw/`:

- `monitor-config.json` - Language preference
- `openclaw.json` - OpenClaw configuration (model selection)
- `last-update-check.json` - Update check timestamp

## Components

### openclaw-monitor.py

The main GUI application with:

- **Status Panel**: Real-time component status
- **Model Selector**: Switch AI models on-the-fly
- **Watchdog Toggle**: Enable/disable automatic monitoring
- **Manual Controls**: Restart Gateway, TUI, or both
- **Update Manager**: Check and install updates with security scanning

### watchdog.sh (macOS/Linux)

Background daemon for automatic recovery:

```bash
# Start watchdog
~/.openclaw/scripts/watchdog.sh start

# Stop watchdog
~/.openclaw/scripts/watchdog.sh stop

# Check status
~/.openclaw/scripts/watchdog.sh status

# Single health check
~/.openclaw/scripts/watchdog.sh check
```

Features:

- Monitors Gateway and TUI health every 30 seconds
- Auto-restarts failed components
- Detects wake-from-sleep and performs recovery
- Cooldown protection (max 3 restarts per 10 minutes)

## Security Scanning

The update checker includes AI-powered security scanning:

### Dangerous Patterns (Always Flagged)

- `curl | sh`, `wget | sh` - Remote code execution
- `nc -e`, `/dev/tcp` - Reverse shells
- `rm -rf /` - Destructive commands
- Fork bombs

### Normal CLI Patterns (Ignored)

- `child_process`, `exec()`, `spawn()` - Required for CLI operation

### AI Analysis

When dangerous patterns are detected, the monitor:

1. Sends the diff to the configured AI model
2. Receives a verdict: SAFE / REVIEW / DANGEROUS
3. Displays the result with explanation

## Supported AI Models

| Provider  | Model           | Description       |
| --------- | --------------- | ----------------- |
| Anthropic | claude-opus-4-5 | Best quality      |
| Anthropic | claude-sonnet-4 | Fast & capable    |
| Anthropic | claude-haiku-3  | Fastest           |
| Groq      | llama-3.3-70b   | Open source, fast |
| Groq      | llama-3.1-8b    | Ultra-fast        |
| OpenAI    | gpt-4o          | GPT-4 Omni        |
| OpenAI    | gpt-4o-mini     | Fast & affordable |

## Troubleshooting

### Monitor doesn't start

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check Tkinter
python3 -c "import tkinter; print('OK')"

# Run with debug output
python3 ~/.openclaw/scripts/openclaw-monitor.py
```

### Gateway won't restart

```bash
# Manual restart
pkill -f openclaw-gateway
cd ~/clawdbot && pnpm openclaw gateway run
```

### TUI shows "(no output)"

```bash
# Restart TUI
pkill -f "openclaw.*tui"
cd ~/clawdbot && pnpm openclaw tui
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See [LICENSE](../../LICENSE) for details.

---

🤖 Built with Claude Code
