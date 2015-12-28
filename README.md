# Venmobot
Pay and charge your coworkers within Slack using Venmo.

## Slack Commands
These are the commands that Venmobot recognizes within Slack.

### `/venmo help`
Displays help information about all of the commands available.

### `/venmo login`
Allows the user to authorize Venmobot to make payments or charges on their behalf by Venmo. After issuing this command, a message wiill be returned to the Slack chat that includes a link to the Venmo website where you will be able to log in and authorize Venmobot to perform.

Venmobot uses OAuth to authenticate with Venmo's API, meaning that your Venmo password is never stored directly. Instead an Access Token is given to Venmobot by Venmo, which is valid for 60 days (and can be refreshed without needing user input afterwards). If you would like to remove Venmobot's access, you can use the `/venmo logout` command, or go to your Account Security Settings page on Venmo [here](https://venmo.com/account/settings/security) and remove Venmobot's access in the "Apps linked" section.

### `/venmo logout`
Removes all information about the user, including username and Venmo access tokens, from Venmobot.

## Setup
### Environment Variables
Venmobot gets a lot of its configuration from environment variables imported at runtime.

| Setting | Required | Description | Example |
| ------- | -------- | ----------- | ------- |
| DATABASE_URL | Yes | URL for Postgres database. Used for storing User information. | postgres://dtillery:mypassword@localhost/venmobot |
| REDIS_URL | Yes | URL for Redis instance. Used as backend for Celery task manager. | redis://localhost:6379/0 |
| SLACK_CMD_TOKEN | Yes | Token provided by Slack for a custom Slash Command.  Used to authenticate requests. | rpPdzWtxu3BqDZM8bi4r8yfA |
| VENMO_CLIENT_ID | Yes | Client ID for Venmo app (see [here](https://developer.venmo.com/gettingstarted/createapp) for more information on creating Venmo apps)| 1234 |
| VENMO_CLIENT_SECRET | Yes | Client Secret key for Venmo app. | L7gsU3qRTKzZPekYYbvZa9eoQUr9nRpL |
| VENMO_SANDBOX | No | Controls whether Venmo request are made against the production or sandbox API (see [here](https://developer.venmo.com/resources/sandbox) for documentation) | true |

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
