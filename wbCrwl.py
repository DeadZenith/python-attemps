import requests
import argparse
import concurrent.futures
from urllib.request import urlparse, urljoin
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup


# boolean check of the validity of url
def validUrl(url):
    try:
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc) and bool(parsed_url.scheme)
    except HTTPError:
        return False
    except URLError:
        return False
    except ValueError:
        return False


# differentiation of internal and external links thinking like a tree
branch = set()
leaves = set()


# This gets the FLD of this url and with beautifulSoup correctly and effectively pulls out urls
def pullUrls(url):
    urls = set()
    trunkUrl = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    print(url)

    for href in soup.findAll("a"):
        link = href.attrs.get("href")

        if link == "" or link is None:
            continue
        # urlparse to narrow URL down to usable schemes
        # allows for not correctly formatted URL's to still be handled
        link = urljoin(url, link)
        parsedUrl = urlparse(link)

        link = parsedUrl.scheme + "://" + parsedUrl.netloc + parsedUrl.path

        if not validUrl(link):
            continue
        if link in branch:
            continue
        if trunkUrl not in link:
            # mail client links
            if link not in leaves and not link.startswith("mailto:") and not link.startswith("tel:"):
                print(link)
                leaves.add(link)
            continue
        print(f"\t{link}")
        urls.add(link)
        branch.add(link)
    return urls


# collect all links within that url
def collectUrl(url):
    for links in pullUrls(url):
        return collectUrl(links)


# Allows this to be speed up massively by this asynchronously executing
def multiThread(url):
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        executor.submit(collectUrl, url, 50)


def main():
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument("url", help="Enter the url: ")
    args = parser.parse_args()
    collectUrl(args.url)
    print("\nTotal webpages crawled: {}\n".format(len(leaves) + len(branch)))
    print("\nInternal links: {}\n".format(len(branch)))
    print("\nExternal links: {}\n".format(len(leaves)))


# apparently this allows for this to run as main
if __name__ == "__main__":
    main()
