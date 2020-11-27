__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

from conans import ConanFile, CMake, tools
import shutil


class IrcConanfile(ConanFile):
    name = "irc"
    version = "6d5c7c37"
    description = "Internal Redundant Coordinates"
    topics = ("conan", "quantum-chemistry", "chemistry")
    url = "https://github.com/rmeli/irc"
    license = "MIT"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"

    settings = "os", "compiler", "arch", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "tests": [True, False]
    }
    default_options = {"shared": False, "fPIC": True, "tests": False}
    requires = [
        "eigen/[~=3.3.7]@conan/stable",
        "boost/[>1.58.0]@conan/stable"
    ]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        # NOTE: Update this when release hits
        # remote = "https://github.com/RMeli/irc/archive/{}.tar.gz"
        # tools.get(remote.format(self.version))
        # extracted_dir = self.name + "-" + self.version
        # os.rename(extracted_dir, "sources")
        # Use the master branch
        self.run("git clone https://github.com/rmeli/irc.git")
        self.run("cd irc && git checkout 6d5c7c372d02ecdbd50f8981669c46ddae0638ac")
        shutil.move("irc", "sources")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["WITH_EIGEN"] = True
        cmake.definitions["BUILD_TESTS"] = self.options.tests
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        cmake.test()

    def package(self):
        self.copy(pattern="sources/LICENSE",
                  dst="licenses", keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        # Remove test option from package id computation
        delattr(self.info.options, "tests")
        self.info.header_only()

    def package_info(self):
        pass
