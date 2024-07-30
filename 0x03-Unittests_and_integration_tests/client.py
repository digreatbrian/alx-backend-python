#!/usr/bin/env python3
"""A GitHub organization client module for fetching organization and repository information from GitHub API."""

from typing import List, Dict
from utils import get_json, access_nested_map, memoize

class GithubOrgClient:
    """A GitHub organization client."""
    
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """
        Initialize the GithubOrgClient with the organization name.

        Args:
            org_name (str): The name of the GitHub organization.
        """
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """
        Fetch and memoize the organization information from GitHub API.

        Returns:
            Dict: The organization information as a dictionary.
        """
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """
        Get the URL to fetch public repositories of the organization.

        Returns:
            str: The URL for the organization's public repositories.
        """
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """
        Fetch and memoize the payload of the organization's public repositories.

        Returns:
            Dict: The payload data of the organization's public repositories.
        """
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """
        Get a list of the organization's public repositories, optionally filtered by license.

        Args:
            license (str, optional): The license key to filter repositories by. Defaults to None.

        Returns:
            List[str]: A list of public repository names.
        """
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]
        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """
        Check if a repository has a specific license.

        Args:
            repo (Dict[str, Dict]): The repository information.
            license_key (str): The license key to check for.

        Returns:
            bool: True if the repository has the specified license, False otherwise.
        """
        assert license_key is not None, "license_key cannot be None"
        try:
            has_license = access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
        return has_license
