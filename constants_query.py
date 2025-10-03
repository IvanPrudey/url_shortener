CREATE_QUERY = '''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''

CREATE_INDEX_QUERY = 'CREATE INDEX IF NOT EXISTS idx_original_url ON urls(original_url)'