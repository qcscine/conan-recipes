__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

import pytz
import requests
import sys
from datetime import datetime, timedelta


class ArtifactoryAPI(object):
    def __init__(self, api_base, auth):
        """ Initialize API class with base URI and authentication tuple """
        self.api_base = api_base
        self.auth = auth

    def api(self, path):
        return "/".join([self.api_base, path])

    def get_conan_repositories(self):
        """ Fetch list of conan repositories in the artifactory """
        api_path = self.api("api/repositories?type=local&packageType=conan")
        r = requests.get(api_path, auth=self.auth)
        if not r.ok:
            msg = "Got response {} for GET {}".format(r.status_code, api_path)
            raise RuntimeError(msg)

        return [d["key"] for d in r.json()]

    def get_path_list_base(self, repo, path):
        """ Base fn for directory listings """
        api_path = self.api("api/storage/{}/{}".format(repo, path))
        r = requests.get(api_path, auth=self.auth)
        if not r.ok:
            msg = "Got response {} for GET {}".format(r.status_code, api_path)
            raise RuntimeError(msg)

        return r.json()

    def get_subdirectories(self, repo, path):
        """ Get list of subdirectories for a path """
        listing = self.get_path_list_base(repo, path)
        return [d["uri"].lstrip("/") for d in listing["children"] if d["folder"]]

    def get_last_updated(self, repo, path):
        """ Get date object for last updated time of a path """
        # Only in Python 3.7 onwards does %z correclty interpret +01:00 suffix
        # to date format

        if sys.version_info.major >= 3 and sys.version_info.minor >= 7:
            date_str = self.get_path_list_base(repo, path)["lastUpdated"]
            date_format_str = "%Y-%m-%dT%H:%M:%S.%f%z"
            return datetime.strptime(date_str, date_format_str)

        date_str = self.get_path_list_base(repo, path)["lastUpdated"]
        plus_idx = date_str.index("+")
        date_str = date_str[:plus_idx]
        date_format_str = "%Y-%m-%dT%H:%M:%S.%f"
        return datetime.strptime(date_str, date_format_str)

    def older_than(self, delta, repo, path):
        """ Returns if a package is older than a supplied time delta """
        last_updated = self.get_last_updated(repo, path)
        if sys.version_info.major >= 3 and sys.version_info.minor >= 7:
            now = datetime.now(pytz.utc)
        else:
            now = datetime.now()
        return (now - last_updated) > delta

    def delete(self, repo, path):
        """ Deletes a path from the artifactory """
        api_path = self.api("{}/{}".format(repo, path))
        r = requests.delete(api_path, auth=self.auth)
        if not r.ok:
            raise RuntimeError(
                "Got response {} for DELETE {}".format(r.status_code, api_path)
            )

    def list_old_packages(self, repo, user, old_package_delta=timedelta(days=1), preserve_channels=["stable", "master"], preserve_newest=3):
        """
        Lists old packages that could be deleted

        Descends along user-name-version-channel folder hierarchy. In each
        channel folder:

        - If a channel is in preserve_channels, skips the channel
        - Sorts packages by age
        - Preserves newest packages as specified by preserve_newest
        - Selects packages older than old_package_delta

        Returns a list of full paths to package directories
        """
        if sys.version_info.major >= 3 and sys.version_info.minor >= 7:
            now = datetime.now(pytz.utc)
        else:
            now = datetime.now()

        old_packages = []
        for name in self.get_subdirectories(repo, user):
            inc_path = "/".join([user, name])
            for version in self.get_subdirectories(repo, inc_path):
                inc_path = "/".join([user, name, version])
                for channel in self.get_subdirectories(repo, inc_path):
                    if channel in preserve_channels:
                        continue

                    pkgs_path = "/".join([user, name, version, channel])

                    def lookup_age(pkg):
                        return self.get_last_updated(repo, "/".join([pkgs_path, pkg]))

                    pkgs = self.get_subdirectories(repo, pkgs_path)
                    # Sort packages by date created (newer first, older last)
                    sorted_pkgs = sorted(pkgs, key=lookup_age, reverse=True)
                    # Always preserve n newest packages
                    non_preserved = sorted_pkgs[preserve_newest:]
                    # Select packages older than set delta
                    older_pkgs = [pkg for pkg in non_preserved
                                  if now - lookup_age(pkg) > old_package_delta]

                    # Add to old packages
                    old_packages.extend(
                        ["/".join([pkgs_path, pkg]) for pkg in older_pkgs]
                    )

        return old_packages
