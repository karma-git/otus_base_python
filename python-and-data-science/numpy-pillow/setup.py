from setuptools import setup

setup(
    name="image-editor",
    python_requires='>=3.10',
    version="1.0",
    py_modules=["img"],
    include_package_data=True,
    install_requires=["click", "Pillow", "loguru", "numpy"],
    entry_points="""
        [console_scripts]
        img=imager:cli
    """,
)
