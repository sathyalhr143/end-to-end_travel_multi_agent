from setuptools import setup, find_packages

def get_requirements(filename: str) -> list[str]:
    """This function return the packages in the filename
    as a list of strings.
    """
    requirements =[]
    with open(filename, 'r') as f:
        requirements = f.read().splitlines()
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements 


li = get_requirements('requirements.txt')
print(li)

setup(
    name="end_to_end_travel_multi_agent",
    version="0.1.0",
    author="Sathyaraj Medipalli",
    author_email="sathyarajmedipalli6@gmail.com",
    description="An end-to-end multi-agent travel planning system using specialized agents and tools from beeai framework.",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    python_requires='>=3.8'
)