from setuptools import setup, find_packages

setup(
    name="bllose-helper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 依赖包列表
    ],
    author="Bllose",
    author_email="bllose2018@gmail.com",
    description="A short description",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bllose/bllose-helper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
