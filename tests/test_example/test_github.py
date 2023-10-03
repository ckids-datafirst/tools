import os

import pytest
from github import Github
from github.Organization import Organization

from datafirst_tools.github_methods import (
    add_members_to_team,
    add_repository_to_team,
    check_team_exists,
    create_team,
    delete_team,
    get_organization,
    get_repo_by_organization,
    get_team,
    get_user,
    has_in_members,
    invite_user_to_organization,
    is_user_part_of_organization,
)


def test_user_exists(client: Github):
    """Test check_user_exists"""
    get_user("mosoriob", client)
    with pytest.raises(Exception) as e:
        print(e)
        get_user("mosoriobasdfasfdqsd", client)


def test_check_user_is_member(
    client: Github,
    organization: Organization,
):
    """Test check_user_is_member"""
    user = get_user("mosoriobnew", client)
    is_user_part_of_organization(user, organization)


def test_check_team_exists(organization: Organization):
    """Test check_team_exists"""
    assert check_team_exists("2023-fall", organization) == True
    assert check_team_exists("2023-fall-not-found", organization) == False


def test_create_team(organization: Organization):
    """Test create_team"""
    create_team("test-team", "test-team", organization)


def test_invite_user_to_organization(client: Github, organization: Organization):
    """Test invite_user_to_organization"""
    user = get_user("mosoriobnew", client)
    invite_user_to_organization(user, organization)


def test_get_team(organization: Organization):
    """Test check_team_exists"""
    get_team("2023-fall", organization)


def test_check_repository_exists(organization: Organization):
    """Test check_repository_exists"""
    get_repo_by_organization("website", organization)


def test_add_members_to_team(organization: Organization, client: Github):
    """Test add_members_to_team"""
    user = get_user("mosoriobnew", client)
    team = get_team("2023-fall", organization)
    add_members_to_team(user, team)


def test_has_in_members(client: Github, organization: Organization):
    """Test has_in_members"""
    user = get_user("mosoriob", client)
    team = get_team("2023-fall", organization)
    has_in_members(user, team)


def test_delete_team(organization: Organization):
    """Test delete_team"""
    team = get_team("test-team", organization)
    delete_team(team)
