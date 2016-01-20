VIDEO_MAPPING = {
    'mappings': {
        'video_document': {
            'properties': {
                'title': {
                    'type': 'string'
                },
                'video_id': {
                    'type': 'string'
                },
                'video_type': {
                    'type': 'string'
                },
                'thumbnail_url': {
                    'type': 'string'
                },
                'date_added': {
                    'type': 'date'
                },
                'id': {
                    'type': 'long'
                }
            }
        }
    }
}
