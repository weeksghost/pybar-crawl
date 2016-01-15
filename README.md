pybar-crawl
----

A modest multi-threaded web crawler

Usage
----
pybar-crawl uses Fabric to execute the script and accepts two arguments:

- URL
- crawl depth

Execute
----

```fab get_urls:'<URL> <depth>'```

or

```fab get_urls:'https://www.reddit.com/ 1'```