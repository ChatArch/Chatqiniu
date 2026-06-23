"""CLI entrypoint for chatqiniu."""

from __future__ import annotations

import json

import click
from chatstyle import (
    CommandField,
    CommandSchema,
    add_interactive_option,
    render_success,
    resolve_command_inputs,
)

from .apps import find_app, load_apps, remove_app, resolve_registry_path, upsert_app


ADD_SCHEMA = CommandSchema(
    name="add",
    fields=(
        CommandField("name", prompt="app name", required=True),
        CommandField("endpoint", prompt="app endpoint", required=True),
    ),
)
APP_SCHEMA = CommandSchema(
    name="app",
    fields=(CommandField("name", prompt="app name", required=True),),
)


@click.group()
def main() -> None:
    """Manage Qiniu lightweight app entries."""


@main.command("list")
@click.option("--registry", type=click.Path(dir_okay=False, path_type=str), help="App registry JSON path.")
@click.option("--json", "as_json", is_flag=True, help="Print raw JSON.")
def list_apps(registry: str | None, as_json: bool) -> None:
    """List managed lightweight apps."""

    apps = load_apps(registry)
    if as_json:
        click.echo(json.dumps([app.to_dict() for app in apps], ensure_ascii=False, indent=2))
        return
    if not apps:
        click.echo("No apps configured.")
        return
    for app in apps:
        title = f" ({app.title})" if app.title else ""
        click.echo(f"{app.name}{title}: {app.endpoint}")


@main.command()
@click.argument("name", required=False)
@click.option("--endpoint", help="Lightweight app entry URL or service endpoint.")
@click.option("--title", default="", show_default=False, help="Human readable app title.")
@click.option("--description", default="", show_default=False, help="App description.")
@click.option("--registry", type=click.Path(dir_okay=False, path_type=str), help="App registry JSON path.")
@add_interactive_option
def add(
    name: str | None,
    endpoint: str | None,
    title: str,
    description: str,
    registry: str | None,
    interactive: bool | None,
) -> None:
    """Add or update a lightweight app entry."""

    values = resolve_command_inputs(
        schema=ADD_SCHEMA,
        provided={"name": name, "endpoint": endpoint},
        interactive=interactive,
        usage="Usage: chatqiniu add [NAME] --endpoint URL [-i|-I]",
    )
    app = upsert_app(
        name=values["name"],
        endpoint=values["endpoint"],
        title=title,
        description=description,
        path=registry,
    )
    render_success(f"Saved {app.name} -> {app.endpoint}")


@main.command()
@click.argument("name", required=False)
@click.option("--registry", type=click.Path(dir_okay=False, path_type=str), help="App registry JSON path.")
@click.option("--json", "as_json", is_flag=True, help="Print raw JSON.")
@add_interactive_option
def show(name: str | None, registry: str | None, as_json: bool, interactive: bool | None) -> None:
    """Show one lightweight app entry."""

    values = resolve_command_inputs(
        schema=APP_SCHEMA,
        provided={"name": name},
        interactive=interactive,
        usage="Usage: chatqiniu show [NAME] [-i|-I]",
    )
    app = find_app(values["name"], registry)
    if app is None:
        raise click.ClickException(f"App not found: {values['name']}")
    if as_json:
        click.echo(json.dumps(app.to_dict(), ensure_ascii=False, indent=2))
        return
    click.echo(f"name: {app.name}")
    click.echo(f"endpoint: {app.endpoint}")
    if app.title:
        click.echo(f"title: {app.title}")
    if app.description:
        click.echo(f"description: {app.description}")


@main.command()
@click.argument("name", required=False)
@click.option("--registry", type=click.Path(dir_okay=False, path_type=str), help="App registry JSON path.")
@add_interactive_option
def remove(name: str | None, registry: str | None, interactive: bool | None) -> None:
    """Remove a lightweight app entry."""

    values = resolve_command_inputs(
        schema=APP_SCHEMA,
        provided={"name": name},
        interactive=interactive,
        usage="Usage: chatqiniu remove [NAME] [-i|-I]",
    )
    if not remove_app(values["name"], registry):
        raise click.ClickException(f"App not found: {values['name']}")
    render_success(f"Removed {values['name']}")


@main.command()
@click.option("--registry", type=click.Path(dir_okay=False, path_type=str), help="App registry JSON path.")
def path(registry: str | None) -> None:
    """Print the registry path Chatqiniu will use."""

    click.echo(str(resolve_registry_path(registry)))


if __name__ == "__main__":
    main()
