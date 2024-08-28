class Company:
    NAME = None
    LIST_URL = None
    DESC_URL = None
    CATEGORY = None

    def __init__(self, conn, logger=None):
        self.conn = conn
        self.logger = logger

    def pull(self, include_all=False):
        pass

    def load_seen(self):
        seen = set()
        cursor = self.conn.cursor()
        cursor.execute("SELECT id from jobs WHERE company = '%s'" % self.NAME)
        for row in cursor.fetchall():
            seen.add(row[0])
        return seen

    def mark_seen(self, job_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO jobs (company, id) VALUES ('%s', '%s')" % (self.NAME, job_id)
        )
