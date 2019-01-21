from setuptools import setup, find_packages
from pip._internal.download import PipSession
from pip._internal.req import parse_requirements


def get_requirements(file_name):
    return [
        str(requirement.req) for requirement in parse_requirements(
            file_name, session=PipSession()
        )
    ]


if __name__ == '__main__':
    setup(
            name='skyeng-cli',
        version='0.0.1',
        description='A sample Python project',
        install_requires=get_requirements('requirements.txt'),
        include_package_data=True,
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'skyeng-cli=skyeng_cli.main:entry_point',
            ],
        },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
    )
