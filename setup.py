import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bavli_pages",
    version="0.1.2",
    author="Lior Israeli",
    author_email="israelilior@gmail.com",
    description="List of pages per Masechet at each chapter at the Jewish Talmud/Gemara/Shas Bavli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lisrael1/bavli_pages",
    project_urls={
        "Bug Tracker": "https://github.com/lisrael1/bavli_pages/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas', 'gematriapy'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=['*_tests', '*_examples'], ),
    python_requires=">=3.6",
)
