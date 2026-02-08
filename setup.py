from setuptools import setup, find_packages

setup(
    name="korean-spacing-corrector",
    version="1.0.0",
    description="고정밀 한국어 띄어쓰기 교정 시스템 (금융/법률 문서 특화)",
    author="Lucy Assignment",
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "torch>=2.0.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "tqdm>=4.65.0",
        "loguru>=0.7.0",
        "pydantic>=2.0.0",
        "regex",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "notebook": [
            "jupyter>=1.0.0",
            "matplotlib>=3.7.0",
            "seaborn>=0.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "spacing-correct=core.cli:main",
        ],
    },
)
