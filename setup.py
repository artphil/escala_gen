setup(
    name="escala_gen",
    version="2.0.0",
    description="Gerador de escalas PEB/PEQ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/artphil/escala_gen",
    author="Arthur Phillip Silva",
    author_email="artphil.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["escala_gen"],
    include_package_data=True,
    install_requires=[
       "et-xmlfile","jdcal","numpy","openpyxl","Pillow","pywin32",    
	   ],
    entry_points={"console_scripts": ["realpython=escala_gen.__main__:main"]},
)
