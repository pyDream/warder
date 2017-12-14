import pbr.version

WARDER_VENDOR = "pyDream"
WARDER_PRODUCT = "warder"

version_info = pbr.version.VersionInfo('warder')


def vendor_string():
    return WARDER_VENDOR


def product_string():
    return WARDER_PRODUCT


def version_string_with_package():
    return version_info.version_string()