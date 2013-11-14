from setuptools import setup, find_packages


setup(name='agent.http',
      version='0.2',
      description='Rackspace Monitoring agent.plugin HTTP check',
      author='Vic Watkins',
      author_email='vic.watkins@rackspace.com',
      url='https://github.com/vickleford/agent.http',
      install_requires=['requests', 'argparse', 'logging'],
      packages=find_packages(),
      entry_points = { 'console_scripts': [
        'agent.http = check:spawn'
      ] }
     )