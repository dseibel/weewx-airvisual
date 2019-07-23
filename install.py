# Installer for air visual air quality extension
# Dan Seibel, 2019

from setup import ExtensionInstaller

def loader():
    return AQInstaller()

class AQInstaller(ExtensionInstaller):
    def __init__(self):
        super(AQInstaller, self).__init__(
            version="0.2",
            name='weewx-airvisual',
            description='Collect airvisual data',
            author="Dan Seibel",
            author_email="dan.seibel@dantine.ca",
            data_services='user.weewx-airvisual.AQService',
            config={
                'AQService': {
                    'api_key': 'add key here'
                    },
            },
            files=[('bin/user', ['bin/user/weewx-airvisual.py']), ]
            )
