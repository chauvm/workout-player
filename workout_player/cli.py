"""Console script for workout_player."""

import csv
import os
from time import sleep
from typing import List

import click
import playsound
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.text import Text
from workout import WorkoutSet

DEFAULT_WORKOUT = "./sample_workouts/future_full_body.csv"
DEFAULT_HEADERS = ["order", "name", "duration", "side", "description"]
DEFAULT_SET_INTERVAL = 1
DEFAULT_SWITCH_SET_ALERT = 3
DEFAULT_SWITCH_SET_SOUND = "audio/ping.mp3"

console = Console()


@click.command("play-workout")
@click.option("--workout", type=click.Path(), default=DEFAULT_WORKOUT, help="Path to a workout in CSV format")
def main(workout):
    """Small program to play workout set countdown on terminal"""
    workout_sets = _parse_workout(workout)
    _display_workout(workout_sets)


def _parse_workout(workout_path: str) -> List[WorkoutSet]:
    """Parse a workout CSV file and return a list of workout sets"""
    panel = Panel(Text(f"Starting workout from {os.path.basename(workout_path)}", justify="center", style="bold cyan"))
    print(panel)
    csv_reader = csv.reader(open(workout_path, "r"), delimiter=";")
    headers = next(csv_reader, None)
    if headers != DEFAULT_HEADERS:
        raise click.ClickException(f"Expected headers to be {DEFAULT_HEADERS}, got {headers}")

    workout_sets = [WorkoutSet(**dict(zip(headers, row))) for row in csv_reader]
    return workout_sets


def _display_workout(workout_sets: List[WorkoutSet]):
    """Render workout sets in terminal"""
    # for ws_step in track(range(len(workout_sets)), description="Workout Progress... "):
    #     ws = workout_sets[ws_step]
    #     sleep(ws.duration)
    total_sets = len(workout_sets)
    for ws in workout_sets:
        emoji = _get_emoji(ws.name)
        progress = f"{ws.order}/{total_sets}"
        text = Text(f"{progress} {ws.name}: {ws.description}")
        text.stylize("bold cyan", 0, len(progress) + 1)
        text.stylize("bold red", len(progress) + 1, len(progress) + len(ws.name) + 1)
        console.print(text)
        num_intervals = int(ws.duration / DEFAULT_SET_INTERVAL)
        for i in track(range(num_intervals), description=f"--> {emoji} "):
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
