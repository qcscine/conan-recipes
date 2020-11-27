__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

from conans.client.command import Command, Conan
import sys

rehost_packages = [
    "boost_assert/1.69.0@bincrafters/stable",
    "boost_base/1.69.0@bincrafters/stable",
    "boost_config/1.69.0@bincrafters/stable",
    "boost_container_hash/1.69.0@bincrafters/stable",
    "boost_core/1.69.0@bincrafters/stable",
    "boost_detail/1.69.0@bincrafters/stable",
    "boost_integer/1.69.0@bincrafters/stable",
    "boost_move/1.69.0@bincrafters/stable",
    "boost_optional/1.69.0@bincrafters/stable",
    "boost_predef/1.69.0@bincrafters/stable",
    "boost_preprocessor/1.69.0@bincrafters/stable",
    "boost_smart_ptr/1.69.0@bincrafters/stable",
    "boost_static_assert/1.69.0@bincrafters/stable",
    "boost_throw_exception/1.69.0@bincrafters/stable",
    "boost_type_traits/1.69.0@bincrafters/stable",
    "boost_utility/1.69.0@bincrafters/stable",
    "icu/63.1@bincrafters/stable",
    "sqlite3/3.27.2@bincrafters/stable",
    "sqlitecpp/2.4.0@bincrafters/stable",
    "yaml-cpp/0.6.3@_/_",
    "openssl/1.1.1g@_/_",
    "boost/1.71.0@conan/stable",
    "bzip2/1.0.8@conan/stable",
    "eigen/3.3.7@conan/stable",
    "lapack/3.7.1@conan/stable",
    "zlib/1.2.11@conan/stable",
    "gtest/1.10.0@_/_",
    "cmake/3.17.3@_/_"
]

if __name__ == "__main__":
    target_remote = sys.argv[1]
    conan_api, _, _ = Conan.factory()
    # for pkg in rehost_packages:
    for pkg in rehost_packages:
        # Which remote should we be getting this from?
        remote = None
        if "bincrafters" in pkg:
            remote = "bincrafters"
        else:
            remote = "conan-center"

        install_args = ["install", "-r", remote,
                        "--build=missing", pkg]

        print("conan {}".format(" ".join(install_args)))
        cmd = Command(conan_api)
        error = cmd.run(install_args)
        if error != 0:
            raise RuntimeError("Result is not zero, but {}".format(error))

        upload_args = ["upload", "-r", target_remote,
                       "--all", "-c", pkg]
        print("conan {}".format(" ".join(upload_args)))
        cmd = Command(conan_api)
        error = cmd.run(upload_args)
        if error != 0:
            raise RuntimeError("Result is not zero, but {}".format(error))
