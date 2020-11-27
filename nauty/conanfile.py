__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

import os
from conans import ConanFile, CMake, tools


class NautyConanfile(ConanFile):
    name = "nauty"
    version = "2.7r1"
    description = "Graph Canonical Labeling and Automorphism Group Computation"
    topics = ("conan", "math", "graph")
    url = "http://pallini.di.uniroma1.it"
    license = "Apache-2.0"
    exports_sources = [
        "CMakeLists.txt",
        "config.cmake.in"
    ]
    generators = "cmake"

    settings = "os", "compiler", "arch", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {"shared": False, "fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        remote = "http://pallini.di.uniroma1.it/nauty27r1.tar.gz"
        tools.get(remote)
        os.rename("nauty27r1", "sources")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="sources/COPYRIGHT",
                  dst="licenses", keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()
