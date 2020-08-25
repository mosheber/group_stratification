import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scale_fpn", # Replace with your own username
    version="0.0.1",
    author="mosheber",
    author_email="screedo1997@gmail.com",
    description="a scalable fpn architecture using pytorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mosheber/scalable_feature_pyramid_network.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)