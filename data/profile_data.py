import faker
fake = faker.Faker()

PROFILE_GENERIC = {
    'browser_type': 'mimic',
    'folder_id': '',
    'core_version': 131,
    'name': f'{fake.name()}',
    'os_type': 'windows',
    'parameters': {
        'fingerprint': {},
        'flags': {
            'audio_masking': 'mask',
            'fonts_masking': 'mask',
            'geolocation_masking': 'mask',
            'geolocation_popup': 'prompt',
            'graphics_masking': 'mask',
            'graphics_noise': 'mask',
            'localization_masking': 'mask',
            'media_devices_masking': 'mask',
            'navigator_masking': 'mask',
            'ports_masking': 'mask',
            'proxy_masking': 'disabled',
            'quic_mode': 'natural',
            'screen_masking': 'mask',
            'timezone_masking': 'mask',
            'webrtc_masking': 'disabled',
            'startup_behavior': 'recover',
        },
        'storage': {'is_local': False, 'save_service_worker': False},
    },
    'times': 1,
}
