# Venmobot
Pay and charge your coworkers within Slack using Venmo.

## Setup
### PostgreSQL
Venmobot requires a PostgreSQL database set up with a 'users' table.  This should
probably be automated in a script but for now just run this!

```sql
-- Create 'users' table.
CREATE TABLE users (
    slack_id text PRIMARY KEY,
    user_name text,
    access_toekn text,
    refresh_token text,
    access_expires timestamp
);
```
