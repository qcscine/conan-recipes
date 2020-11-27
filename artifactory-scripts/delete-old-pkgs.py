__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

from artifactory_api import ArtifactoryAPI
import sys

"""
NOTE:
- Conan package order: name/version@user/channel
  E.g. scine_molassembler/1.0.0@ci/develop
- Artifactory storage order: user/name/version/channel
  E.g. ci/scine_molassembler/version/develop

"""

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise RuntimeError(
            "Supply the Artifactory repository URL (e.g. http://localhost:8082/artifactory/api/conan/scine-internal), a username and password as arguments")

    full_api = sys.argv[1]

    # Determine api base part
    splat = full_api.split("/")
    api_idx = splat.index("api")
    api_base = "/".join(splat[:api_idx])
    repo_name = splat[-1]

    user = sys.argv[2]
    passw = sys.argv[3]

    api = ArtifactoryAPI(api_base=api_base, auth=(user, passw))
    old_pkgs = api.list_old_packages(repo_name, "scine")
    for pkg in old_pkgs:
        print("{}: {}".format(pkg, api.get_last_updated(repo_name, pkg)))
        api.delete(repo_name, pkg)
