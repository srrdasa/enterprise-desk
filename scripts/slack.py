#!/usr/bin/env python3
"""Slack Web API helper. Reads bot tokens from the environment ONLY.
CRITICAL LEARNING: conversations.list/history/replies MUST be form-encoded —
a JSON body silently ignores params like `types`. This helper is always form-encoded.
CRITICAL LEARNING: oldest/latest timestamps MUST have at most 6 fractional digits —
str(time.time()) sometimes emits 7, and Slack then silently returns ZERO messages
(ok=true, empty list). Always pass ts6(t), never str(t).

Identity comes from the environment so this file is deployment-agnostic:
  DESK_NAME  — the bot's display username (default "The Desk")
  DESK_ICON  — icon emoji (default :file_cabinet:)
A second workspace is optional via SLACK_BOT_TOKEN_2."""
import os, json, time, urllib.request, urllib.parse, urllib.error

WORKSPACE_ENV = {'primary': 'SLACK_BOT_TOKEN', 'secondary': 'SLACK_BOT_TOKEN_2'}

def ts6(t):
    """Slack ts param: max 6 fractional digits or results silently come back empty."""
    return f"{float(t):.6f}"

def sl(method, workspace='primary', **params):
    tok = os.environ[WORKSPACE_ENV[workspace]]
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request('https://slack.com/api/' + method, data=data,
        headers={'Authorization': f'Bearer {tok}',
                 'Content-Type': 'application/x-www-form-urlencoded'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503):
                time.sleep(2 ** attempt); continue
            raise
    return {}

def post_as_desk(channel, text, workspace='primary', thread_ts=None):
    """Post as the desk. ONLY for approved replies or Principal-directed notifications —
    never an unapproved reply to a human (binding rule 1).
    THREADING RULE: a REPLY to an existing message MUST pass thread_ts (the parent's ts)
    so it lands in-thread. A brand-new post omits thread_ts."""
    kwargs = dict(channel=channel, text=text,
                  username=os.environ.get('DESK_NAME', 'The Desk'),
                  icon_emoji=os.environ.get('DESK_ICON', ':file_cabinet:'),
                  unfurl_links='false')
    if thread_ts:
        kwargs['thread_ts'] = thread_ts
    return sl('chat.postMessage', workspace=workspace, **kwargs)
