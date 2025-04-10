import inspect
import threading
import time
import logging
import os
import tracemalloc
from rich.panel import Panel
from rich.tree import Tree
from rich.console import Console
from rich.layout import Layout
from rich.live import Live

__tracked_vars = {}
__tracked_funcs = {}
__tracked_returns = {}
__console = Console()
__log_file = "debug_logs.log"

logging.basicConfig(filename=__log_file,
                    filemode='a',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

tracemalloc.start()


def _mem_usage():
    current, peak = tracemalloc.get_traced_memory()
    return f"Current: {current / 1024:.2f} KB, Peak: {peak / 1024:.2f} KB"


def var_ins(var_name: str):
    frame = inspect.currentframe().f_back
    local_vars = frame.f_locals
    global_vars = frame.f_globals

    def watch():
        last_val, last_type = None, None
        while True:
            val = local_vars.get(var_name, global_vars.get(var_name, None))
            val_type = type(val).__name__
            if (val != last_val) or (val_type != last_type):
                log_msg = f"[var_ins] {var_name} = {val} ({val_type}) , Mem: {_mem_usage()}"
                __tracked_vars.setdefault(var_name, []).append((val, val_type, _mem_usage()))
                logging.info(log_msg)
                last_val, last_type = val, val_type
            time.sleep(0.2)

    threading.Thread(target=watch, daemon=True).start()


def func_ins(func):
    def wrapper(*args, **kwargs):
        caller = inspect.stack()[1]
        location = f"{os.path.basename(caller.filename)}:{caller.lineno}"
        mem_before = _mem_usage()
        result = func(*args, **kwargs)
        mem_after = _mem_usage()

        log_call = f"[func_ins] {func.__name__}() at {location}, args={args}, kwargs={kwargs}, Mem Before={mem_before}"
        log_return = f"[func_return] {func.__name__}() returned {result} at {location}, Mem After={mem_after}"

        __tracked_funcs.setdefault(func.__name__, []).append((args, kwargs, location, mem_before))
        __tracked_returns.setdefault(func.__name__, []).append((result, location, mem_after))

        logging.info(log_call)
        logging.info(log_return)

        return result

    return wrapper


def render_ui():
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )

    layout["body"].split_row(
        Layout(name="variables"),
        Layout(name="functions"),
        Layout(name="returns")
    )

    layout["header"].update(Panel("[bold magenta]📊 Live Debugger Panel - bugly.py || xspoilt-dev[/bold magenta]"))
    layout["footer"].update(Panel(f"[cyan]Memory[/cyan]: {_mem_usage()}"))

    var_tree = Tree("🧠 [bold yellow]Variable Changes[/bold yellow]")
    for var, changes in __tracked_vars.items():
        branch = var_tree.add(f"[bold green]{var}[/bold green]")
        for val, val_type, mem in changes[-3:]:
            branch.add(f"{val} ({val_type}) — [red]{mem}[/red]")
    layout["variables"].update(Panel(var_tree))

    func_tree = Tree("🚀 [bold cyan]Function Calls[/bold cyan]")
    for fname, calls in __tracked_funcs.items():
        branch = func_tree.add(f"[bold magenta]{fname}()[/bold magenta]")
        for args, kwargs, loc, mem in calls[-3:]:
            branch.add(f"[yellow]{loc}[/yellow] - args={args}, kwargs={kwargs} — [red]{mem}[/red]")
    layout["functions"].update(Panel(func_tree))

    return_tree = Tree("🔁 [bold green]Return Values[/bold green]")
    for fname, rets in __tracked_returns.items():
        branch = return_tree.add(f"[bold blue]{fname}()[/bold blue]")
        for ret, loc, mem in rets[-3:]:
            branch.add(f"[yellow]{loc}[/yellow] → [cyan]{ret}[/cyan] — [red]{mem}[/red]")
    layout["returns"].update(Panel(return_tree))

    return layout


def live_trace():
    with Live(render_ui(), refresh_per_second=5, screen=True) as live:
        while True:
            try:
                live.update(render_ui())
                time.sleep(0.2)
            except KeyboardInterrupt:
                break
        __console.print("[bold red]❌ Exiting live trace...[/bold red]")
        __console.print("[bold green]👋 Goodbye![/bold green]")
        logging.info("Live tracing ended.")
        
