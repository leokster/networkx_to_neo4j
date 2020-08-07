import setuptools


setuptools.setup(
    name="networkx-to-neo4j", # Replace with your own username
    version="0.0.1",
    author="leokster",
    author_email="tim.rohner@smartmind.ch",
    description="Small tool for exporting networkx graphs to neo4j",
    long_description="Small tool for exporting networkx graphs to neo4j",
    long_description_content_type="text/markdown",
    url="https://github.com/leokster/networkx-to-neo4j",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires = ["neo4j","networkx","progressbar2"]
)