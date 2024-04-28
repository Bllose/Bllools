

def inspect_exampl():
    my_list = ['foo', 'bar']
    from rich import inspect
    inspect(my_list, methods=True)

    from tcl.mbyq_cmd import mbyq
    inspect(mbyq, methods=True)

def progress_example():
    import time
    from rich.progress import Progress
    
    with Progress() as progress:
        task1 = progress.add_task("[red]Doing Task 1", total=100)
        task2 = progress.add_task("[blue]Doing Task 2", total=40)
        task3 = progress.add_task("[green]Doing Task 3", total=500)
        
        while not progress.finished:
            progress.update(task1, advance=0.1)
            progress.update(task2, advance=0.3)
            progress.update(task3, advance=0.6)
            time.sleep(0.01)


def tree_example():
    # rich-tree.py
    from rich.console import Console
    from rich.tree import Tree
    
    console = Console(width=100)
    tree = Tree("Programming Languages")
    
    python_tree = tree.add("[b green]Python[/]")
    python_tree.add("Numpy")
    python_tree.add("Pandas")
    python_tree.add("Django")
    python_tree.add("Flask")
    
    java_tree = tree.add("[b dark_orange3]Java[/]")
    java_tree.add("Spring")
    java_tree.add("Apache")
    
    frameworks = ["Express", "React", "Next", "Vue", "Angular"]
    js_tree = tree.add("[b yellow]Javascript[/]")
    for framework in frameworks:
        js_tree.add(framework)
        
    console.print(tree)
    
    CONSOLE_HTML_FORMAT = """\
    <pre style="font-family:Menlo">{code}</pre>
    """



def md_example():
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    with open("sample.md") as readme:
        markdown = Markdown(readme.read())
    console.print(markdown)



def colorful_table_example():
    from rich.align import Align
    from rich.console import Console
    from rich.live import Live
    from rich.table import Table

    TABLE_DATA = [
        [
            "[b white]DSA Course[/]: [i]Beginner[/]",
            "[magenta][/]10",
            "[green]Geeks for Geeks[/]",
            "15 hours",
        ],
        [
            "[b white]DSA Course[/]: [i]Intermediate[/]",
            "[magenta][/]20",
            "[green]Geeks for Geeks[/]",
            "25 hours",
        ],
        [
            "[b white]DSA Course[/]: [i]Advanced[/]",
            "[magenta][/]30",
            "[green]Geeks for Geeks[/]",
            "30 hours",
        ],
        [
            "[b white]Operating System Fundamentals[/]",
            "[magenta][/]25",
            "[green]Geeks for Geeks[/]",
            "35 hours",
        ],
    ]

    console = Console()
    table = Table(show_footer=False)
    table_centered = Align.center(table)

    console.clear()

    with Live(table_centered, console=console, screen=False):
        table.add_column("Course Name", no_wrap=True)
        table.add_column("Price", no_wrap=True)
        table.add_column("Organization", no_wrap=True)
        table.add_column("Duration", no_wrap=True)
        for row in TABLE_DATA:
            table.add_row(*row)
        table_width = console.measure(table).maximum
        table.width = None



def processing_task_example():
    from time import sleep
    from rich.console import Console
    console = Console()
    tasks = [f'Task {n}' for n in range(1, 8)]

    with console.status('[bold dark_orange]Finishing tasks...') as status:
        while tasks:
            task = tasks.pop(0)
            sleep(1)
            console.log(f'{task} complete')

if __name__ == '__main__':
    # processing_task_example()          
    # colorful_table_example()
    # md_example()
    # tree_example()
    # progress_example()
    inspect_exampl()
