CREATE_QUERY = '''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
CREATE_INDEX_QUERY = 'CREATE INDEX IF NOT EXISTS idx_original_url ON urls(original_url)'
SELECT_STATUS_QUERY = 'SELECT original_url, short_code, created_at FROM urls ORDER BY created_at DESC LIMIT 100'
INSERT_URL_QUERY = 'INSERT INTO urls (original_url, short_code) VALUES (?, ?)'
SELECT_EXISTING_URL_QUERY = 'SELECT short_code FROM urls WHERE original_url = ?'
SELECT_REDIRECT_QUERY = 'SELECT original_url FROM urls WHERE short_code = ?'