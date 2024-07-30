#!/usr/bin/env python3
"""
Test module for client module
"""

from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import unittest
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for `GithubOrgClient` class
    """

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name: str, mock_get: Mock) -> None:
        """
        Test `org` property returns expected result
        """
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"payload": True})
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get.assert_called_once_with(url)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org) -> None:
        """
        Test `_public_repos_url` property returns expected result
        """
        mock_org.return_value = {"repos_url": "url"}
        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, "url")

    @patch("client.get_json",
           return_value=[{"name": "repo1"},
                         {"name": "repo2"}])
    def test_public_repos(self, mock_get_json) -> None:
        """
        Test `public_repos` method returns expected result
        """
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = "url"
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result) -> None:
        """
        Test `has_license` method returns expected result
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.has_license(
                repo,
                license_key),
            expected_result)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD["org_payload"],
        "repos_payload": TEST_PAYLOAD["repos_payload"],
        "expected_repos": TEST_PAYLOAD["expected_repos"],
        "apache2_repos": TEST_PAYLOAD["apache2_repos"],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test case for `GithubOrgClient` class
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up test case before running tests
        """
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return MockResponse(cls.repos_payload)

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up test case after running tests
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Test `public_repos` method returns expected result
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test `public_repos` method with license filter returns expected result
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(
                license="apache-2.0"),
            self.apache2_repos)


class MockResponse:
    """
    MockResponse class to simulate requests response
    """

    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data
