__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

import os
from conans import ConanFile, CMake, tools


class RDLConanfile(ConanFile):
    name = "RingDecomposerLib"
    version = "1.1.3"
    description = "Unique Ring Families Algorithm"
    topics = ("conan", "cheminformatics", "chemistry")
    url = "https://github.com/rareylab/RingDecomposerLib"
    license = "BSD-3-Clause"
    exports_sources = [
        "CMakeLists.txt",
        "config.patch"
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
        full_version = "1.1.3_rdkit"
        remote = "https://github.com/rareylab/RingDecomposerLib/archive/v{}.tar.gz"
        tools.get(remote.format(full_version))
        os.rename("{}-{}".format(self.name, full_version), "sources")
        tools.patch(base_path="sources", patch_file="config.patch")

    def _configure_cmake(self):
        cmake = CMake(self)
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
