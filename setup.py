import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gym-os2r-real",
    version="1.0.0",
    author="Dawson Horvath",
    author_email="horvath.dawson@gmail.com",
    description="gym-ignition environments for open sim2real \
    development platform real robot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenSim2Real/gym-os2r-real",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'numpy',
          'gym-os2r',
    ],
    python_requires='>=3.8',
)
