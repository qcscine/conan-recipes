__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

import os
from conans import ConanFile, CMake, tools
import shutil



def microarch(conanfile):
    """ Determine microarch of compiler and os (CPU chipset family or ISA) """
    cmdlist = None
    regex = None

    # Note that it doesn't matter if gcc or clang have different names for what
    # we call microarchitecture here. Any package ID is a hash convolution of
    # os, compiler, and then the microarch string. Collisions are so unlikely
    # they're impossible.

    if conanfile.settings.compiler == "gcc":
        cmdlist = ["gcc", "-march=native", "-Q", "--help=target"]
        regex = r"-march=\s+(?P<arch>[A-z0-9]+)"

    if conanfile.settings.compiler in ["clang", "apple-clang"]:
        cmdlist = ["clang", "-march=native", "-xc", "-", "-###"]
        regex = r"\"-target-cpu\"\\s+\"(?P<arch>[A-z0-9]+)\""

    if cmdlist is None:
        return None

    result = sp.run(cmdlist, stdout=sp.PIPE,
                    stderr=sp.STDOUT, universal_newlines=True)
    result.check_returncode()
    matcher = re.compile(regex)

    for match in matcher.finditer(result.stdout):
        return match.group("arch")

    for match in matcher.finditer(result.stderr):
        return match.group("arch")

    return None


class SerenityConanfile(ConanFile):
    name = "serenity"
    version = "1.3.0"
    description = "Serenity: A subsystem quantum chemistry program."
    topics = ("conan", "quantum-chemistry", "chemistry")
    url = "https://github.com/qcserenity/serenity"
    license = "LGPL-3.0"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    exports = "serenity.patch"

    settings = "os", "compiler", "arch", "build_type"
    options = {
        "shared": [True, False],
        "tests": [True, False],
        "microarch": ["detect", "none"]
    }
    default_options = {"shared": False, "tests": False, "microarch": "none"}
    build_requires = "cmake/[>3.13.3]@scine/stable"
    requires = [
        "zlib/[~=1.2.11]",
        "hdf5/[=1.12.0]@scine/stable",
        "eigen/[~=3.3.7]@conan/stable",
        "boost/[>1.58.0]@conan/stable"
    ]

    def source(self):
        self.run("git clone https://github.com/qcserenity/serenity")
        self.run("cd serenity && git checkout 1.3.0")
        shutil.move("serenity", "sources")

        tools.patch(base_path="sources", patch_file="serenity.patch")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["SERENITY_ENABLE_TESTS"] = self.options.tests
        if self.options.microarch == "none":
            cmake.definitions["SERENITY_MARCH"] = ""
        else:
            cmake.definitions["SERENITY_MARCH"] = microarch(self) or ""
        cmake.definitions["HDF5_USE_STATIC_LIBRARIES"] = not self.options['hdf5'].shared
        cmake.definitions["HDF5_ROOT"] = self.deps_cpp_info["hdf5"].rootpath
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="sources/LICENSE",
                  dst="licenses", keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        # Remove test option from package id computation
        delattr(self.info.options, "tests")
        # Overwrite microarch value in info with detected or make it empty
        if "microarch" in self.options:
            if self.options.get_safe("microarch") == "detect":
                self.info.options.microarch = microarch(self) or ""
            else:
                self.info.options.microarch = ""


    def package_info(self):
        pass
