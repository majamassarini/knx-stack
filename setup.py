from setuptools import setup, find_packages

setup(name="knx-stack",
      version="0.9",
      description="A python3 KNX stack for USB HID and KNXnet IP",
      url="https://github.com/majamassarini/knx-stack",
      long_description="A python3 KNX stack for USB HID and KNXnet IP, "
                       "which can be used both in a synchronous and asynchronous client.",
      author="Maja Massarini",
      author_email="maja.massarini@gmail.com",
      license="MIT",
      classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3.8",
            "Topic :: Communications",
            "Intended Audience :: Developers",
      ],
      packages=find_packages(exclude=[]),
      include_package_data=True,
      )


