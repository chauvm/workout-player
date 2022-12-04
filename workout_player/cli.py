"""Console script for workout_player."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("workout-player")
    click.echo("=" * len("workout-player"))
    click.echo("Small program to play workout set countdown on terminal")


if __name__ == "__main__":
    main()  # pragma: no cover
