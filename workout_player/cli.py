"""Console script for workout_player."""

import csv
from typing import List

import click
from rich.pretty import pprint
from workout import WorkoutSet

DEFAULT_WORKOUT = "./sample_workouts/future_full_body.csv"
DEFAULT_HEADERS = ["order", "name", "duration", "side", "description"]


@click.command("play-workout")
@click.option("--workout", type=click.Path(), default=DEFAULT_WORKOUT, help="Path to a workout in CSV format")
def main(workout):
    """Small program to play workout set countdown on terminal"""
    workout_sets = _parse_workout(workout)
    _display_workout(workout_sets)


def _parse_workout(workout_path: str) -> List[WorkoutSet]:
    """Parse a workout CSV file and return a list of workout sets"""
    click.echo("_parse_workout")
    csv_reader = csv.reader(open(workout_path, "r"), delimiter=";")
    headers = next(csv_reader, None)
    if headers != DEFAULT_HEADERS:
        raise click.ClickException(f"Expected headers to be {DEFAULT_HEADERS}, got {headers}")

    workout_sets = [WorkoutSet(**dict(zip(headers, row))) for row in csv_reader]
    return workout_sets


def _display_workout(workout_sets: List[WorkoutSet]):
    """Render workout sets in terminal"""
    click.echo("_display_workout")
    for ws in workout_sets:
        pprint(ws)


if __name__ == "__main__":
    main()  # pragma: no cover
