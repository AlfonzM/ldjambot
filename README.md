# LDJAM Bot

A Twitter bot that selects and tweets a random Ludum Dare game every few minutes.

Follow LDJAM Bot at [@ldjambot](http://twitter.com/ldjambot).

## Changelog
#### Update 1.2.1 (04-26-2015)
  * Do not include game author's LD name anymore in the tweet if Twitter handle exists (to avoid redundancy [e.g. Lorem by Ipsum (@Ipsum)] and game title trimming due to > 140 characters)

#### Update 1.2 (04-23-2015)
  * Fetch game author's Twitter handle (if exists) and include it in the tweet
  * Use meta data from the LD website source to fetch game information 

#### Update 1.1 (04-22-2015)
  * Updated for Ludum Dare 32
  * Trim game title if tweet > 140 characters
  
#### Version 1.0 (04-15-2015)
  * Released for Mini LD #58