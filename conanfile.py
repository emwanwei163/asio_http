from conans import ConanFile, CMake, tools


class AsioHttpConan(ConanFile):
    name = "asio_http"
    version = "0.0.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of AsioHttp here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    build_policy = 'missing'
    short_paths = True

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    requires = (
        'websocketpp/0.8.1-5@k3p/stable'
    )

    def build(self):
        cmake = CMake(self)
        cmake.configure()

        # cmake.definitions['BUILD_EXAMPLE'] = "1"
        cmake.build()


    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*http.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["asio_http"]

