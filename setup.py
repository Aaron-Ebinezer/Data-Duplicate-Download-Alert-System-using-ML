from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="scda",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Smart Collaborative Download Assistant (SCDA) - A tool to manage downloads efficiently.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/scda",  # Replace with your project URL
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "watchdog==2.1.6",
        "scikit-learn==1.0.2",
        "Pillow==9.5.0",
        "imagehash==4.3.1",
        "scikit-image==0.19.3",  # Optional: For image similarity
        "requests==2.28.1",      # Optional: For cloud integration
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "scda=main:main",  # Allows running `scda` from the command line
        ],
    },
)