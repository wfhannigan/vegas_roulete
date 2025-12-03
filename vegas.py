import argparse
import time
from random import randint as random_integer
from rich import print as rprint
from rich.console import Console
from rich.status import Status

def is_odd(number: int) -> bool:
     return number % 2 == 1

def is_even(number: int) -> bool:
     return number % 2 == 0

def show_spinning_wheel(spin_time: float):
    with Status("[italic]Roulete Wheel Noises[/italic]", spinner="dots") as status:
        start_time = time.time()

        while time.time() - start_time < spin_time:
            time.sleep(0.1)
            elapsed = int(time.time() - start_time)
            status.update()

def spin_wheel() -> int:
    my_num = random_integer(0,35)
    if my_num == 0:
        rprint(f"[bold green]{my_num}[/bold green]")
    elif is_odd(my_num):
        rprint(f"[bold white]{my_num}[/bold white]")
    elif is_even(my_num):
        rprint(f"[bold red]{my_num}[/bold red]")
    return my_num

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-spins", type=int, default=1, required=False)
    parser.add_argument("--spin-time", type=float, default=4.0, required=False)
    args = parser.parse_args()

    for _ in range(args.num_spins):
        show_spinning_wheel(args.spin_time)
        spin_wheel()