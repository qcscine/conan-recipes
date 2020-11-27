__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

import os

from conans import ConanFile, CMake, tools


class CerealConan(ConanFile):
    name = "cereal"
    version = "1.3.0"
    description = "Serialization header-only library for C++11."
    license = "BSD-3-Clause"
    topics = ("conan", "cereal", "header-only", "serialization", "cpp11")
    homepage = "https://github.com/USCiLab/cereal"
    url = "https://github.com/conan-io/conan-center-index"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"thread_safe": [True, False]}
    default_options = {"thread_safe": False}
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        url = "https://github.com/USCiLab/cereal/archive/v{}.tar.gz"
        tools.get(url.format(self.version))
        os.rename(self.name + "-" + self.version, self._source_subfolder)

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = CMake(self)
        cmake.definitions["JUST_INSTALL_CEREAL"] = True
        cmake.configure()
        cmake.install()

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        if self.options.thread_safe:
            self.cpp_info.defines = ["CEREAL_THREAD_SAFE=1"]
            if self.settings.os == "Linux":
                self.cpp_info.system_libs.append("pthread")
