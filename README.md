# Reaction Watchdog v1.0
A suuuper simple/lazy discord bot for watching and listing reaction events on messages sent on a server.

## Installation
Requires discord.py!
Install with `pip install discord`.
Don't forget to set your bot token with variable `TOKEN`!

## Commands
* `~post (channel name) (message)`
  * Posts a message to a channel and watches its reactions.
* `~watch (message id)`
  * Watches message thats been posted (not needed for messages posted by the post command).
* `~stop (message id)`
  * Stops watching a message thats been posted and deletes the logs. it is highly recommended to do this after you are done watching a message.
* `~log (message id) ((optional)modifiers)`
  * Outputs a log of reactions on a message thats being watched. 
  * modifiers:
    * force-mention or fm: overrides mention settings on the log
    * include-removed or ir: includes removed reactions in the log
