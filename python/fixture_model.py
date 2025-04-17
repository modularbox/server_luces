class FixtureModel():
    '''
    FixtureModel represents a DMX light fixture model.

    Generic fixtures:
    R: Red, G: Green, B: Blue, W: White
    D: Dimmer, S: Strobe
    E: Effect, P: Speed

    Example of fixtures:
    RGBD     - 4 channels: Red, Green, Blue, Dimmer
    DRGB     - 4 channels: Dimmer, Red, Green, Blue
    RGBW     - 4 channels: Red, Green, Blue, White
    DRGBW    - 5 channels: Dimmer, Red, Green, Blue, White

    Attributes:
        fixture (str): The name of the fixture model.
        channels_length (int): The number of channels in the fixture.
        channels (dict): The metadata for each channel in the fixture,
            mapping channel names to their indices.

    Usage:
        rgb = FixtureModel('RGB')
        print(rgb.channels_length)  # Output: 3
        print(rgb.channels)
    '''

    channel_map = {
        '1': 'switch_1',
        '2': 'switch_2',
        '3': 'switch_3',
        '4': 'switch_4',
        'R': 'red',
        'G': 'green',
        'B': 'blue',
        'W': 'white',
        'D': 'dimmer',
        'S': 'strobe',
        'E': 'effect',
        'P': 'speed'
    }


    def __init__(self, fixture):
        '''
        Initializes a FixtureModel instance with the specified fixture name.

        Args:
            fixture (str): The name of the fixture model.
        '''
        self.fixture = fixture
        self.channels_length = 0
        self.channels = {}
        try:
            self.parse_fixture_name()
        except ValueError as e:
            print(f"Warning: {e}")

        

    def parse_fixture_name(self):
        '''
        Parses the fixture name and sets the channels_length and channels attributes.
        '''
        channels = {
            'switch_1': None,
            'switch_2': None,
            'switch_3': None,
            'switch_4': None,
            'red': None,
            'green': None,
            'blue': None,
            'white': None,
            'dimmer': None,
            'strobe': None,
            'effect': None,
            'speed': None
        }

        channel_index = 1
        for char in self.fixture:
            print(f'Processing character: {char}')  # Agregamos esta línea para imprimir el carácter
            if char in FixtureModel.channel_map:
                channel_name = FixtureModel.channel_map[char]
                if channels[channel_name] is None:
                    channels[channel_name] = channel_index
                    channel_index += 1
                else:
                    raise ValueError(f'Duplicate character in fixture name: {char}')
            else:
                raise ValueError(f'Invalid character in fixture name: {char}')

        self.channels_length = channel_index - 1
        self.channels = channels

    def setup_fixture(self, fixture_instance):
        '''
        Sets up the provided Fixture instance based on the FixtureModel.

        Args:
            fixture_instance (Fixture): The Fixture instance to set up.
        '''

        # Filter non-null items and sort by channel_name
        filtered_channels = {channel_name: channel_index for channel_name, channel_index in self.channels.items() if channel_index is not None}
        sorted_channels = dict(sorted(filtered_channels.items(), key=lambda item: item[1]))

        # Loop through the sorted and filtered channels
        for channel_name, channel_index in sorted_channels.items():
            fixture_instance._register_channel(channel_name)
            aliases = [key for key, value in FixtureModel.channel_map.items() if value == channel_name]
            fixture_instance._register_channel_aliases(channel_name, *aliases)

    def __getattribute__(self, attr):
        '''
        Retrieves the value of the requested attribute.

        Args:
            attr (str): The name of the attribute to retrieve.

        Returns:
            The value of the requested attribute.

        Raises:
            AttributeError: If the requested attribute is not valid.
        '''
        if attr == 'channels_length':
            return object.__getattribute__(self, 'channels_length')
        elif attr == 'channels':
            return object.__getattribute__(self, 'channels')
        else:
            return object.__getattribute__(self, attr)