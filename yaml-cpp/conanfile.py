__copyright__ = """This code is licensed under the 3-clause BSD license.
Copyright ETH Zurich, Laboratory of Physical Chemistry, Reiher Group.
See LICENSE.txt for details.
"""

from conans import ConanFile, CMake, tools
import os


class YamlCppConan(ConanFile):
    name = "yaml-cpp"
    version = "0.6.3"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/jbeder/yaml-cpp"
    topics = ("conan", "yaml", "yaml-parser",
              "serialization", "data-serialization")
    description = "A YAML parser and emitter in C++"
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _cmake = None

    def source(self):
        tools.get(
            url="https://github.com/jbeder/yaml-cpp/archive/yaml-cpp-0.6.3.tar.gz",
            sha256="77ea1b90b3718aa0c324207cb29418f5bced2354c2e483a9523d98c3460af1ed"
        )
        extracted_dir = self.name + "-" + self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        tools.check_min_cppstd(self, "11")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self._cmake = CMake(self)
        self._cmake.definitions["YAML_CPP_BUILD_TESTS"] = False
        self._cmake.definitions["YAML_CPP_BUILD_CONTRIB"] = True
        self._cmake.definitions["YAML_CPP_BUILD_TOOLS"] = False
        self._cmake.definitions["YAML_BUILD_SHARED_LIBS"] = self.options.shared
        if self.settings.compiler == "Visual Studio":
            self._cmake.definitions["MSVC_SHARED_RT"] = "MD" in self.settings.compiler.runtime
        self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses",
                  src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append('m')
        if self.settings.compiler == 'Visual Studio':
            self.cpp_info.defines.append('_NOEXCEPT=noexcept')
