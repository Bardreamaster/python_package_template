from importlib.metadata import version

import python_package_template


def test_package_is_installed():
    assert python_package_template.__doc__
    assert version("python-package-template")
