#!/usr/bin/env python3
import psutil
import requests
import datetime
import time
import socket
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text

console = Console()

def get_system_info():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    cpu_count = psutil.cpu_count(logical=True)
    cpu_percent = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Temperatura CPU
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = temps.get('coretemp', [None])[0].current if temps.get('coretemp') else None
        cpu_temp_str = f"{cpu_temp:.1f}°C" if cpu_temp else "N/A"
    except Exception:
        cpu_temp_str = "N/A"

    return {
        "CPU Núcleos": cpu_count,
        "CPU Uso": cpu_percent,
        "CPU Temp": cpu_temp_str,
        "RAM Total": f"{ram.total / (1024 ** 3):.2f} GB",
        "RAM Usada": f"{ram.used / (1024 ** 3):.2f} GB ({ram.percent}%)",
        "Disk Total": f"{disk.total / (1024 ** 3):.2f} GB",
        "Disk Usado": f"{disk.used / (1024 ** 3):.2f} GB ({disk.percent}%)",
        "Uptime": str(uptime).split('.')[0]
    }

def get_network_info():
    """Información general de red y adaptadores"""
    # IP pública
    try:
        ip_public = requests.get("https://api.ipify.org", timeout=2).text
    except:
        ip_public = "N/A"

    net_io = psutil.net_io_counters()
    # Interfaces
    interfaces = []
    default_iface = None
    # Intento determinar la interfaz por defecto usando la conexión a google
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = None

    for iface, addrs in psutil.net_if_addrs().items():
        ipv4 = ipv6 = mac = "-"
        for addr in addrs:
            if addr.family == socket.AF_INET:
                ipv4 = addr.address
            elif addr.family == socket.AF_INET6:
                ipv6 = addr.address
            elif addr.family == psutil.AF_LINK:
                mac = addr.address
        marker = " "
        if ipv4 == local_ip:
            marker = ">"
            default_iface = iface
        interfaces.append((marker, iface, ipv4, mac))

    return {
        "IP Pública": ip_public,
        "TX": f"{net_io.bytes_sent / (1024**2):.2f} MB",
        "RX": f"{net_io.bytes_recv / (1024**2):.2f} MB",
        "Interfaces": interfaces
    }

def get_process_table():
    table = Table(title="Procesos Activos", expand=True)
    table.add_column("PID", justify="right", style="cyan")
    table.add_column("Nombre", style="magenta")
    table.add_column("CPU %", justify="right", style="green")

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            table.add_row(str(proc.info['pid']),
                          proc.info['name'][:20],
                          str(proc.info['cpu_percent']))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return table

def create_dashboard():
    sys_info = get_system_info()
    net_info = get_network_info()

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["body"].split_row(
        Layout(name="system"),
        Layout(name="processes")
    )

    # Panel sistema + RAM, CPU, disco, uptime
    sys_panel = Panel(
        f"[bold cyan]CPU Núcleos:[/bold cyan] {sys_info['CPU Núcleos']}\n"
        f"[bold cyan]CPU Uso:[/bold cyan] {sys_info['CPU Uso']}%\n"
        f"[bold red]CPU Temp:[/bold red] {sys_info['CPU Temp']}\n"
        f"[bold green]RAM:[/bold green] {sys_info['RAM Usada']} / {sys_info['RAM Total']}\n"
        f"[bold yellow]Disco:[/bold yellow] {sys_info['Disk Usado']} / {sys_info['Disk Total']}\n"
        f"[bold white]Uptime:[/bold white] {sys_info['Uptime']}\n\n"
        f"[bold magenta]IP Pública:[/bold magenta] {net_info['IP Pública']}\n"
        f"[bold blue]TX:[/bold blue] {net_info['TX']} | [bold blue]RX:[/bold blue] {net_info['RX']}\n\n"
        f"[bold white]Interfaces:[/bold white]\n" +
        "\n".join([f"{m} {iface} {ip} ({mac})" for m, iface, ip, mac in net_info['Interfaces']]),
        title="📊 Información del Sistema",
        border_style="bright_blue"
    )

    # Tabla de procesos
    proc_table = get_process_table()

    layout["header"].update(
        Panel(Text("⚙️  SVAROG v2 - MONITOR DEL SISTEMA", justify="center", style="bold white on blue"))
    )
    layout["system"].update(sys_panel)
    layout["processes"].update(proc_table)
    layout["footer"].update(
        Panel(f"[green]Última actualización:[/green] {datetime.datetime.now().strftime('%H:%M:%S')}", border_style="green")
    )

    return layout

if __name__ == "__main__":
    refresh_interval = 1
    with Live(create_dashboard(), refresh_per_second=2, screen=True) as live:
        while True:
            live.update(create_dashboard())
            time.sleep(refresh_interval)
