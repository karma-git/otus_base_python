from setuptools import setup

setup(
    name="numpy-pillow",
    version="1.0",
    py_modules=["np"],
    include_package_data=True,
    install_requires=["click", "Pillow", "loguru", "numpy"],
    entry_points="""
        [console_scripts]
        np=main:cli
    """,
)
