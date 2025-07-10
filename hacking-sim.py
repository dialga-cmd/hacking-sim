import pygame
import sys
import time
from random import random, choice

pygame.init()
# Open in full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Kali Terminal Simulation")

FONT = pygame.font.SysFont("consolas", 22)
BIG_FONT = pygame.font.SysFont("consolas", 40, bold=True)
BG_COLOR = (10, 10, 10)
FG_COLOR = (0, 255, 0)
ERROR_COLOR = (255, 60, 60)
STATUS_COLOR = (255, 255, 0)
PROGRESS_BG = (40, 40, 40)
PROGRESS_FG = (0, 200, 0)

lines = []
max_lines = (HEIGHT - 60) // 26

# Expanded list of echo commands for realism
commands = [
    "echo Scanning network...",
    "echo Found open port: 22",
    "echo Attempting SSH brute force...",
    "echo SSH login successful: root@192.168.1.1",
    "echo Downloading payload...",
    "echo Uploading payload to target...",
    "echo Executing payload...",
    "echo Privilege escalation in progress...",
    "echo Root privileges acquired.",
    "echo Searching for sensitive files...",
    "echo Data exfiltration started...",
    "echo Data exfiltration complete.",
    "echo Cleaning up traces...",
    "echo Removing logs...",
    "echo Attack complete.",
    "nmap -A 192.168.1.1",
    "hydra -l admin -P passwords.txt 192.168.1.1 ssh",
    "sudo -l",
    "scp /tmp/backdoor root@192.168.1.22:/tmp/",
    "tar czf /tmp/data.tar.gz /var/www/html",
    "history -c",
]
outputs = [
    "Connection established.",
    "Login successful.",
    "Access denied.",
    "Root privileges acquired.",
    "Exploit sent.",
    "ERROR: Permission denied.",
    "Sensitive data found.",
    "Payload executed successfully.",
    "Logs removed.",
    "No traces left.",
]
status_msgs = [
    "Connecting to target...",
    "Bypassing firewall...",
    "Uploading payload...",
    "Hijacking system...",
    "Escalating privileges...",
    "Exfiltrating data...",
    "Cleaning up...",
]

def draw_terminal():
    screen.fill(BG_COLOR)
    y = 10
    for line, color in lines[-max_lines:]:
        txt = FONT.render(line, True, color)
        screen.blit(txt, (20, y))
        y += 26

def draw_progress(progress):
    pygame.draw.rect(screen, PROGRESS_BG, (20, HEIGHT-40, WIDTH-40, 20))
    pygame.draw.rect(screen, PROGRESS_FG, (20, HEIGHT-40, int((WIDTH-40)*progress), 20))

def add_line(text, color=FG_COLOR):
    lines.append((text, color))

def show_hijacked_banner():
    banner = [
        "███████╗██╗   ██╗███████╗████████╗██╗███╗   ███╗",
        "██╔════╝██║   ██║██╔════╝╚══██╔══╝██║████╗ ████║",
        "█████╗  ██║   ██║███████╗   ██║   ██║██╔████╔██║",
        "██╔══╝  ██║   ██║╚════██║   ██║   ██║██║╚██╔╝██║",
        "██║     ╚██████╔╝███████║   ██║   ██║██║ ╚═╝ ██║",
        "╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚═╝╚═╝     ╚═╝",
        "",
        ">>> SYSTEM HACKED! <<<"
    ]
    lines.clear()
    for b in banner:
        add_line(b, ERROR_COLOR)

clock = pygame.time.Clock()
progress = 0
step = 0
total_steps = 100  # More steps for slower progress
running = True
show_banner = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    if not show_banner:
        if step < total_steps:
            # 1. Status message (yellow)
            if step % 4 == 0:
                status = choice(status_msgs)
                add_line("[!] " + status, STATUS_COLOR)
                last_status = status
            # 2. Command (green)
            cmd = choice(commands)
            add_line(f"root@kali:~# {cmd}", FG_COLOR)
            # 3. Output or error (cyan or red)
            if "denied" in cmd.lower() or "fail" in cmd.lower() or random() < 0.15:
                # Only show error after a command that could fail, or sometimes randomly
                error = "ERROR: Permission denied."
                add_line(error, ERROR_COLOR)
            elif random() < 0.4:
                out = choice(outputs)
                color = ERROR_COLOR if "ERROR" in out else FG_COLOR
                add_line(out, color)
            progress = (step+1)/total_steps
            step += 1
            time.sleep(0.2)
        else:
            show_hijacked_banner()
            show_banner = True

    draw_terminal()
    draw_progress(progress)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
