# DISQUS data collection

To collect data on discussion boards hosted by [DISQUS](https://disqus.com/).

## Set Up
Setting up an application on [DISQUS API](https://disqus.com/api/docs/) platform is needed. The "Public
Key" associated with the application should be used as the "API key" in the HTTP requests.

## Usages
The python wrappers of DISQUS APIs require a configuration file containing necessary parameters to
send requests. Example configs are [here](config/). The result is in json format saved as pickle.

Wrappers to call DISQUS APIs:

- `disqus_list_threads`: returns all threads within a forum.
- `disqus_list_posts`: returns all posts within a forum.

Other helper files:

- `thread_info_tsv`: convert a pickle from `list_threads` to a TSV file.

## Examples
Sites that runs their comment sections with DISQUS can be pulled with this repository. Usually a site
corresponds to a forum on DISQUS, and each sub-discussion section in the site corresponds to a
thread.

This repo worked on the following sites:

- [Down Detector](https://downdetector.com/)
- [Is The Service Down](https://istheservicedown.com/)
