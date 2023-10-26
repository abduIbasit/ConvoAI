from setuptools import setup, find_packages

setup(
    name="ConvoAI",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'sentence-transformers',
        'spacy',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'convoai=convoai.convoai:start_cli',
        ],
    }
)
