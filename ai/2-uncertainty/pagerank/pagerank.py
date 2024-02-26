import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_ranks = dict()
    page_links = corpus[page]
    # If corpus contains no links, return equal probability for every item in corpus
    if not page_links:
        return {key: 1 / len(corpus) for key in corpus}

    # Calculate page_ranks of links in corpus
    for link in page_links:
        page_ranks[link] = damping_factor / len(page_links)

    # Calculate 1 - d probability of randomly visiting a page
    remainder_d = round(1 - damping_factor, 2)
    for link in corpus:
        if link not in page_ranks:
            page_ranks[link] = 0
        page_ranks[link] = page_ranks[link] + (remainder_d / len(corpus))

    return page_ranks


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Return random page from corpus
    current_page = random.choice(list(corpus.keys()))
    # Keep track of times looped
    i = 0
    # Keep track of page_ranks
    page_ranks = {key: 0 for key in corpus}

    # use transition model to retrieve new page_ranks
    while i < n:
        new_page_ranks = transition_model(corpus, current_page, damping_factor)
        for key, value in new_page_ranks.items():
            page_ranks[key] = page_ranks[key] + value
        current_page = random.choices(list(new_page_ranks.keys()), weights=new_page_ranks.values(), k=1)[0]
        i += 1

    # Calculate probability
    for key, value in page_ranks.items():
        page_ranks[key] = value / n

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages_length = len(corpus)
    page_ranks = {key: 1 / pages_length for key in corpus}

    # page_rank per page
    base_rank = (1 - damping_factor) / pages_length

    # Keep iterating when at least one probability changes more than 0.001
    matches = 0
    while matches < pages_length:
        matches = 0
        for page in corpus.keys():
            # Get current rank, new_rank
            current_rank = page_ranks[page]
            new_rank = base_rank

            for _page, links in corpus.items():
                # If page has no links, assume it has one link to every page and add to new_rank
                if not links:
                    new_rank += damping_factor * page_ranks[_page] / pages_length
                    continue
                # If page links to itself or not linked to page in question, continue
                elif page == _page or page not in links:
                    continue
                # Add d * PR[i] / number_of_links[i] to new_rank
                new_rank += damping_factor * page_ranks[_page] / len(links)

            page_ranks[page] = new_rank
            # If new_rank differs less than 0.001 from current, add to matches
            if abs(current_rank - new_rank) < 0.001:
                matches += 1

    return page_ranks


if __name__ == "__main__":
    main()
