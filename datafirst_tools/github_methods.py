from typing import Union

from github import Auth, Github
from github.AuthenticatedUser import AuthenticatedUser
from github.NamedUser import NamedUser
from github.Organization import Organization
from github.Repository import Repository
from github.Team import Team

# headers = {
#     "Accept": "application/vnd.github+json",
#     "Authorization": f"Bearer {TOKEN}",
#     "X-GitHub-Api-Version": "2022-11-28",
# }
# def create_repository_using_template(name: str, description: str, organization: str):
#     data = {
#         "owner": ORGANIZATION,
#         "name": name,
#         "description": description,
#         "include_all_branches": False,
#         "private": False,
#     }
#     response = requests.post(
#         f"https://api.github.com/repos/{ORGANIZATION}/{TEMPLATE_REPO}/generate",
#         headers=headers,
#         data=data,
#     )
#     if response.status_code != 201:
#         raise Exception("Failed to create repository using template")
#     return response.json()["full_name"]


def get_repo_by_organization(name: str, organization: Organization) -> Repository:
    return organization.get_repo(name)


def get_team(name: str, organization: Organization) -> Team:
    return organization.get_team_by_slug(name)


def add_members_to_team(user: NamedUser | AuthenticatedUser, team: Team):
    """Add members to a team"""
    if isinstance(user, AuthenticatedUser):
        raise Exception("AuthenticatedUser is not supported")
    else:
        team.add_membership(user)


def has_in_members(user: NamedUser | AuthenticatedUser, team: Team) -> bool:
    """Check if a user is a member of a team"""
    if isinstance(user, AuthenticatedUser):
        raise Exception("AuthenticatedUser is not supported")
    return team.has_in_members(user)


def delete_team(team: Team):
    """Delete a team"""
    team.delete()


def add_repository_to_team(repository: Repository, team: Team):
    """Add a repository to a team"""
    team.add_to_repos(repository)


def create_team(
    name: str,
    description: str,
    organization: Organization,
    repo_names: list[str] = [],
) -> Team:
    """Create a new team"""
    return organization.create_team(
        name=name,
        description=description,
        privacy="closed",
        permission="push",
    )


def invite_user_to_organization(
    user: NamedUser | AuthenticatedUser,
    organization: Organization,
    teams: list[Team] = [],
):
    """Invite a user to the organization"""
    if isinstance(user, AuthenticatedUser):
        raise Exception("AuthenticatedUser is not supported")
    else:
        organization.invite_user(
            user,
            teams=teams,
        )


def get_user(username: str, client: Github) -> Union[NamedUser, AuthenticatedUser]:
    """Check if a user exists by username on github"""
    return client.get_user(username)


def check_user_is_member(
    user: Union[NamedUser, AuthenticatedUser], organization: Organization
) -> bool:
    """Check if a user is a member of the organization"""
    if isinstance(user, AuthenticatedUser):
        raise Exception("AuthenticatedUser is not supported")
    else:
        return organization.has_in_members(user)


def get_organization(organization: str, client: Github) -> Organization:
    """Get the organization"""
    return client.get_organization(organization)
