from setuptools import setup, find_packages

setup(name="knx-stack",
      version="0.9",
      description="Parse and send knx messages",
      url="https://bitbucket.org/culsucar/knxstack",
      long_description="",
      author="Maja Massarini",
      author_email="maja.massarini@gmail.com",
      license="All rights reserved",
      packages=find_packages(exclude=[]),
      include_package_data=True,
      )


