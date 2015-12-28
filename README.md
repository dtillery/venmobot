# Venmobot
Pay and charge your coworkers within Slack using Venmo.

## Setup
### Environment Variables
Venmobot gets a lot of its configuration from environment variables imported at runtime.

| Setting | Required | Description | Example |
| ------- | -------- | ----------- | ------- |
| SLACK_CMD_TOKEN | Yes | Token provided by Slack for a custom Slash Command.  Used to authenticate requests. | rpPdzWtxu3BqDZM8bi4r8yfA |

### PostgreSQL
Venmobot requires a PostgreSQL database set up with a 'users' table.  This should
probably be automated in a script but for now just run this!

```sql
-- Create 'users' table.
CREATE TABLE users (
    slack_id text PRIMARY KEY,
    user_name text,
    access_token text,
    refresh_token text,
    access_expires timestamp
);
```
