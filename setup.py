from setuptools import setup, find_packages

setup(
    name = 'mcqgenerator',
    version = '0.0.1',
    author = 'Pratik Suchak',
    author_email = 'pratiksuchak16@gmail.com',
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages = find_packages()
)