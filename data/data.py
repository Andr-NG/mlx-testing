# flake8: noqa

import faker


RESTRICTIONS = {
    'workspace_id': '',
    'restrictions': {
        'plan_name': 'Team Monthly',
        'cloud_profiles_count': 1000,
        'allowed_browser_types': [
            'mimic',
            'stealthfox',
            'android'
        ],
        'folders_count': 100000,
        'local_profiles_count': 1000,
        'team_members_count': 100,
        'active_profiles_count': 0,
        'automation_available': True,
        'ratelimit': [
            {
                'limit_size': 50,
                'operation': 'all',
                'window_size': '1m'
            }
        ]
    }
}
