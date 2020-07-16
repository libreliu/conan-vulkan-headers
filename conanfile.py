from conans import ConanFile, CMake, tools


class VulkanHeadersConan(ConanFile):
    name = "vulkan-headers"
    version = "1.2.141.0"
    license = "Apache-2.0"
    author = "Libre Liu <libreliu@foxmail.com>"
    url = "https://github.com/libreliu/conan-vulkan-headers"
    description = "Conan recipe for Vulkan-headers"
    topics = ("vulkan", "graphics", "api")

    # It's a header-only library, but I'm keeping it for convenience
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source(self):
        # Only SDK builds are maintained for now
        tools.get("https://github.com/KhronosGroup/Vulkan-Headers/archive/sdk-{}.tar.gz".format(
            self.version
        ))

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="Vulkan-Headers-sdk-{}".format(self.version))
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = CMake(self)
        cmake.install(build_dir=self.build_folder)

    def package_info(self):
        # The vulkan registry python scripts
        # can be used by self.deps_user_info["vulkan-headers"].VULKAN_REGISTRY ...
        import os
        self.user_info.VULKAN_REGISTRY = os.path.join(self.package_folder, "share", "vulkan", "registry")

