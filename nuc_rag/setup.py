from setuptools import setup, find_packages
import os

# Read the requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    return []

# Read the README if it exists
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Nuclear Safety RAG Application for Technical Data Retrieval and Analysis"

setup(
    name="nuc_rag",
    version="1.0.0",
    author="Nuclear Safety RAG Team",
    author_email="",
    description="Nuclear Safety RAG Application for Technical Data Retrieval and Analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dcalderin/rag_nuclear_safety",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "nuc-rag=nuc_rag.main:main",
        ],
    },
    package_data={
        "nuc_rag": ["*.pdf", "*.hdf5", "*.csv"],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="nuclear safety, RAG, retrieval-augmented generation, gradio, AI, NLP",
)
