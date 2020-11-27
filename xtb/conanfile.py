__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

import os
from conans import ConanFile, CMake, tools


class XtbConanfile(ConanFile):
    name = "xtb"
    version = "6.3.2"
    description = "Semiempirical Extended Tight-Binding Program Package"
    topics = ("conan", "quantum-chemistry", "chemistry")
    url = "https://github.com/grimme-lab/xtb"
    homepage = "https://www.chemie.uni-bonn.de/pctc/mulliken-center/software/xtb/xtb"
    license = "LGPL-3.0-only"
    exports = "portable-linalg.patch"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"

    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    requires = [
        "cmake/[>=3.18.0]@scine/stable",
        "lapack/3.7.1@conan/stable"
    ]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        remote = "https://github.com/grimme-lab/xtb/archive/v{}.tar.gz"
        tools.get(remote.format(self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")
        tools.patch(base_path="sources", patch_file="portable-linalg.patch")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="sources/COPYING*", dst="licenses", keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        pass
