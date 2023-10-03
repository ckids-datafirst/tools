from typing import Annotated

import os
from pathlib import Path

import typer
from github import Auth, Github
from github.Organization import Organization

from datafirst_tools.database_methods import (
    close_database,
    get_cursor,
    get_members_of_team,
    get_projects_by_semester,
    get_students_by_semester,
    open_database,
)
from datafirst_tools.github_methods import (
    add_members_to_team,
    check_team_exists,
    create_team,
    get_team,
    get_user,
    has_in_members,
    invite_user_to_organization,
    is_user_part_of_organization,
)

ORGANIZATION = "ckids-datafirst"

if (
    "GITHUB_TOKEN" in os.environ
    and os.environ.get("GITHUB_TOKEN") != ""
    and os.environ.get("GITHUB_TOKEN") != None
):
    token = os.environ.get("GITHUB_TOKEN")
else:
    print("GITHUB_TOKEN environment variable is not set")
    exit(1)

auth = Auth.Token(token)
client = Github(auth=auth)
organization = client.get_organization(ORGANIZATION)


app = typer.Typer()


@app.command(
    name="invite-students", help="Invite students to DataFirst Organization on GitHub"
)
def invite_students(
    database_file: Annotated[
        Path,
        typer.Argument(help="DataFirst sqlite3 file", default=None),
    ],
    semester: Annotated[
        str,
        typer.Argument(help="Semester to create teams for", default=None),
    ],
    year: Annotated[
        str,
        typer.Argument(
            help="Year to create teams for",
            default=None,
        ),
    ],
) -> None:
    if not database_file or database_file.exists() is False:
        raise typer.Exit(code=1)
    connection = open_database(database_file)
    cursor = get_cursor(connection)
    students = get_students_by_semester(cursor, semester, year)
    send_invitation(students)
    close_database(connection)


def send_invitation(students: list[dict[str, str | None]]):
    for student in students:
        username = student["github_username"]
        name = student["name"]
        if username != None:
            try:
                user = get_user(username, client)
                if user:
                    if not is_user_part_of_organization(user, organization):
                        print(
                            f"""Invite {name} ({username}) to DataFirst Organization on GitHub"""
                        )
                        invite_user_to_organization(user, organization)
            except:
                continue


@app.command(
    name="create-teams",
    help="Create one team per project in DataFirst Organization on GitHub",
)
def create_teams(
    database_file: Annotated[
        Path,
        typer.Argument(help="DataFirst sqlite3 file", default=None),
    ],
    semester: Annotated[
        str,
        typer.Argument(help="Semester to create teams for", default=None),
    ],
    year: Annotated[
        str,
        typer.Argument(help="Year to create teams for", default=None),
    ],
) -> None:
    connection = open_database(database_file)
    cursor = get_cursor(connection)
    projects = get_projects_by_semester(cursor, semester, year)
    for project in projects:
        members = get_members_of_team(cursor, project["id"])
        create_team_for_project(project, semester, year, members)
    close_database(connection)


def create_team_for_project(
    project: dict[str, str], semester: str, year: str, members: list[str]
):
    project_id = project["id"]
    project_name = project["name"]
    team_name = f"{project_id}"
    team_description = f"Team for {project_name} ({year} {semester})"
    if not check_team_exists(team_name, organization):
        team = create_team(team_name, team_description, organization)
    else:
        team = get_team(team_name, organization)

    for member in members:
        try:
            user = get_user(member, client)
        except:
            print(f"User {member} not found")
            continue
        if user and not has_in_members(user, team):
            add_members_to_team(user, team)


@app.command(
    name="create-website-repositories",
    help="Create one website repository per project in DataFirst Organization on GitHub",
)
def create_website_repositories(
    database_file: Annotated[
        Path,
        typer.Argument(help="DataFirst sqlite3 file", default=None),
    ],
    semester: Annotated[
        str,
        typer.Argument(help="Semester to create teams for", default=None),
    ],
    year: Annotated[
        str,
        typer.Argument(help="Year to create teams for", default=None),
    ],
) -> None:
    pass


if __name__ == "__main__":
    app()
