import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="epibox", 
    version="0.0.1",
    author="Ana Sofia Carmo",
    author_email="anascacais@gmail.com",
    description="EpiBOX: A novel approch to long-term monitoring in Epilepsy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anascacais/EpiBOX",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)