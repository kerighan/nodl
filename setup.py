import setuptools


setuptools.setup(
    name="nodl",
    version="0.0.0",
    url="https://github.com/kerighan/nodl",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["networkx", "numpy"]
)
