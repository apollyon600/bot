GUILD_CONFIG = {
    '_id': None,
    'name': None,
    'icon': None,
    'banner': None,
    'visible': True,
    'reports_enabled': True,
    'global_blacklisted': False,
    'global_blacklisted_commands': [],
    'restricted_commands': [],
    'events': {
        'default_enabled': True,
        'default_mention_id': None,
        'default_webhook_data': None,
        'magmaBoss': {
            'enabled': False,
            'mention_id': None,
            'webhook_data': None
        },
        'darkAuction': {
            'enabled': False,
            'mention_id': None,
            'webhook_data': None
        },
        'bankInterest': {
            'enabled': False,
            'mention_id': None,
            'webhook_data': None
        },
        'newYear': {
            'enabled': False,
            'mention_id': None,
            'webhook_data': None
        },
        'zoo': {
            'enabled': False,
            'mention_id': None,
            'webhook_data': None
        },
        'spookyFestival': {
            'enabled': False,
            'mention_id': None,
            'webhook_data': None
        },
        'winterEvent': {
            'enabled': False,
            'mention_id': None,
            'channel_id': None,
            'webhook_data': None
        },
        'jerryWorkshopEvent': {
            'enabled': False,
            'mention_id': None,
            'webhook_data': None
        }
    },
    'last_updated': None
}

PLAYER_DATA = {
    'mojang_uuids': [],
    'discord_ids': [],
    'global_blacklisted': False,
    'guild_report_blacklisted': [],
    'guild_reputation_blacklisted': [],
}

REPUTATION = {
    'guild_id': None,
    'reporter_discord_id': None,
    'submitter_discord_id': None,
    'reason': None,
    'positive': None,
    'type': None,
    'staff_sorted_discord_id': None,
    'submitted_timestamp': None
}
