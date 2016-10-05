#!/usr/bin/env python
# -*- coding: utf-8 -*-


import setuptools


REQUIREMENTS = (
    "bcrypt",
    "cephlcm-common==0.1.0a0",
    "Flask",
    "jsonschema"
)


setuptools.setup(
    name="cephlcm-api",
    description="Ceph Lifecycle Management API service",
    long_description="",  # TODO
    version="0.1.0a0",
    author="Sergey Arkhipov",
    author_email="sarkhipov@mirantis.com",
    maintainer="Sergey Arkhipov",
    maintainer_email="sarkhipov@mirantis.com",
    license="Apache2",
    url="https://github.com/Mirantis/ceph-lcm",
    packages=setuptools.find_packages(),
    python_requires=">=3.4",
    install_requires=REQUIREMENTS,
    zip_safe=True,
    entry_points={
        "console_scripts": [
            "cephlcm-api-ensure-indexes = cephlcm_api:index_db"
        ]
    },
    classifiers=(
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    )
)