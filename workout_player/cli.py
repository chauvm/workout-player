"""Console script for workout_player."""

import csv
import os
from time import sleep
from typing import List

import click
import playsound
from rich import print
from rich.console import Console
from rich.progress import track
from rich.prompt import IntPrompt
from rich.text import Text
from workout import WorkoutSet

SAMPLE_WORKOUT_DIR = "./sample_workouts/"
DEFAULT_WORKOUT = "./sample_workouts/future_full_body.csv"
DEFAULT_PRE_WORKOUT_WAIT = 3
DEFAULT_HEADERS = ["order", "name", "duration", "side", "description"]
DEFAULT_SET_INTERVAL = 1
DEFAULT_SWITCH_SET_ALERT = 3
DEFAULT_SWITCH_SET_SOUND = "audio/ping.mp3"

console = Console()


@click.command("play-workout")
@click.option("--workout", type=click.Path(), default=None, help="Path to a workout in CSV format")
def main(workout):
    """Small program to play workout set countdown on terminal"""
    if workout is None:
        workout = _prompt_workout_selection()
    _display_pre_workout(workout)
    workout_sets = _parse_workout(workout)
    _display_workout(workout_sets)


def _display_pre_workout(workout_path: str):
    for _ in track(
        range(DEFAULT_PRE_WORKOUT_WAIT),
        description=f"Get ready in {DEFAULT_PRE_WORKOUT_WAIT} seconds! ",
        transient=True,
    ):
        playsound.playsound(DEFAULT_SWITCH_SET_SOUND)
    print("\n")


def _parse_workout(workout_path: str) -> List[WorkoutSet]:
    """Parse a workout CSV file and return a list of workout sets"""
    csv_reader = csv.reader(open(workout_path, "r"), delimiter=";")
    headers = next(csv_reader, None)
    if headers != DEFAULT_HEADERS:
        raise click.ClickException(f"Expected headers to be {DEFAULT_HEADERS}, got {headers}")

    workout_sets = [WorkoutSet(**dict(zip(headers, row))) for row in csv_reader]
    return workout_sets


def _prompt_workout_selection() -> str:
    print("[bold cyan]Choose a workout to start from this list...[/bold cyan]")
    workouts = [f for f in os.listdir(SAMPLE_WORKOUT_DIR) if f.endswith(".csv")]
    for i, w in enumerate(workouts):
        print(f"[cyan]{i+1}. [/cyan][bold red]{w}[/bold red]")

    order = IntPrompt.ask(f"[bold cyan]...enter a number from [red]1[/red] to [red]{len(workouts)}[/red][/bold cyan]")
    try:
        order = int(order)
        if not (1 <= order <= len(workouts)):
            raise ValueError
    except ValueError:
        raise click.ClickException(f"Expected a number from 1 to {len(workouts)}, got {order}")

    chosen = workouts[order - 1]
    print("\n")
    console.rule(f"[bold cyan]Workout [bold red]{chosen}[/bold red] selected![/bold cyan]", style="cyan")
    chosen_path = os.path.join(SAMPLE_WORKOUT_DIR, chosen)
    return chosen_path


def _display_workout(workout_sets: List[WorkoutSet]):
    """Render workout sets in terminal"""
    total_sets = len(workout_sets)
    for ws in workout_sets:
        _display_set_description(ws, total_sets)
        _display_set_progress_bar(ws)


def _display_set_description(ws: WorkoutSet, total_sets: int):
    # construct set progress, e.g. " 2/50"
    progress = f"{ws.order}/{total_sets}"
    if ws.order < 10:
        progress = " " + progress

    # construct set text
    text = Text(f"{progress} {ws.name}: {ws.description}")
    text.stylize("bold cyan", 0, len(progress) + 1)
    text.stylize("bold red", len(progress) + 1, len(progress) + len(ws.name) + 1)

    console.print(text)


def _display_set_progress_bar(ws: WorkoutSet):
    # construct set progress bar
    emoji = _get_emoji(ws.name)
    num_intervals = int(ws.duration / DEFAULT_SET_INTERVAL)
    for i in track(range(num_intervals), description=f"--> {emoji} ", transient=True):
        if num_intervals - i > DEFAULT_SWITCH_SET_ALERT:
            sleep(DEFAULT_SET_INTERVAL)
        else:
            playsound.playsound(DEFAULT_SWITCH_SET_SOUND)


def _get_emoji(name: str) -> str:
    if name.lower() == "recover":
        return ":palm_tree:"
    else:
        return ":running:"


if __name__ == "__main__":
    main()  # pragma: no cover
