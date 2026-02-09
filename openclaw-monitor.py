#!/usr/bin/env python3
"""
OpenClaw Monitor - GUI for Gateway & TUI Monitoring
Cross-platform: macOS, Windows, Linux
Multi-language: DE, EN, FR, IT, ES

Author: Community Contribution
License: MIT
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import time
import os
import sys
import json
import platform
from pathlib import Path
from datetime import datetime

# === TRANSLATIONS ===
TRANSLATIONS = {
    "en": {
        "title": "OpenClaw Monitor",
        "platform": "Platform",
        "status": "Status",
        "watchdog": "Watchdog",
        "gateway": "Gateway",
        "port": "Port 18789",
        "tui": "TUI",
        "logs": "Logs",
        "updates": "Updates",
        "running": "Running",
        "stopped": "Stopped",
        "responding": "Responding",
        "not_responding": "Not responding",
        "connected": "Connected",
        "disconnected": "Disconnected",
        "not_running": "Not running",
        "fresh": "Fresh",
        "stale": "Stale (>5min)",
        "warning": "Warning",
        "available": "Available",
        "current": "Up to date",
        "not_checked": "Not checked",
        "ai_model": "AI Model",
        "apply": "Apply",
        "model_changed": "Model changed",
        "model_changed_msg": "Model changed to {model}.\n\nRestart Gateway now?",
        "config_error": "Error saving model configuration",
        "watchdog_auto": "Watchdog Auto-Mode",
        "auto_monitoring": "Automatic Monitoring",
        "on": "ON",
        "off": "OFF",
        "manual_control": "Manual Control",
        "restart_gateway": "Gateway",
        "restart_tui": "TUI",
        "restart_all": "All",
        "software_update": "Software Update",
        "check": "Check",
        "install": "Install",
        "events": "Events",
        "updated_at": "Updated",
        "starting_watchdog": "Starting watchdog...",
        "stopping_watchdog": "Stopping watchdog...",
        "watchdog_started": "Watchdog started",
        "watchdog_stopped": "Watchdog stopped",
        "watchdog_not_available": "Watchdog not available on Windows",
        "restarting_gateway": "Restarting Gateway...",
        "gateway_restart_complete": "Gateway restart complete",
        "restarting_tui": "Restarting TUI...",
        "tui_restart_complete": "TUI restart complete",
        "restarting_all": "Restarting all...",
        "full_restart_complete": "Full restart complete",
        "checking_updates": "Checking for updates...",
        "security_warning": "Security Warning",
        "suspicious_patterns": "Suspicious patterns found!\n\n",
        "continue_anyway": "\nContinue anyway?",
        "update_cancelled": "Update cancelled",
        "installing_updates": "Installing updates...",
        "update_installed": "Update installed!",
        "update_failed": "Update failed",
        "openclaw_current": "OpenClaw is up to date",
        "security_update": "SECURITY UPDATE!",
        "commits_behind": "commits behind",
        "security_scan_ok": "Security scan OK",
        "files": "files",
        "suspicious_files": "Suspicious patterns in",
        "gateway_restart_required": "Gateway restart required!",
        "language": "Language",
        "ai_analyzing": "AI is analyzing changes...",
        "ai_analysis_ok": "AI Analysis: No security issues found",
        "ai_analysis_warning": "AI Analysis: Potential issues found",
        "ai_analysis_failed": "AI Analysis: Could not complete (Gateway offline?)",
        "ai_verdict": "AI Verdict",
        "safe": "SAFE",
        "review_recommended": "REVIEW RECOMMENDED",
        "potentially_dangerous": "POTENTIALLY DANGEROUS",
        "version": "Version",
        "last_update": "Last check",
        "ignore": "Ignore",
        "update_ignored": "Update ignored",
        "advanced": "Advanced",
        "show_more": "Show more",
        "show_less": "Show less",
        "notifications": "Notifications",
        "gateway_down": "Gateway offline",
        "high_cost": "High cost",
        "security_alert": "Security alert",
        "ai_update_check": "AI Check",
        "ai_checking": "AI analyzing...",
        "recheck_ai": "Re-check",
        "bots": "Bots",
        "add_bot": "Add",
        "all_bots_status": "All Bots",
        "usage_stats": "Usage & Costs",
        "tokens_today": "Tokens today",
        "cost_today": "Cost today",
        "reset": "Reset",
        "total": "Total",
    },
    "de": {
        "title": "OpenClaw Monitor",
        "platform": "Plattform",
        "status": "Status",
        "watchdog": "Watchdog",
        "gateway": "Gateway",
        "port": "Port 18789",
        "tui": "TUI",
        "logs": "Logs",
        "updates": "Updates",
        "running": "Läuft",
        "stopped": "Gestoppt",
        "responding": "Antwortet",
        "not_responding": "Keine Antwort",
        "connected": "Verbunden",
        "disconnected": "Getrennt",
        "not_running": "Nicht aktiv",
        "fresh": "Aktuell",
        "stale": "Veraltet (>5min)",
        "warning": "Warnung",
        "available": "Verfügbar",
        "current": "Aktuell",
        "not_checked": "Nicht geprüft",
        "ai_model": "KI-Modell",
        "apply": "Anwenden",
        "model_changed": "Modell geändert",
        "model_changed_msg": "Modell auf {model} geändert.\n\nGateway jetzt neu starten?",
        "config_error": "Fehler beim Speichern der Modell-Konfiguration",
        "watchdog_auto": "Watchdog Auto-Modus",
        "auto_monitoring": "Automatische Überwachung",
        "on": "AN",
        "off": "AUS",
        "manual_control": "Manuelle Steuerung",
        "restart_gateway": "Gateway",
        "restart_tui": "TUI",
        "restart_all": "Alle",
        "software_update": "Software Update",
        "check": "Prüfen",
        "install": "Installieren",
        "events": "Ereignisse",
        "updated_at": "Aktualisiert",
        "starting_watchdog": "Starte Watchdog...",
        "stopping_watchdog": "Stoppe Watchdog...",
        "watchdog_started": "Watchdog gestartet",
        "watchdog_stopped": "Watchdog gestoppt",
        "watchdog_not_available": "Watchdog nicht verfügbar auf Windows",
        "restarting_gateway": "Gateway wird neugestartet...",
        "gateway_restart_complete": "Gateway-Neustart abgeschlossen",
        "restarting_tui": "TUI wird neugestartet...",
        "tui_restart_complete": "TUI-Neustart abgeschlossen",
        "restarting_all": "Alles wird neugestartet...",
        "full_restart_complete": "Vollständiger Neustart abgeschlossen",
        "checking_updates": "Prüfe auf Updates...",
        "security_warning": "Sicherheitswarnung",
        "suspicious_patterns": "Verdächtige Patterns gefunden!\n\n",
        "continue_anyway": "\nTrotzdem fortfahren?",
        "update_cancelled": "Update abgebrochen",
        "installing_updates": "Installiere Updates...",
        "update_installed": "Update installiert!",
        "update_failed": "Update fehlgeschlagen",
        "openclaw_current": "OpenClaw ist aktuell",
        "security_update": "SICHERHEITS-UPDATE!",
        "commits_behind": "Commits zurück",
        "security_scan_ok": "Sicherheits-Scan OK",
        "files": "Dateien",
        "suspicious_files": "Verdächtige Patterns in",
        "gateway_restart_required": "Gateway-Neustart erforderlich!",
        "language": "Sprache",
        "ai_analyzing": "KI analysiert Änderungen...",
        "ai_analysis_ok": "KI-Analyse: Keine Sicherheitsprobleme gefunden",
        "ai_analysis_warning": "KI-Analyse: Mögliche Probleme gefunden",
        "ai_analysis_failed": "KI-Analyse: Konnte nicht abgeschlossen werden (Gateway offline?)",
        "ai_verdict": "KI-Bewertung",
        "safe": "SICHER",
        "review_recommended": "PRÜFUNG EMPFOHLEN",
        "potentially_dangerous": "POTENZIELL GEFÄHRLICH",
        "version": "Version",
        "last_update": "Letzte Prüfung",
        "ignore": "Ignorieren",
        "update_ignored": "Update ignoriert",
        "advanced": "Erweitert",
        "show_more": "Mehr anzeigen",
        "show_less": "Weniger anzeigen",
        "notifications": "Benachrichtigungen",
        "gateway_down": "Gateway offline",
        "high_cost": "Hohe Kosten",
        "security_alert": "Sicherheitsalarm",
        "ai_update_check": "KI-Prüfung",
        "ai_checking": "KI analysiert...",
        "recheck_ai": "Nochmal",
        "bots": "Bots",
        "add_bot": "Hinzufügen",
        "all_bots_status": "Alle Bots",
        "usage_stats": "Nutzung & Kosten",
        "tokens_today": "Tokens heute",
        "cost_today": "Kosten heute",
        "reset": "Reset",
        "total": "Gesamt",
    },
    "fr": {
        "title": "OpenClaw Monitor",
        "platform": "Plateforme",
        "status": "État",
        "watchdog": "Watchdog",
        "gateway": "Gateway",
        "port": "Port 18789",
        "tui": "TUI",
        "logs": "Logs",
        "updates": "Mises à jour",
        "running": "En cours",
        "stopped": "Arrêté",
        "responding": "Répond",
        "not_responding": "Ne répond pas",
        "connected": "Connecté",
        "disconnected": "Déconnecté",
        "not_running": "Inactif",
        "fresh": "Récent",
        "stale": "Périmé (>5min)",
        "warning": "Attention",
        "available": "Disponible",
        "current": "À jour",
        "not_checked": "Non vérifié",
        "ai_model": "Modèle IA",
        "apply": "Appliquer",
        "model_changed": "Modèle changé",
        "model_changed_msg": "Modèle changé en {model}.\n\nRedémarrer Gateway maintenant?",
        "config_error": "Erreur lors de l'enregistrement de la configuration",
        "watchdog_auto": "Mode Auto Watchdog",
        "auto_monitoring": "Surveillance automatique",
        "on": "ON",
        "off": "OFF",
        "manual_control": "Contrôle manuel",
        "restart_gateway": "Gateway",
        "restart_tui": "TUI",
        "restart_all": "Tout",
        "software_update": "Mise à jour",
        "check": "Vérifier",
        "install": "Installer",
        "events": "Événements",
        "updated_at": "Mis à jour",
        "starting_watchdog": "Démarrage du watchdog...",
        "stopping_watchdog": "Arrêt du watchdog...",
        "watchdog_started": "Watchdog démarré",
        "watchdog_stopped": "Watchdog arrêté",
        "watchdog_not_available": "Watchdog non disponible sur Windows",
        "restarting_gateway": "Redémarrage du Gateway...",
        "gateway_restart_complete": "Redémarrage Gateway terminé",
        "restarting_tui": "Redémarrage du TUI...",
        "tui_restart_complete": "Redémarrage TUI terminé",
        "restarting_all": "Redémarrage de tout...",
        "full_restart_complete": "Redémarrage complet terminé",
        "checking_updates": "Vérification des mises à jour...",
        "security_warning": "Avertissement de sécurité",
        "suspicious_patterns": "Patterns suspects trouvés!\n\n",
        "continue_anyway": "\nContinuer quand même?",
        "update_cancelled": "Mise à jour annulée",
        "installing_updates": "Installation des mises à jour...",
        "update_installed": "Mise à jour installée!",
        "update_failed": "Mise à jour échouée",
        "openclaw_current": "OpenClaw est à jour",
        "security_update": "MISE À JOUR DE SÉCURITÉ!",
        "commits_behind": "commits en retard",
        "security_scan_ok": "Scan de sécurité OK",
        "files": "fichiers",
        "suspicious_files": "Patterns suspects dans",
        "gateway_restart_required": "Redémarrage Gateway requis!",
        "language": "Langue",
        "ai_analyzing": "L'IA analyse les changements...",
        "ai_analysis_ok": "Analyse IA: Aucun problème de sécurité",
        "ai_analysis_warning": "Analyse IA: Problèmes potentiels détectés",
        "ai_analysis_failed": "Analyse IA: Échec (Gateway hors ligne?)",
        "ai_verdict": "Verdict IA",
        "safe": "SÛR",
        "review_recommended": "RÉVISION RECOMMANDÉE",
        "potentially_dangerous": "POTENTIELLEMENT DANGEREUX",
        "version": "Version",
        "last_update": "Dernière vérif.",
        "ignore": "Ignorer",
        "update_ignored": "Mise à jour ignorée",
        "advanced": "Avancé",
        "show_more": "Afficher plus",
        "show_less": "Afficher moins",
        "notifications": "Notifications",
        "gateway_down": "Gateway hors ligne",
        "high_cost": "Coût élevé",
        "security_alert": "Alerte sécurité",
        "ai_update_check": "Vérif. IA",
        "ai_checking": "IA en analyse...",
        "recheck_ai": "Revérifier",
        "bots": "Bots",
        "add_bot": "Ajouter",
        "all_bots_status": "Tous les Bots",
        "usage_stats": "Utilisation & Coûts",
        "tokens_today": "Tokens aujourd'hui",
        "cost_today": "Coût aujourd'hui",
        "reset": "Réinitialiser",
        "total": "Total",
    },
    "it": {
        "title": "OpenClaw Monitor",
        "platform": "Piattaforma",
        "status": "Stato",
        "watchdog": "Watchdog",
        "gateway": "Gateway",
        "port": "Porta 18789",
        "tui": "TUI",
        "logs": "Log",
        "updates": "Aggiornamenti",
        "running": "In esecuzione",
        "stopped": "Fermato",
        "responding": "Risponde",
        "not_responding": "Non risponde",
        "connected": "Connesso",
        "disconnected": "Disconnesso",
        "not_running": "Non attivo",
        "fresh": "Recente",
        "stale": "Obsoleto (>5min)",
        "warning": "Attenzione",
        "available": "Disponibile",
        "current": "Aggiornato",
        "not_checked": "Non verificato",
        "ai_model": "Modello IA",
        "apply": "Applica",
        "model_changed": "Modello cambiato",
        "model_changed_msg": "Modello cambiato in {model}.\n\nRiavviare Gateway adesso?",
        "config_error": "Errore nel salvare la configurazione",
        "watchdog_auto": "Modalità Auto Watchdog",
        "auto_monitoring": "Monitoraggio automatico",
        "on": "ON",
        "off": "OFF",
        "manual_control": "Controllo manuale",
        "restart_gateway": "Gateway",
        "restart_tui": "TUI",
        "restart_all": "Tutti",
        "software_update": "Aggiornamento",
        "check": "Verifica",
        "install": "Installa",
        "events": "Eventi",
        "updated_at": "Aggiornato",
        "starting_watchdog": "Avvio watchdog...",
        "stopping_watchdog": "Arresto watchdog...",
        "watchdog_started": "Watchdog avviato",
        "watchdog_stopped": "Watchdog arrestato",
        "watchdog_not_available": "Watchdog non disponibile su Windows",
        "restarting_gateway": "Riavvio Gateway...",
        "gateway_restart_complete": "Riavvio Gateway completato",
        "restarting_tui": "Riavvio TUI...",
        "tui_restart_complete": "Riavvio TUI completato",
        "restarting_all": "Riavvio di tutto...",
        "full_restart_complete": "Riavvio completo completato",
        "checking_updates": "Verifica aggiornamenti...",
        "security_warning": "Avviso di sicurezza",
        "suspicious_patterns": "Pattern sospetti trovati!\n\n",
        "continue_anyway": "\nContinuare comunque?",
        "update_cancelled": "Aggiornamento annullato",
        "installing_updates": "Installazione aggiornamenti...",
        "update_installed": "Aggiornamento installato!",
        "update_failed": "Aggiornamento fallito",
        "openclaw_current": "OpenClaw è aggiornato",
        "security_update": "AGGIORNAMENTO DI SICUREZZA!",
        "commits_behind": "commit indietro",
        "security_scan_ok": "Scansione sicurezza OK",
        "files": "file",
        "suspicious_files": "Pattern sospetti in",
        "gateway_restart_required": "Riavvio Gateway richiesto!",
        "language": "Lingua",
        "ai_analyzing": "L'IA sta analizzando le modifiche...",
        "ai_analysis_ok": "Analisi IA: Nessun problema di sicurezza",
        "ai_analysis_warning": "Analisi IA: Potenziali problemi rilevati",
        "ai_analysis_failed": "Analisi IA: Non completata (Gateway offline?)",
        "ai_verdict": "Verdetto IA",
        "safe": "SICURO",
        "review_recommended": "REVISIONE CONSIGLIATA",
        "potentially_dangerous": "POTENZIALMENTE PERICOLOSO",
        "version": "Versione",
        "last_update": "Ultimo controllo",
        "ignore": "Ignora",
        "update_ignored": "Aggiornamento ignorato",
        "advanced": "Avanzate",
        "show_more": "Mostra più",
        "show_less": "Mostra meno",
        "notifications": "Notifiche",
        "gateway_down": "Gateway offline",
        "high_cost": "Costo elevato",
        "security_alert": "Allarme sicurezza",
        "ai_update_check": "Controllo IA",
        "ai_checking": "IA in analisi...",
        "recheck_ai": "Ricontrolla",
        "bots": "Bot",
        "add_bot": "Aggiungi",
        "all_bots_status": "Tutti i Bot",
        "usage_stats": "Utilizzo & Costi",
        "tokens_today": "Token oggi",
        "cost_today": "Costo oggi",
        "reset": "Azzera",
        "total": "Totale",
    },
    "es": {
        "title": "OpenClaw Monitor",
        "platform": "Plataforma",
        "status": "Estado",
        "watchdog": "Watchdog",
        "gateway": "Gateway",
        "port": "Puerto 18789",
        "tui": "TUI",
        "logs": "Logs",
        "updates": "Actualizaciones",
        "running": "Ejecutando",
        "stopped": "Detenido",
        "responding": "Respondiendo",
        "not_responding": "Sin respuesta",
        "connected": "Conectado",
        "disconnected": "Desconectado",
        "not_running": "Inactivo",
        "fresh": "Reciente",
        "stale": "Obsoleto (>5min)",
        "warning": "Advertencia",
        "available": "Disponible",
        "current": "Actualizado",
        "not_checked": "No verificado",
        "ai_model": "Modelo IA",
        "apply": "Aplicar",
        "model_changed": "Modelo cambiado",
        "model_changed_msg": "Modelo cambiado a {model}.\n\n¿Reiniciar Gateway ahora?",
        "config_error": "Error al guardar la configuración",
        "watchdog_auto": "Modo Auto Watchdog",
        "auto_monitoring": "Monitoreo automático",
        "on": "ON",
        "off": "OFF",
        "manual_control": "Control manual",
        "restart_gateway": "Gateway",
        "restart_tui": "TUI",
        "restart_all": "Todo",
        "software_update": "Actualización",
        "check": "Verificar",
        "install": "Instalar",
        "events": "Eventos",
        "updated_at": "Actualizado",
        "starting_watchdog": "Iniciando watchdog...",
        "stopping_watchdog": "Deteniendo watchdog...",
        "watchdog_started": "Watchdog iniciado",
        "watchdog_stopped": "Watchdog detenido",
        "watchdog_not_available": "Watchdog no disponible en Windows",
        "restarting_gateway": "Reiniciando Gateway...",
        "gateway_restart_complete": "Reinicio Gateway completado",
        "restarting_tui": "Reiniciando TUI...",
        "tui_restart_complete": "Reinicio TUI completado",
        "restarting_all": "Reiniciando todo...",
        "full_restart_complete": "Reinicio completo completado",
        "checking_updates": "Verificando actualizaciones...",
        "security_warning": "Advertencia de seguridad",
        "suspicious_patterns": "¡Patrones sospechosos encontrados!\n\n",
        "continue_anyway": "\n¿Continuar de todos modos?",
        "update_cancelled": "Actualización cancelada",
        "installing_updates": "Instalando actualizaciones...",
        "update_installed": "¡Actualización instalada!",
        "update_failed": "Actualización fallida",
        "openclaw_current": "OpenClaw está actualizado",
        "security_update": "¡ACTUALIZACIÓN DE SEGURIDAD!",
        "commits_behind": "commits atrás",
        "security_scan_ok": "Escaneo de seguridad OK",
        "files": "archivos",
        "suspicious_files": "Patrones sospechosos en",
        "gateway_restart_required": "¡Reinicio de Gateway requerido!",
        "language": "Idioma",
        "ai_analyzing": "La IA está analizando los cambios...",
        "ai_analysis_ok": "Análisis IA: Sin problemas de seguridad",
        "ai_analysis_warning": "Análisis IA: Posibles problemas detectados",
        "ai_analysis_failed": "Análisis IA: No completado (¿Gateway offline?)",
        "ai_verdict": "Veredicto IA",
        "safe": "SEGURO",
        "review_recommended": "REVISIÓN RECOMENDADA",
        "potentially_dangerous": "POTENCIALMENTE PELIGROSO",
        "version": "Versión",
        "last_update": "Última verif.",
        "ignore": "Ignorar",
        "update_ignored": "Actualización ignorada",
        "advanced": "Avanzado",
        "show_more": "Mostrar más",
        "show_less": "Mostrar menos",
        "notifications": "Notificaciones",
        "gateway_down": "Gateway offline",
        "high_cost": "Costo alto",
        "security_alert": "Alerta seguridad",
        "ai_update_check": "Verificación IA",
        "ai_checking": "IA analizando...",
        "recheck_ai": "Revisar",
        "bots": "Bots",
        "add_bot": "Añadir",
        "all_bots_status": "Todos los Bots",
        "usage_stats": "Uso y Costos",
        "tokens_today": "Tokens hoy",
        "cost_today": "Costo hoy",
        "reset": "Reiniciar",
        "total": "Total",
    },
}

LANGUAGE_NAMES = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "it": "Italiano",
    "es": "Español",
}


class OpenClawMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OpenClaw Monitor")
        self.root.geometry("450x500")
        self.root.resizable(True, True)
        self.root.minsize(400, 400)

        # Detect platform
        self.platform = platform.system().lower()  # 'darwin', 'windows', 'linux'
        self.is_mac = self.platform == 'darwin'
        self.is_windows = self.platform == 'windows'
        self.is_linux = self.platform == 'linux'

        # Dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.success_color = "#4caf50"
        self.warning_color = "#ff9800"
        self.error_color = "#f44336"
        self.neutral_color = "#666666"

        self.root.configure(bg=self.bg_color)

        # State
        self.running = True
        self.watchdog_auto = tk.BooleanVar(value=False)
        self.advanced_expanded = tk.BooleanVar(value=False)
        self.update_available = False
        self.last_update_check = None
        self.update_info = ""

        # Usage tracking
        self.tokens_today = 0
        self.cost_today = 0.0
        self.usage_by_model = {}
        self.current_model = tk.StringVar()
        self.current_lang = tk.StringVar(value="en")

        # Cross-platform paths
        self.home_dir = Path.home()
        self.openclaw_config_dir = self.home_dir / ".openclaw"
        self.openclaw_dir = self._find_openclaw_dir()
        self.config_file = self.openclaw_config_dir / "openclaw.json"
        self.watchdog_script = self.openclaw_config_dir / "scripts" / "watchdog.sh"
        self.update_check_file = self.openclaw_config_dir / "last-update-check.json"
        self.monitor_config_file = self.openclaw_config_dir / "monitor-config.json"

        # Available models
        self.available_models = [
            ("anthropic/claude-opus-4-5", "Claude Opus 4.5 (Best)"),
            ("anthropic/claude-sonnet-4", "Claude Sonnet 4 (Fast)"),
            ("anthropic/claude-haiku-3", "Claude Haiku 3 (Fastest)"),
            ("groq/llama-3.3-70b-versatile", "Llama 3.3 70B (Groq)"),
            ("groq/llama-3.1-8b-instant", "Llama 3.1 8B (Groq Fast)"),
            ("openai/gpt-4o", "GPT-4o (OpenAI)"),
            ("openai/gpt-4o-mini", "GPT-4o Mini (OpenAI)"),
        ]

        # Load configs
        self.load_monitor_config()
        self.load_config()

        self.setup_ui()
        self.initialize_advanced_visibility()
        self.load_usage_stats()
        self.update_usage_display()
        self.start_monitoring()

    def t(self, key):
        """Get translation for current language"""
        lang = self.current_lang.get()
        return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

    def _find_openclaw_dir(self):
        """Find the OpenClaw installation directory"""
        # Common locations to check
        possible_paths = [
            self.home_dir / "clawdbot",
            self.home_dir / "openclaw",
            self.home_dir / "OpenClaw",
            Path("/opt/openclaw"),
            Path("/usr/local/openclaw"),
        ]

        # Check environment variable first
        env_path = os.environ.get("OPENCLAW_DIR")
        if env_path:
            return Path(env_path)

        # Check common locations
        for path in possible_paths:
            if path.exists() and (path / "package.json").exists():
                return path

        # Default fallback
        return self.home_dir / "clawdbot"

    def load_monitor_config(self):
        """Load monitor-specific configuration (language, etc.)"""
        try:
            if self.monitor_config_file.exists():
                with open(self.monitor_config_file, 'r') as f:
                    config = json.load(f)
                    self.current_lang.set(config.get("language", "en"))
                    self.advanced_expanded.set(config.get("advanced_expanded", False))
            else:
                # Try to detect system language
                import locale
                sys_lang = locale.getdefaultlocale()[0] or "en"
                lang_code = sys_lang[:2].lower()
                if lang_code in TRANSLATIONS:
                    self.current_lang.set(lang_code)
                else:
                    self.current_lang.set("en")
        except Exception:
            self.current_lang.set("en")

    def save_monitor_config(self):
        """Save monitor-specific configuration"""
        try:
            self.monitor_config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.monitor_config_file, 'w') as f:
                json.dump({
                    "language": self.current_lang.get(),
                    "advanced_expanded": self.advanced_expanded.get()
                }, f, indent=2)
        except Exception:
            pass

    def load_config(self):
        """Load OpenClaw configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                    # Get current model
                    model = self.config.get("agents", {}).get("defaults", {}).get("model", {})
                    if isinstance(model, dict):
                        self.current_model.set(model.get("primary", "anthropic/claude-opus-4-5"))
                    else:
                        self.current_model.set(model or "anthropic/claude-opus-4-5")
            else:
                self.config = {}
                self.current_model.set("anthropic/claude-opus-4-5")
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
            self.current_model.set("anthropic/claude-opus-4-5")

    def save_model_config(self, model_id):
        """Save selected model to config"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}

            # Ensure nested structure exists
            if "agents" not in config:
                config["agents"] = {}
            if "defaults" not in config["agents"]:
                config["agents"]["defaults"] = {}
            if "model" not in config["agents"]["defaults"]:
                config["agents"]["defaults"]["model"] = {}

            # Update model
            if isinstance(config["agents"]["defaults"]["model"], dict):
                config["agents"]["defaults"]["model"]["primary"] = model_id
            else:
                config["agents"]["defaults"]["model"] = {"primary": model_id}

            # Save
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def setup_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.bg_color, padx=15, pady=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = tk.Label(self.main_frame, text="🐾 OpenClaw Monitor",
                                    font=("Helvetica", 18, "bold"),
                                    bg=self.bg_color, fg=self.fg_color)
        self.title_label.pack(pady=(0, 5))

        # Language selector row
        lang_row = tk.Frame(self.main_frame, bg=self.bg_color)
        lang_row.pack(pady=(0, 10))

        self.platform_label = tk.Label(lang_row,
                                       text=f"{self.t('platform')}: {self.platform.capitalize()}",
                                       font=("Helvetica", 9),
                                       bg=self.bg_color, fg=self.neutral_color)
        self.platform_label.pack(side=tk.LEFT, padx=(0, 20))

        self.lang_label = tk.Label(lang_row, text=f"{self.t('language')}:",
                                   font=("Helvetica", 9),
                                   bg=self.bg_color, fg=self.neutral_color)
        self.lang_label.pack(side=tk.LEFT)

        # Language dropdown
        lang_names = list(LANGUAGE_NAMES.values())
        self.lang_combo = ttk.Combobox(lang_row, values=lang_names,
                                       state="readonly", width=10)
        self.lang_combo.pack(side=tk.LEFT, padx=(5, 0))

        # Set current language in dropdown
        current_lang = self.current_lang.get()
        for i, (code, name) in enumerate(LANGUAGE_NAMES.items()):
            if code == current_lang:
                self.lang_combo.current(i)
                break
        else:
            self.lang_combo.current(0)

        self.lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)

        # Status Section
        self.status_frame = tk.LabelFrame(self.main_frame, text=f" {self.t('status')} ",
                                          font=("Helvetica", 12, "bold"),
                                          bg=self.bg_color, fg=self.fg_color,
                                          padx=10, pady=10)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))

        # Status indicators
        self.status_labels = {}
        self.component_keys = ["watchdog", "gateway", "port", "tui", "logs", "updates"]

        for key in self.component_keys:
            row = tk.Frame(self.status_frame, bg=self.bg_color)
            row.pack(fill=tk.X, pady=2)

            indicator = tk.Label(row, text="⚫", font=("Helvetica", 12),
                                 bg=self.bg_color, fg=self.neutral_color)
            indicator.pack(side=tk.LEFT)

            name = tk.Label(row, text=f"  {self.t(key)}", font=("Helvetica", 11),
                            bg=self.bg_color, fg=self.fg_color, anchor="w")
            name.pack(side=tk.LEFT)

            status_text = tk.Label(row, text="", font=("Helvetica", 9),
                                   bg=self.bg_color, fg=self.neutral_color, anchor="e")
            status_text.pack(side=tk.RIGHT)

            self.status_labels[key] = {"indicator": indicator, "name": name, "status": status_text}

        # Advanced Section Toggle Button
        self.expand_btn = tk.Button(self.main_frame,
                                    text=f"▶ {self.t('show_more')}",
                                    font=("Helvetica", 10),
                                    bg=self.bg_color, fg=self.accent_color,
                                    relief=tk.FLAT, cursor="hand2",
                                    command=self.toggle_advanced_section)
        self.expand_btn.pack(fill=tk.X, pady=(0, 5))

        # Advanced Container Frame (collapsible)
        self.advanced_container = tk.Frame(self.main_frame, bg=self.bg_color)

        # Model Selection Section
        self.model_frame = tk.LabelFrame(self.advanced_container, text=f" {self.t('ai_model')} ",
                                         font=("Helvetica", 12, "bold"),
                                         bg=self.bg_color, fg=self.fg_color,
                                         padx=10, pady=10)
        self.model_frame.pack(fill=tk.X, pady=(0, 10))

        model_row = tk.Frame(self.model_frame, bg=self.bg_color)
        model_row.pack(fill=tk.X)

        # Model dropdown
        model_names = [name for _, name in self.available_models]
        self.model_combo = ttk.Combobox(model_row, values=model_names,
                                        state="readonly", width=35)
        self.model_combo.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        # Set current model in dropdown
        current_model_id = self.current_model.get()
        for i, (model_id, model_name) in enumerate(self.available_models):
            if model_id == current_model_id:
                self.model_combo.current(i)
                break
        else:
            self.model_combo.current(0)

        self.apply_model_btn = tk.Button(model_row, text=self.t("apply"),
                                         font=("Helvetica", 10),
                                         bg=self.accent_color, fg="#000000",
                                         relief=tk.FLAT, cursor="hand2",
                                         command=self.apply_model_change)
        self.apply_model_btn.pack(side=tk.RIGHT)

        # Watchdog Toggle Section
        self.toggle_frame = tk.LabelFrame(self.advanced_container, text=f" {self.t('watchdog_auto')} ",
                                          font=("Helvetica", 12, "bold"),
                                          bg=self.bg_color, fg=self.fg_color,
                                          padx=10, pady=10)
        self.toggle_frame.pack(fill=tk.X, pady=(0, 10))

        toggle_row = tk.Frame(self.toggle_frame, bg=self.bg_color)
        toggle_row.pack(fill=tk.X)

        self.toggle_label = tk.Label(toggle_row, text=self.t("auto_monitoring"),
                                     font=("Helvetica", 11),
                                     bg=self.bg_color, fg=self.fg_color)
        self.toggle_label.pack(side=tk.LEFT)

        self.toggle_btn = tk.Button(toggle_row, text=self.t("off"), width=6,
                                    font=("Helvetica", 10, "bold"),
                                    bg=self.neutral_color, fg="#000000",
                                    relief=tk.FLAT, cursor="hand2",
                                    command=self.toggle_watchdog)
        self.toggle_btn.pack(side=tk.RIGHT)

        # Usage Stats Section
        self.usage_frame = tk.LabelFrame(self.advanced_container, text=f" {self.t('usage_stats')} ",
                                         font=("Helvetica", 12, "bold"),
                                         bg=self.bg_color, fg=self.fg_color,
                                         padx=10, pady=8)
        self.usage_frame.pack(fill=tk.X, pady=(0, 10))

        usage_row1 = tk.Frame(self.usage_frame, bg=self.bg_color)
        usage_row1.pack(fill=tk.X, pady=2)

        self.tokens_label = tk.Label(usage_row1, text=f"{self.t('tokens_today')}: 0",
                                     font=("Helvetica", 10),
                                     bg=self.bg_color, fg=self.fg_color)
        self.tokens_label.pack(side=tk.LEFT)

        self.cost_label = tk.Label(usage_row1, text=f"{self.t('cost_today')}: $0.00",
                                   font=("Helvetica", 10, "bold"),
                                   bg=self.bg_color, fg=self.success_color)
        self.cost_label.pack(side=tk.RIGHT)

        usage_row2 = tk.Frame(self.usage_frame, bg=self.bg_color)
        usage_row2.pack(fill=tk.X, pady=2)

        self.usage_details_label = tk.Label(usage_row2, text="",
                                            font=("Helvetica", 9),
                                            bg=self.bg_color, fg=self.neutral_color)
        self.usage_details_label.pack(side=tk.LEFT)

        self.reset_usage_btn = tk.Button(usage_row2, text=f"🔄 {self.t('reset')}",
                                         font=("Helvetica", 9),
                                         bg=self.neutral_color, fg="#000000",
                                         relief=tk.FLAT, cursor="hand2",
                                         command=self.reset_usage_stats)
        self.reset_usage_btn.pack(side=tk.RIGHT)

        # Manual Controls Section
        self.controls_frame = tk.LabelFrame(self.advanced_container, text=f" {self.t('manual_control')} ",
                                            font=("Helvetica", 12, "bold"),
                                            bg=self.bg_color, fg=self.fg_color,
                                            padx=10, pady=10)
        self.controls_frame.pack(fill=tk.X, pady=(0, 10))

        btn_row = tk.Frame(self.controls_frame, bg=self.bg_color)
        btn_row.pack(fill=tk.X)

        self.gateway_btn = tk.Button(btn_row, text=f"🔄 {self.t('restart_gateway')}",
                                     font=("Helvetica", 10),
                                     bg=self.accent_color, fg="#000000",
                                     relief=tk.FLAT, cursor="hand2", padx=10, pady=6,
                                     command=self.restart_gateway)
        self.gateway_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 3))

        self.tui_btn = tk.Button(btn_row, text=f"🖥️ {self.t('restart_tui')}",
                                 font=("Helvetica", 10),
                                 bg=self.accent_color, fg="#000000",
                                 relief=tk.FLAT, cursor="hand2", padx=10, pady=6,
                                 command=self.restart_tui)
        self.tui_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(3, 3))

        self.restart_all_btn = tk.Button(btn_row, text=f"⚡ {self.t('restart_all')}",
                                         font=("Helvetica", 10),
                                         bg=self.warning_color, fg="#000000",
                                         relief=tk.FLAT, cursor="hand2", padx=10, pady=6,
                                         command=self.restart_all)
        self.restart_all_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(3, 0))

        # Update Section
        self.update_frame = tk.LabelFrame(self.advanced_container, text=f" {self.t('software_update')} ",
                                          font=("Helvetica", 12, "bold"),
                                          bg=self.bg_color, fg=self.fg_color,
                                          padx=10, pady=10)
        self.update_frame.pack(fill=tk.X, pady=(0, 10))

        update_btn_row = tk.Frame(self.update_frame, bg=self.bg_color)
        update_btn_row.pack(fill=tk.X)

        self.check_update_btn = tk.Button(update_btn_row, text=f"🔍 {self.t('check')}",
                                          font=("Helvetica", 10),
                                          bg=self.accent_color, fg="#000000",
                                          relief=tk.FLAT, cursor="hand2", padx=10, pady=6,
                                          command=self.check_updates)
        self.check_update_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.ignore_update_btn = tk.Button(update_btn_row, text=f"🚫 {self.t('ignore')}",
                                           font=("Helvetica", 10),
                                           bg=self.neutral_color, fg="#000000",
                                           relief=tk.FLAT, cursor="hand2", padx=10, pady=6,
                                           command=self.ignore_update,
                                           state=tk.DISABLED)
        self.ignore_update_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 5))

        self.install_update_btn = tk.Button(update_btn_row, text=f"⬇️ {self.t('install')}",
                                            font=("Helvetica", 10),
                                            bg=self.success_color, fg="#000000",
                                            relief=tk.FLAT, cursor="hand2", padx=10, pady=6,
                                            command=self.install_updates,
                                            state=tk.DISABLED)
        self.install_update_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(0, 0))

        # Second row with recheck button
        update_btn_row2 = tk.Frame(self.update_frame, bg=self.bg_color)
        update_btn_row2.pack(fill=tk.X, pady=(5, 0))

        self.recheck_btn = tk.Button(update_btn_row2, text=f"🤖 {self.t('recheck_ai')}",
                                     font=("Helvetica", 10),
                                     bg=self.accent_color, fg="#000000",
                                     relief=tk.FLAT, cursor="hand2", padx=10, pady=6,
                                     command=self.recheck_with_ai,
                                     state=tk.DISABLED)
        self.recheck_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Notifications Section
        self.notify_frame = tk.LabelFrame(self.advanced_container, text=f" {self.t('notifications')} ",
                                          font=("Helvetica", 12, "bold"),
                                          bg=self.bg_color, fg=self.fg_color,
                                          padx=10, pady=5)
        self.notify_frame.pack(fill=tk.X, pady=(0, 10))

        notify_row = tk.Frame(self.notify_frame, bg=self.bg_color)
        notify_row.pack(fill=tk.X)

        # Checkboxes for notification types
        self.notify_gateway = tk.BooleanVar(value=True)
        self.notify_cost = tk.BooleanVar(value=True)
        self.notify_security = tk.BooleanVar(value=True)
        self.ai_update_check = tk.BooleanVar(value=True)

        cb1 = tk.Checkbutton(notify_row, text=f"🔴 {self.t('gateway_down')}",
                             variable=self.notify_gateway,
                             bg=self.bg_color, fg=self.fg_color,
                             selectcolor=self.bg_color, activebackground=self.bg_color,
                             font=("Helvetica", 9))
        cb1.pack(side=tk.LEFT)

        cb2 = tk.Checkbutton(notify_row, text=f"💰 {self.t('high_cost')}",
                             variable=self.notify_cost,
                             bg=self.bg_color, fg=self.fg_color,
                             selectcolor=self.bg_color, activebackground=self.bg_color,
                             font=("Helvetica", 9))
        cb2.pack(side=tk.LEFT, padx=(10, 0))

        cb3 = tk.Checkbutton(notify_row, text=f"🛡️ {self.t('security_alert')}",
                             variable=self.notify_security,
                             bg=self.bg_color, fg=self.fg_color,
                             selectcolor=self.bg_color, activebackground=self.bg_color,
                             font=("Helvetica", 9))
        cb3.pack(side=tk.LEFT, padx=(10, 0))

        # Second row for AI check
        notify_row2 = tk.Frame(self.notify_frame, bg=self.bg_color)
        notify_row2.pack(fill=tk.X, pady=(5, 0))

        cb4 = tk.Checkbutton(notify_row2, text=f"🤖 {self.t('ai_update_check')}",
                             variable=self.ai_update_check,
                             bg=self.bg_color, fg=self.fg_color,
                             selectcolor=self.bg_color, activebackground=self.bg_color,
                             font=("Helvetica", 9))
        cb4.pack(side=tk.LEFT)

        # Store checkbuttons for language refresh
        self.notify_checkbuttons = [
            (cb1, "gateway_down", "🔴"),
            (cb2, "high_cost", "💰"),
            (cb3, "security_alert", "🛡️"),
            (cb4, "ai_update_check", "🤖")
        ]

        # Log Section
        self.log_frame = tk.LabelFrame(self.advanced_container, text=f" {self.t('events')} ",
                                       font=("Helvetica", 12, "bold"),
                                       bg=self.bg_color, fg=self.fg_color,
                                       padx=10, pady=10)
        self.log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(self.log_frame,
                                                  font=("Courier", 9),
                                                  bg="#2d2d2d", fg="#cccccc",
                                                  height=6, wrap=tk.WORD,
                                                  relief=tk.FLAT)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # Last update label
        self.update_label = tk.Label(self.main_frame, text="",
                                     font=("Helvetica", 9),
                                     bg=self.bg_color, fg=self.neutral_color)
        self.update_label.pack(pady=(5, 0))

    def on_language_change(self, event=None):
        """Handle language change"""
        selected_index = self.lang_combo.current()
        lang_codes = list(LANGUAGE_NAMES.keys())
        if 0 <= selected_index < len(lang_codes):
            self.current_lang.set(lang_codes[selected_index])
            self.save_monitor_config()
            self.refresh_ui_texts()

    def toggle_advanced_section(self):
        """Toggle the visibility of advanced sections"""
        if self.advanced_expanded.get():
            # Collapse
            self.advanced_container.pack_forget()
            self.expand_btn.config(text=f"▶ {self.t('show_more')}")
            self.advanced_expanded.set(False)
        else:
            # Expand
            self.advanced_container.pack(fill=tk.BOTH, expand=True, before=self.update_label)
            self.expand_btn.config(text=f"▼ {self.t('show_less')}")
            self.advanced_expanded.set(True)
        self.save_monitor_config()

    def initialize_advanced_visibility(self):
        """Initialize the visibility of advanced sections based on saved state"""
        if self.advanced_expanded.get():
            self.advanced_container.pack(fill=tk.BOTH, expand=True, before=self.update_label)
            self.expand_btn.config(text=f"▼ {self.t('show_less')}")

    def refresh_ui_texts(self):
        """Refresh all UI texts with current language"""
        # Update frame titles
        self.status_frame.config(text=f" {self.t('status')} ")
        self.model_frame.config(text=f" {self.t('ai_model')} ")
        self.toggle_frame.config(text=f" {self.t('watchdog_auto')} ")
        self.controls_frame.config(text=f" {self.t('manual_control')} ")
        self.update_frame.config(text=f" {self.t('software_update')} ")
        self.log_frame.config(text=f" {self.t('events')} ")

        # Update labels
        self.platform_label.config(text=f"{self.t('platform')}: {self.platform.capitalize()}")
        self.lang_label.config(text=f"{self.t('language')}:")
        self.toggle_label.config(text=self.t("auto_monitoring"))

        # Update status component names
        for key in self.component_keys:
            self.status_labels[key]["name"].config(text=f"  {self.t(key)}")

        # Update buttons
        self.apply_model_btn.config(text=self.t("apply"))
        self.toggle_btn.config(text=self.t("on") if self.watchdog_auto.get() else self.t("off"))
        self.gateway_btn.config(text=f"🔄 {self.t('restart_gateway')}")
        self.tui_btn.config(text=f"🖥️ {self.t('restart_tui')}")
        self.restart_all_btn.config(text=f"⚡ {self.t('restart_all')}")
        self.check_update_btn.config(text=f"🔍 {self.t('check')}")
        self.ignore_update_btn.config(text=f"🚫 {self.t('ignore')}")
        self.install_update_btn.config(text=f"⬇️ {self.t('install')}")
        self.recheck_btn.config(text=f"🤖 {self.t('recheck_ai')}")

        # Update usage stats frame
        self.usage_frame.config(text=f" {self.t('usage_stats')} ")
        self.reset_usage_btn.config(text=f"🔄 {self.t('reset')}")
        self.update_usage_display()

        # Update notifications frame and checkbuttons
        self.notify_frame.config(text=f" {self.t('notifications')} ")
        for cb, key, emoji in self.notify_checkbuttons:
            cb.config(text=f"{emoji} {self.t(key)}")

        # Update expand button
        if self.advanced_expanded.get():
            self.expand_btn.config(text=f"▼ {self.t('show_less')}")
        else:
            self.expand_btn.config(text=f"▶ {self.t('show_more')}")

        # Refresh status display
        self.check_all_status()

    def run_command(self, cmd, timeout=10):
        """Run a shell command and return output (cross-platform)"""
        try:
            if self.is_windows:
                result = subprocess.run(cmd, shell=True, capture_output=True,
                                        text=True, timeout=timeout)
            else:
                result = subprocess.run(cmd, shell=True, capture_output=True,
                                        text=True, timeout=timeout)
            return result.stdout.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "Timeout", -1
        except Exception as e:
            return str(e), -1

    def check_process(self, pattern):
        """Check if a process matching pattern is running (cross-platform)"""
        if self.is_windows:
            output, _ = self.run_command(f'tasklist /FI "IMAGENAME eq {pattern}*" 2>NUL')
            return pattern.lower() in output.lower()
        else:
            output, _ = self.run_command(f"pgrep -f '{pattern}'")
            return bool(output)

    def check_port(self, port):
        """Check if a port is responding (cross-platform)"""
        if self.is_windows:
            output, code = self.run_command(
                f'powershell -Command "Test-NetConnection -ComputerName localhost -Port {port} -WarningAction SilentlyContinue | Select-Object -ExpandProperty TcpTestSucceeded"'
            )
            return "True" in output
        else:
            _, code = self.run_command(f"nc -z 127.0.0.1 {port}")
            return code == 0

    def check_websocket_connection(self, port):
        """Check if there are established connections to the port"""
        if self.is_windows:
            output, _ = self.run_command(f'netstat -an | findstr ":{port}.*ESTABLISHED"')
        else:
            output, _ = self.run_command(f"lsof -i :{port} 2>/dev/null | grep ESTABLISHED")
        return bool(output.strip())

    def check_logs_fresh(self):
        """Check if logs were updated recently (within 5 min)"""
        log_file = Path(f"/tmp/openclaw/openclaw-{datetime.now().strftime('%Y-%m-%d')}.log")
        if self.is_windows:
            log_file = self.openclaw_config_dir / "logs" / f"openclaw-{datetime.now().strftime('%Y-%m-%d')}.log"

        if log_file.exists():
            mtime = log_file.stat().st_mtime
            age = time.time() - mtime
            return age < 300  # 5 minutes
        return False

    def get_recent_errors(self, lines=5):
        """Get recent errors from log"""
        log_file = Path(f"/tmp/openclaw/openclaw-{datetime.now().strftime('%Y-%m-%d')}.log")
        if self.is_windows:
            log_file = self.openclaw_config_dir / "logs" / f"openclaw-{datetime.now().strftime('%Y-%m-%d')}.log"

        if log_file.exists():
            if self.is_windows:
                output, _ = self.run_command(
                    f'powershell -Command "Get-Content \'{log_file}\' | Select-String -Pattern \'error|fail\' | Select-Object -Last {lines}"'
                )
            else:
                output, _ = self.run_command(
                    f"grep -i 'error\\|fail' '{log_file}' | tail -{lines}"
                )
            return output
        return ""

    def check_git_updates(self):
        """Check if there are updates available on GitHub"""
        # Fetch latest from remote
        self.run_command(f"cd {self.openclaw_dir} && git fetch origin", timeout=30)

        # Check if we're behind
        output, code = self.run_command(
            f"cd {self.openclaw_dir} && git rev-list HEAD..origin/main --count"
        )

        try:
            commits_behind = int(output.strip()) if output.strip().isdigit() else 0
        except:
            commits_behind = 0

        # Get current and remote version
        local_version, _ = self.run_command(
            f"cd {self.openclaw_dir} && git describe --tags --always 2>/dev/null || git rev-parse --short HEAD"
        )
        remote_version, _ = self.run_command(
            f"cd {self.openclaw_dir} && git describe --tags --always origin/main 2>/dev/null || git rev-parse --short origin/main"
        )

        # Check for security-related commits
        security_output, _ = self.run_command(
            f"cd {self.openclaw_dir} && git log HEAD..origin/main --oneline --grep='security\\|Security\\|CVE\\|vulnerability\\|fix' 2>/dev/null"
        )
        has_security_updates = bool(security_output.strip())

        # Security scan of incoming changes
        security_scan = self.scan_incoming_changes()

        return {
            "commits_behind": commits_behind,
            "local_version": local_version.strip(),
            "remote_version": remote_version.strip(),
            "has_security": has_security_updates,
            "update_available": commits_behind > 0,
            "security_scan": security_scan
        }

    def scan_incoming_changes(self):
        """Scan incoming changes for suspicious patterns with AI analysis"""
        # DANGEROUS patterns - these are almost always malicious
        dangerous_patterns = [
            (r"curl\s+.*\|.*sh", "Remote code execution: curl | sh"),
            (r"wget\s+.*\|.*sh", "Remote code execution: wget | sh"),
            (r"nc\s+-e", "Reverse shell: netcat -e"),
            (r"/dev/tcp/", "Reverse shell: /dev/tcp"),
            (r"bash\s+-i\s+>&", "Reverse shell: bash -i"),
            (r"python.*-c.*socket", "Potential reverse shell: python socket"),
            (r"rm\s+-rf\s+/[^.]", "Dangerous: rm -rf /"),
            (r":(){ :|:& };:", "Fork bomb"),
            (r"mkfifo.*nc.*sh", "Named pipe reverse shell"),
        ]

        # NORMAL patterns for CLI tools - these are expected in OpenClaw
        # We note them but don't flag as dangerous
        normal_cli_patterns = [
            "child_process",  # Node.js process spawning - required for CLI
            "exec(",          # Command execution - required for CLI
            "spawn(",         # Process spawning - required for CLI
            "execSync",       # Sync execution - required for CLI
            "spawnSync",      # Sync spawning - required for CLI
        ]

        results = {
            "clean": True,
            "warnings": [],
            "info": [],
            "files_checked": 0,
            "suspicious_files": [],
            "ai_verdict": None,
            "ai_details": None
        }

        # Get list of changed files
        changed_files, _ = self.run_command(
            f"cd {self.openclaw_dir} && git diff --name-only HEAD..origin/main"
        )

        if not changed_files.strip():
            return results

        files = changed_files.strip().split('\n')
        results["files_checked"] = len(files)

        # Check for DANGEROUS patterns only
        for pattern, description in dangerous_patterns:
            output, _ = self.run_command(
                f"cd {self.openclaw_dir} && git diff HEAD..origin/main -U0 2>/dev/null | grep -E '{pattern}' | head -3"
            )
            if output.strip():
                results["clean"] = False
                results["warnings"].append(f"⚠️ {description}")
                results["suspicious_files"].append(output.strip()[:100])

        # Check for new executable scripts in unexpected places
        new_scripts, _ = self.run_command(
            f"cd {self.openclaw_dir} && git diff HEAD..origin/main --name-only --diff-filter=A | grep -E '\\.(sh|bash|py|rb|pl)$' | grep -v -E '^(scripts/|test/)'"
        )
        if new_scripts.strip():
            results["info"].append(f"New scripts added: {new_scripts.strip()[:50]}")

        # Check for new binary files
        binary_files, _ = self.run_command(
            f"cd {self.openclaw_dir} && git diff HEAD..origin/main --numstat 2>/dev/null | grep -E '^-\\s+-' | head -5"
        )
        if binary_files.strip():
            results["info"].append("New binary files detected")

        # If dangerous patterns found, try AI analysis via Gateway
        if not results["clean"]:
            ai_result = self.ai_security_analysis()
            if ai_result:
                results["ai_verdict"] = ai_result.get("verdict", "unknown")
                results["ai_details"] = ai_result.get("details", "")

        return results

    def ai_security_analysis(self):
        """Use OpenClaw Gateway to analyze security of incoming changes"""
        try:
            # Check if gateway is running
            if not self.check_port(18789):
                return None

            # Get the diff content (limited to avoid token overflow)
            diff_output, code = self.run_command(
                f"cd {self.openclaw_dir} && git diff HEAD..origin/main --stat && echo '---DIFF---' && git diff HEAD..origin/main -U3 | head -500",
                timeout=30
            )

            if code != 0 or not diff_output.strip():
                return None

            # Create a security analysis prompt
            analysis_prompt = f"""Analyze this git diff for security issues.
Focus on: remote code execution, data exfiltration, backdoors, obfuscation.
Context: This is for OpenClaw, a CLI tool that legitimately uses child_process/exec for terminal operations.

Respond with ONLY a JSON object:
{{"verdict": "SAFE|REVIEW|DANGEROUS", "details": "brief explanation"}}

Diff:
{diff_output[:8000]}"""

            # Save prompt to temp file
            prompt_file = self.openclaw_config_dir / "security-check-prompt.txt"
            with open(prompt_file, 'w') as f:
                f.write(analysis_prompt)

            # Call OpenClaw CLI for analysis (uses configured model)
            result, code = self.run_command(
                f"cd {self.openclaw_dir} && echo '{analysis_prompt[:2000]}' | timeout 30 pnpm openclaw ask --no-stream 'Is this code safe? Reply with just SAFE, REVIEW, or DANGEROUS and one sentence why.' 2>/dev/null | tail -5",
                timeout=45
            )

            if code == 0 and result.strip():
                # Parse the response
                response = result.strip().upper()
                if "DANGEROUS" in response:
                    return {"verdict": "DANGEROUS", "details": result.strip()}
                elif "REVIEW" in response:
                    return {"verdict": "REVIEW", "details": result.strip()}
                elif "SAFE" in response:
                    return {"verdict": "SAFE", "details": result.strip()}

            return None

        except Exception as e:
            print(f"AI analysis error: {e}")
            return None

    def should_auto_check_updates(self):
        """Check if we should auto-check updates (every 2 days)"""
        try:
            if self.update_check_file.exists():
                with open(self.update_check_file, 'r') as f:
                    data = json.load(f)
                    last_check = datetime.fromisoformat(data.get("last_check", "2000-01-01"))
                    days_since = (datetime.now() - last_check).days
                    return days_since >= 2
            return True
        except:
            return True

    def save_update_check_time(self):
        """Save the last update check time"""
        try:
            self.update_check_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.update_check_file, 'w') as f:
                json.dump({"last_check": datetime.now().isoformat()}, f)
        except:
            pass

    def update_status(self, key, is_ok, status_text=""):
        """Update a status indicator"""
        indicator = self.status_labels[key]["indicator"]
        status = self.status_labels[key]["status"]

        if is_ok is None:  # Neutral/Unknown
            indicator.config(text="⚫", fg=self.neutral_color)
        elif is_ok:
            indicator.config(text="🟢", fg=self.success_color)
        elif is_ok is False and status_text and self.t("warning").lower() in status_text.lower():
            indicator.config(text="🟡", fg=self.warning_color)
        else:
            indicator.config(text="🔴", fg=self.error_color)

        status.config(text=status_text)

    def log_event(self, message):
        """Add event to log"""
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        # Update log frame title with last event time
        date_str = now.strftime("%d.%m. %H:%M")
        self.log_frame.config(text=f" {self.t('events')} ({date_str}) ")

    def check_all_status(self):
        """Check all component status"""
        # Watchdog
        watchdog_running = self.check_process("watchdog")
        self.update_status("watchdog", watchdog_running,
                           self.t("running") if watchdog_running else self.t("stopped"))

        # Update toggle button
        if watchdog_running:
            self.watchdog_auto.set(True)
            self.toggle_btn.config(text=self.t("on"), bg=self.success_color, fg="#000000")
        else:
            self.watchdog_auto.set(False)
            self.toggle_btn.config(text=self.t("off"), bg=self.neutral_color, fg="#000000")

        # Gateway
        gateway_running = self.check_process("openclaw-gateway")
        self.update_status("gateway", gateway_running,
                           self.t("running") if gateway_running else self.t("stopped"))

        # Port
        port_ok = self.check_port(18789)
        self.update_status("port", port_ok,
                           self.t("responding") if port_ok else self.t("not_responding"))

        # TUI
        tui_running = self.check_process("openclaw.*tui") if not self.is_windows else self.check_process("openclaw")
        if tui_running:
            connected = self.check_websocket_connection(18789)
            self.update_status("tui", connected,
                               self.t("connected") if connected else f"{self.t('disconnected')} ({self.t('warning')})")
        else:
            self.update_status("tui", None, self.t("not_running"))

        # Logs
        logs_fresh = self.check_logs_fresh()
        self.update_status("logs", logs_fresh,
                           self.t("fresh") if logs_fresh else f"{self.t('stale')} ({self.t('warning')})")

        # Updates - show cached status with version
        current_version = self.get_current_version() if hasattr(self, 'get_current_version') else ""
        version_prefix = f"v{current_version} → " if current_version else ""

        if self.update_available:
            if hasattr(self, 'has_security_update') and self.has_security_update:
                self.update_status("updates", False, f"{version_prefix}{self.t('security_update')} ({self.update_info})")
            else:
                indicator = self.status_labels["updates"]["indicator"]
                indicator.config(text="🟡", fg=self.warning_color)
                self.status_labels["updates"]["status"].config(text=f"{version_prefix}{self.t('available')} ({self.update_info})")
        elif self.last_update_check:
            version_info = self.get_current_version() if hasattr(self, 'get_current_version') else ""
            check_date = self.last_update_check.strftime('%d.%m. %H:%M')
            if version_info:
                self.update_status("updates", True, f"v{version_info} ({check_date})")
            else:
                self.update_status("updates", True, f"{self.t('current')} ({check_date})")
        else:
            self.update_status("updates", None, self.t("not_checked"))

        # Auto-check updates every 2 days
        if self.should_auto_check_updates() and not hasattr(self, '_auto_check_done'):
            self._auto_check_done = True
            threading.Thread(target=self._background_update_check, daemon=True).start()

        # Update timestamp
        self.update_label.config(
            text=f"{self.t('updated_at')}: {datetime.now().strftime('%H:%M:%S')}"
        )

    def apply_model_change(self):
        """Apply the selected model"""
        selected_index = self.model_combo.current()
        if selected_index >= 0:
            model_id, model_name = self.available_models[selected_index]

            if self.save_model_config(model_id):
                self.current_model.set(model_id)
                self.log_event(f"{self.t('model_changed')}: {model_name}")
                self.log_event(self.t("gateway_restart_required"))

                # Ask if user wants to restart gateway
                if messagebox.askyesno(self.t("model_changed"),
                                       self.t("model_changed_msg").format(model=model_name)):
                    self.restart_gateway()
            else:
                self.log_event(f"❌ {self.t('config_error')}")

    def toggle_watchdog(self):
        """Toggle watchdog on/off"""
        if self.watchdog_auto.get():
            # Turn off
            self.log_event(self.t("stopping_watchdog"))
            if self.is_windows:
                self.run_command("taskkill /F /IM watchdog* 2>NUL")
            else:
                self.run_command(f"{self.watchdog_script} stop")
            self.toggle_btn.config(text=self.t("off"), bg=self.neutral_color, fg="#000000")
            self.watchdog_auto.set(False)
            self.log_event(self.t("watchdog_stopped"))
        else:
            # Turn on
            self.log_event(self.t("starting_watchdog"))
            if not self.is_windows:
                self.run_command(f"{self.watchdog_script} start")
            else:
                self.log_event(self.t("watchdog_not_available"))
            time.sleep(1)
            self.toggle_btn.config(text=self.t("on"), bg=self.success_color, fg="#000000")
            self.watchdog_auto.set(True)
            self.log_event(self.t("watchdog_started"))

        self.check_all_status()

    def restart_gateway(self):
        """Restart gateway"""
        self.gateway_btn.config(state=tk.DISABLED, text="⏳...")
        self.log_event(self.t("restarting_gateway"))

        def do_restart():
            if self.is_windows:
                self.run_command("taskkill /F /IM openclaw-gateway* 2>NUL")
                time.sleep(2)
                self.run_command(f"cd {self.openclaw_dir} && start /B pnpm openclaw gateway run")
            else:
                self.run_command(f"{self.watchdog_script} restart-gateway", timeout=30)
            time.sleep(3)
            self.root.after(0, self._gateway_restart_complete)

        threading.Thread(target=do_restart, daemon=True).start()

    def _gateway_restart_complete(self):
        self.gateway_btn.config(state=tk.NORMAL, text=f"🔄 {self.t('restart_gateway')}")
        self.log_event(self.t("gateway_restart_complete"))
        self.check_all_status()

    def restart_tui(self):
        """Restart TUI"""
        self.tui_btn.config(state=tk.DISABLED, text="⏳...")
        self.log_event(self.t("restarting_tui"))

        def do_restart():
            if self.is_windows:
                self.run_command("taskkill /F /IM openclaw* 2>NUL")
                time.sleep(1)
                self.run_command(f"start cmd /k \"cd {self.openclaw_dir} && pnpm openclaw tui\"")
            elif self.is_mac:
                self.run_command(f"{self.watchdog_script} restart-tui", timeout=15)
            else:
                # Linux - try to open in a new terminal
                self.run_command(f"pkill -f 'openclaw.*tui'")
                time.sleep(1)
                terminals = ["gnome-terminal", "konsole", "xterm", "xfce4-terminal"]
                for term in terminals:
                    code = os.system(f"which {term} > /dev/null 2>&1")
                    if code == 0:
                        self.run_command(f"{term} -- bash -c 'cd {self.openclaw_dir} && pnpm openclaw tui'")
                        break
            time.sleep(3)
            self.root.after(0, self._tui_restart_complete)

        threading.Thread(target=do_restart, daemon=True).start()

    def _tui_restart_complete(self):
        self.tui_btn.config(state=tk.NORMAL, text=f"🖥️ {self.t('restart_tui')}")
        self.log_event(self.t("tui_restart_complete"))
        self.check_all_status()

    def restart_all(self):
        """Restart everything"""
        self.restart_all_btn.config(state=tk.DISABLED, text="⏳...")
        self.log_event(self.t("restarting_all"))

        def do_restart():
            if self.is_windows:
                self.run_command("taskkill /F /IM openclaw* 2>NUL")
            else:
                self.run_command(f"{self.watchdog_script} restart-all", timeout=45)
            time.sleep(5)
            self.root.after(0, self._restart_all_complete)

        threading.Thread(target=do_restart, daemon=True).start()

    def _restart_all_complete(self):
        self.restart_all_btn.config(state=tk.NORMAL, text=f"⚡ {self.t('restart_all')}")
        self.log_event(self.t("full_restart_complete"))
        self.check_all_status()

    def _background_update_check(self):
        """Background check for updates (auto-check every 2 days)"""
        try:
            result = self.check_git_updates()
            self.root.after(0, lambda: self._update_check_complete(result, silent=True))
        except:
            pass

    def check_updates(self):
        """Manual update check"""
        self.check_update_btn.config(state=tk.DISABLED, text="🔍...")
        self.log_event(self.t("checking_updates"))

        def do_check():
            result = self.check_git_updates()
            self.root.after(0, lambda: self._update_check_complete(result, silent=False))

        threading.Thread(target=do_check, daemon=True).start()

    def _update_check_complete(self, result, silent=False):
        self.check_update_btn.config(state=tk.NORMAL, text=f"🔍 {self.t('check')}")
        self.last_update_check = datetime.now()
        self.save_update_check_time()

        # Store security scan results
        self.security_scan_result = result.get("security_scan", {"clean": True})

        if result["update_available"]:
            self.update_available = True
            self.has_security_update = result["has_security"]
            self.update_info = f"{result['commits_behind']} {self.t('commits_behind')}"

            # Log security scan results
            scan = self.security_scan_result
            if not scan["clean"]:
                # Show warnings
                for warning in scan.get("warnings", [])[:3]:
                    self.log_event(warning)

                # Show AI verdict if available
                if scan.get("ai_verdict"):
                    verdict = scan["ai_verdict"]
                    if verdict == "SAFE":
                        self.log_event(f"🤖 {self.t('ai_verdict')}: {self.t('safe')}")
                        self.install_update_btn.config(bg=self.warning_color)  # Yellow - review but probably OK
                    elif verdict == "REVIEW":
                        self.log_event(f"🤖 {self.t('ai_verdict')}: {self.t('review_recommended')}")
                        self.install_update_btn.config(bg=self.warning_color)
                    else:
                        self.log_event(f"🤖 {self.t('ai_verdict')}: {self.t('potentially_dangerous')}")
                        self.install_update_btn.config(bg=self.error_color)

                    if scan.get("ai_details"):
                        self.log_event(f"   {scan['ai_details'][:100]}")
                else:
                    self.log_event(self.t("ai_analysis_failed"))
                    self.install_update_btn.config(bg=self.error_color)
            else:
                # Show info items (non-dangerous)
                for info in scan.get("info", []):
                    self.log_event(f"ℹ️ {info}")
                self.log_event(f"✅ {self.t('security_scan_ok')} ({scan['files_checked']} {self.t('files')})")
                self.install_update_btn.config(bg=self.success_color)

            if result["has_security"]:
                self.log_event(f"⚠️ {self.t('security_update')} {result['commits_behind']} commits")
            else:
                self.log_event(f"Update: {result['commits_behind']} {self.t('commits_behind')}")

            self.install_update_btn.config(state=tk.NORMAL)
            self.ignore_update_btn.config(state=tk.NORMAL)
            self.recheck_btn.config(state=tk.NORMAL)
        else:
            self.update_available = False
            self.has_security_update = False
            self.update_info = ""
            if not silent:
                self.log_event(f"✅ {self.t('openclaw_current')}")
            self.install_update_btn.config(state=tk.DISABLED, bg=self.success_color)
            self.ignore_update_btn.config(state=tk.DISABLED)
            self.recheck_btn.config(state=tk.DISABLED)

        self.check_all_status()

    def install_updates(self):
        """Install updates from GitHub"""
        # Check if security scan found issues
        scan = getattr(self, 'security_scan_result', {"clean": True})
        if not scan["clean"]:
            warning_msg = self.t("suspicious_patterns")
            for w in scan.get("warnings", [])[:5]:
                warning_msg += f"• {w}\n"
            warning_msg += self.t("continue_anyway")

            if not messagebox.askyesno(self.t("security_warning"), warning_msg, icon='warning'):
                self.log_event(self.t("update_cancelled"))
                return

        self.install_update_btn.config(state=tk.DISABLED, text="⬇️...")
        self.log_event(self.t("installing_updates"))

        def do_update():
            # Stop services
            if self.is_windows:
                self.run_command("taskkill /F /IM openclaw* 2>NUL")
            else:
                self.run_command(f"{self.watchdog_script} stop", timeout=10)
                self.run_command("pkill -9 -f 'openclaw-gateway'", timeout=5)
            time.sleep(2)

            # Git pull
            output, code = self.run_command(
                f"cd {self.openclaw_dir} && git pull origin main",
                timeout=60
            )

            if code == 0:
                # Rebuild
                if self.is_windows:
                    output, code = self.run_command(
                        f"cd {self.openclaw_dir} && npm install && npm run build",
                        timeout=180
                    )
                else:
                    output, code = self.run_command(
                        f"cd {self.openclaw_dir} && pnpm install && pnpm build",
                        timeout=180
                    )

            self.root.after(0, lambda: self._install_complete(code == 0))

        threading.Thread(target=do_update, daemon=True).start()

    def _install_complete(self, success):
        self.install_update_btn.config(state=tk.NORMAL, text=f"⬇️ {self.t('install')}")

        if success:
            self.update_available = False
            self.has_security_update = False
            self.log_event(f"✅ {self.t('update_installed')}")
            self.install_update_btn.config(state=tk.DISABLED)

            # Restart gateway
            self.restart_gateway()
        else:
            self.log_event(f"❌ {self.t('update_failed')}")

        self.check_all_status()

    def get_current_version(self):
        """Get the current version from package.json or git"""
        try:
            package_json = self.openclaw_dir / "package.json"
            if package_json.exists():
                with open(package_json, 'r') as f:
                    data = json.load(f)
                    return data.get("version", "")
        except:
            pass
        return ""

    def reset_usage_stats(self):
        """Reset usage statistics"""
        self.tokens_today = 0
        self.cost_today = 0.0
        self.usage_by_model = {}
        self.update_usage_display()
        self.save_usage_stats()
        self.log_event(f"🔄 {self.t('reset')} - {self.t('usage_stats')}")

    def update_usage_display(self):
        """Update the usage stats display"""
        self.tokens_label.config(text=f"{self.t('tokens_today')}: {self.tokens_today:,}")
        self.cost_label.config(text=f"{self.t('cost_today')}: ${self.cost_today:.4f}")

        # Show breakdown by model
        if self.usage_by_model:
            details = " | ".join([f"{m.split('/')[-1][:10]}: ${c:.3f}"
                                  for m, c in self.usage_by_model.items()])
            self.usage_details_label.config(text=details)
        else:
            self.usage_details_label.config(text="")

    def load_usage_stats(self):
        """Load usage stats from file"""
        try:
            usage_file = self.openclaw_config_dir / "usage-stats.json"
            if usage_file.exists():
                with open(usage_file, 'r') as f:
                    data = json.load(f)
                    # Check if it's from today
                    if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                        self.tokens_today = data.get("tokens", 0)
                        self.cost_today = data.get("cost", 0.0)
                        self.usage_by_model = data.get("by_model", {})
        except:
            pass

    def save_usage_stats(self):
        """Save usage stats to file"""
        try:
            usage_file = self.openclaw_config_dir / "usage-stats.json"
            with open(usage_file, 'w') as f:
                json.dump({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "tokens": self.tokens_today,
                    "cost": self.cost_today,
                    "by_model": self.usage_by_model
                }, f, indent=2)
        except:
            pass

    def add_usage(self, tokens, cost, model="unknown"):
        """Add usage to today's stats"""
        self.tokens_today += tokens
        self.cost_today += cost
        if model not in self.usage_by_model:
            self.usage_by_model[model] = 0.0
        self.usage_by_model[model] += cost
        self.update_usage_display()
        self.save_usage_stats()

    def ignore_update(self):
        """Ignore the current update"""
        self.update_available = False
        self.has_security_update = False
        self.install_update_btn.config(state=tk.DISABLED)
        self.ignore_update_btn.config(state=tk.DISABLED)
        self.recheck_btn.config(state=tk.DISABLED)
        self.log_event(f"🚫 {self.t('update_ignored')}")
        self.check_all_status()

    def recheck_with_ai(self):
        """Re-run AI analysis on the current update"""
        self.recheck_btn.config(state=tk.DISABLED, text="🤖...")
        self.log_event(f"🤖 {self.t('ai_checking')}")

        def do_recheck():
            ai_result = self.ai_security_analysis(always_run=True) if hasattr(self, 'ai_security_analysis') else None
            self.root.after(0, lambda: self._recheck_complete(ai_result))

        threading.Thread(target=do_recheck, daemon=True).start()

    def _recheck_complete(self, ai_result):
        """Handle AI recheck completion"""
        self.recheck_btn.config(state=tk.NORMAL, text=f"🤖 {self.t('recheck_ai')}")

        if ai_result:
            verdict = ai_result.get("verdict", "unknown")
            if verdict == "SAFE":
                self.log_event(f"✅ {self.t('ai_analysis_ok')}")
            elif verdict == "REVIEW":
                self.log_event(f"⚠️ {self.t('ai_analysis_warning')}")
            else:
                self.log_event(f"🔴 {self.t('ai_verdict')}: {verdict}")
        else:
            self.log_event(f"❓ {self.t('ai_analysis_failed')}")

    def monitoring_loop(self):
        """Background monitoring loop"""
        while self.running:
            try:
                self.root.after(0, self.check_all_status)
            except:
                pass
            time.sleep(5)

    def start_monitoring(self):
        """Start the monitoring thread"""
        self.check_all_status()
        thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        thread.start()

    def on_close(self):
        """Handle window close - proper cleanup"""
        self.running = False
        # Give threads a moment to stop
        time.sleep(0.1)
        try:
            self.root.quit()  # Stop mainloop
            self.root.destroy()  # Destroy window
        except:
            pass
        # Force exit to ensure all threads stop
        import os
        os._exit(0)

    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()


if __name__ == "__main__":
    app = OpenClawMonitor()
    app.run()
