# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

import feedparser
import BeautifulSoup
import requests

# <codecell>

from collections import namedtuple as nt

# <codecell>

PodcastItem = nt("PodcastItem", 'title url number')

# <codecell>

def set_segment_filename(episode, seg_number):
    segment_filename = "2013-07-12-episode" + episode + "-segment" + `seg_number` + ".mkd"
    return segment_filename

# <codecell>

def write_segment_file(segment_filename, yaml):
    f = open(segment_filename, "w")
    for line in yaml:
        f.write(line + "\n")
    f.write("\n\n ye olde llorum ipsum goeth here \n")
    f.close()

# <codecell>

def get_section_title(item):
    section_title = item.title.contents[0]
    return section_title

# <codecell>

def get_section_link(item):
    section_link = item.enclosure["url"]
    return section_link

# <codecell>

def get_items_from_feed_url(url):
    r = requests.get(url)
    pod_soup = BeautifulSoup.BeautifulSoup(r.content)
    items = pod_soup.findAll("item")
    return items

# <codecell>

def replace_line_in_yaml(yaml, old_line, new_line):
    new_yaml = []
    for line in yaml:
        if line == old_line:
            new_yaml.append(new_line)
        else:
            new_yaml.append(line)
    return new_yaml

# <codecell>

def set_url(yaml, url):
    old_line = "segment-audio:"
    new_line = "segment-audio: " + url
    new_yaml = replace_line_in_yaml(yaml, old_line, new_line)
    return new_yaml

# <codecell>

def set_title(yaml, title):
    old_line = "title:"
    new_line = "title: " + title
    new_yaml = replace_line_in_yaml(yaml, old_line, new_line)
    return new_yaml

# <codecell>

def set_segment_value(yaml, seg_number):
    old_line = "segment: N"
    new_line = "segment: " + `seg_number`
    new_yaml = replace_line_in_yaml(yaml, old_line, new_line)
    return new_yaml

# <codecell>

def set_episode_value(yaml, episode):
    old_line = "episode: M"
    new_line = "episode: " + episode
    new_yaml = replace_line_in_yaml(yaml, old_line, new_line)
    return new_yaml

# <codecell>

def set_episode_category(yaml, episode):
    old_line = " - episodeX"
    new_line = " - episode" + episode
    new_yaml = replace_line_in_yaml(yaml, old_line, new_line)
    return new_yaml

# <codecell>

def build_yaml_from_section(episode, section):
    yaml = ["---",
            "layout: segment",
            "title:",
            "categories:",
            " - segment",
            " - episodeX",
            "features:",
            " - ['FEATURE TITLE', 'FEATURE LINK']",
            "articles:",
            " - ['ARTICLE TITLE', 'ARTICLE LINK']",
            "insights:",
            " - ['INSIGHT TITLE', 'INSIGHT LINK']",
            "editorials:",
            " - ['EDITORIAL TITLE', 'EDITORIAL LINK']",
            "episode: M",
            "segment: N",
            "segment-audio:",
            "---"]
    yaml = set_url(yaml, section.url)
    yaml = set_title(yaml, section.title)
    yaml = set_episode_category(yaml, episode)
    yaml = set_episode_value(yaml, episode)
    yaml = set_segment_value(yaml, section.number)
    #for line in yaml: print line
    #print ""
    return yaml

# <codecell>

# simple feed
sf = feedparser.parse('http://www.thenakedscientists.com/naked_scientists_podcast.xml')

# enhanced feed
ef = feedparser.parse('http://www.thenakedscientists.com/naked_scientists_enhanced_podcast.xml')

# chapter feed
# cf_xml = feedparser.parse('http://www.thenakedscientists.com/HTML/chaptertool/?tx_nakscichapters_pi1[rss_individual]=1&tx_nakscichapters_pi1[podcastID]=1000408')
url = 'http://www.thenakedscientists.com/HTML/chaptertool/?tx_nakscichapters_pi1[rss_individual]=1&tx_nakscichapters_pi1[podcastID]=1000408'
r = requests.get(url)

# <codecell>

#r.content
pod_soup = BeautifulSoup.BeautifulSoup(r.content)

# <codecell>

items = pod_soup.findAll("item")

# <codecell>

sections = []
section_count = 0
for item in items:
    section_count = section_count + 1 
    title = get_section_title(item)
    link = get_section_link(item)
    section = PodcastItem(title, link, section_count)
    sections.append(section)

# <codecell>

for section in sections:
    episode = "1"
    output_yaml = build_yaml_from_section(episode, section)
    segment_filename = set_segment_filename(episode, section.number)
    print segment_filename
    print output_yaml
    #write_segment_file(segment_filename, output_yaml)
    

# <codecell>

output_yaml

# <codecell>


