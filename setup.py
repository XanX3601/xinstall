import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xinstall",
    version="0.0.1",
    author="Thomas Petiteau",
    author_email="thomas.petiteau@outlook.com",
    description="Install and config stuff I use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XanX3601/xconfigurator",
    packages=setuptools.find_packages(),
    package_data={
        "": ["*.txt", "*.pkg"],
    },
    entry_points={"console_scripts": ["xinstall=xinstall.main:main"]},
    install_requires=["click", "rich"],
)
