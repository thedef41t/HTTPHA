from .sender import send_request
import time
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.rich_console import r_console
from rich.table import Table
from rich.panel import Panel
from .status_codes import analyze_status_code
from .header_checker import request_header_checker

def verify_web(target_url: str) -> dict:
    """ it verifies if the given website is rechable before testing. """

    status_code = 0
    req_headers = {}
    is_rechable = False

    start = time.perf_counter()
    
    try:

        with Progress(
            SpinnerColumn(spinner_name="boxBounce"),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as pr:

            task = pr.add_task(f"[red] Looking for http status code...\n", total=None)
            response = send_request(target_url)

            if response:
                status_code = response.get("status_code", 0)
                req_headers = response.get("headers", {})
                pr.update(task, description="Checking headers...", total=None)
                status_info = analyze_status_code(status_code)
                is_reachable = status_info["is_reachable"]
                vulnerable_headers = request_header_checker(req_headers)
            else:
                status_info = {
                    "category": "No Response",
                    "description": "Connection failed",
                    "color": "red"
                }
                is_reachable = False

        # ----------------------------------------------------------------------------------------------
        if is_reachable:
            table = Table.grid(padding=(0, 2))
            table.add_column(justify="right", no_wrap=True)
            table.add_column()
            table.add_row("[red]URL:[/]", f"{target_url}"),
            table.add_row(
                "[red]Status:[/]",
                f"[{status_info["color"]}]{status_info["category"]}[/]"
            )
            table.add_row(
                "[red]Description[/]",
                f"[{status_info["color"]}]{status_info["description"]}[/]"
            )
            table.add_row(
                "[red]Is Reachable[/]",
                f"[{status_info["color"]}]{status_info["is_reachable"]}[/]"
            )
            r_console.print(Panel(table, title="Request result"))
            print()
        else:
            table = Table.grid(padding=(0, 2))
            table.add_column(justify="right", no_wrap=True)
            table.add_column()
            table.add_row("[red]URL:[/]", f"{target_url}"),
            table.add_row(
                "[red]Status:[/]",
                f"[{status_info["color"]}]{status_info["category"]}[/]"
            )
            table.add_row(
                "[red]Description[/]",
                f"[{status_info["color"]}]{status_info["description"]}[/]"
            )
            table.add_row(
                "[red]Is Reachable[/]",
                f"[{status_info["color"]}]{status_info["is_reachable"]}[/]"
            )
            r_console.print(Panel(table, title="Request result"))
            print()
        # ----------------------------------------------------------------------------------------------  

        # ----------------------------------------------------------------------------------------------
        if req_headers:
            table = Table(title=f"Response headers for [red]{target_url}[/]")
            table.add_column("Header", justify="left", no_wrap=True)
            table.add_column("Value", justify="left", no_wrap=True)
            for header, directive in req_headers.items():
                table.add_row(header ,str(directive))
            r_console.print(table)
            print()
        else:
            r_console.print("[[red]Error[/]] No headers received!")
        # ----------------------------------------------------------------------------------------------
        
        # ----------------------------------------------------------------------------------------------
        if vulnerable_headers:
            for list in vulnerable_headers:
                vulnerable_header = list.get("header", "unknown")
                vulnerable_message = list.get("message", "No description")
            table = Table(title=f"Potential vulnerabilities in [red]{target_url}[/]", style="red")
            table.add_column("Header", justify="left", no_wrap=True)
            table.add_column("Description", justify="left", no_wrap=True)
            table.add_row(vulnerable_header, vulnerable_message)
            r_console.print(table)
        else:
            r_console.print("HTTP headers are securely configurued!")
        # ----------------------------------------------------------------------------------------------

    except Exception:
        r_console.print(f"[Error]: {error}")

    end = time.perf_counter() - start

    return {
        "status_code": status_code,
        "headers": req_headers,
        "is_reachable": is_reachable,
        "end": end
        
    }
