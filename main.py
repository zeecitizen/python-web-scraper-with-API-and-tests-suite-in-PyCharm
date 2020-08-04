import argparse
from bs4 import BeautifulSoup
import itertools


class ServiceFunnel:
    def __init__(self):
        self.complete_match = {}  # managing the complete matched tags dict
        self.partial_match = {}  # managing the partial matched tags dict

    def scrape_html(self, html: str):
        """
                Scrape HTML, extract tags and snippet and store them in an appropriate data structure.

                Args:
                    html (str) : Entire HTML content. Not the path to HTML document.
        """

        soup = BeautifulSoup(html, features="lxml")
        # Seprating tags using bs4
        data_tags_tags = soup.find_all(lambda tag: True if 'data-tags' in tag.attrs else False)
        self.complete_match = {tuple(sorted([v.strip() for v in tag.attrs['data-tags'].
                                            split(',')])): [tag, []] for tag in data_tags_tags}

        # Creating dict with all the complete tags
        for k, v in self.complete_match.items():
            hold_tags = set()
            for k2 in self.complete_match.keys():
                if k == k2:
                    continue
                if set(k).issubset(k2):
                    hold_tags.update(set(k2).difference(k))
            v[1] = sorted([{"name": tag} for tag in hold_tags], key=lambda tag: tag['name'])

        # Creating dict with all the partial and ambigious tags
        for k, v in self.complete_match.items():
            for L in range(0, len(k) + 1):
                for subset in itertools.permutations(k, L):
                    if subset:
                        if not self.partial_match.get(subset):
                            self.partial_match[subset] = []
                        self.partial_match[subset].append(v[0])

        # Inserting tags in the partial match dic for reference
        hold_partial_match = self.partial_match.copy()
        for k, v in self.partial_match.items():
            if len(v) > 1:
                values = set()
                for tags in v:
                    values.update(tags.attrs['data-tags'].split(','))
                v2 = v.copy()
                v2.append(sorted([{"name": tag} for tag in set(values).difference(k)], key=lambda tag: tag['name']))
                hold_partial_match[k] = v2

        self.partial_match = hold_partial_match.copy()

    def handle_request(self, request: dict) -> dict:
        """
                Find out the correct snippet that maps to a set of input tags.

                Args:
                    request (dict): Request object as specified in the readme.
                Returns:
                    response (dict): Response object as specified in the readme.
        """
        """Creating a sorted tuple of tags to be searched"""
        search_tags = tuple(sorted([tag['name'] for tag in request['selected_tags']]))

        # This is checking if the search tags matches exactly
        complete_match = self.complete_match.get(search_tags)
        if complete_match:
            return {
                "snippet": str(complete_match[0]),
                "next_tags": complete_match[1],
                "status": {"code": 0, "msg": "Valid tags with snippet"},
                "selected_tags": request['selected_tags']
            }

        partial_match = self.partial_match.get(search_tags)
        # This is checking if the search tags matches partially
        if partial_match:
            if isinstance(partial_match[-1], list):
                next_tags = partial_match[-1]
                partial_match.pop(-1)

            if partial_match and len(partial_match) == 1:
                return {
                    "snippet": str(partial_match[0]),
                    "next_tags": [],
                    "status": {"code": 0, "msg": "Valid tags with snippet"},
                    "selected_tags": request['selected_tags']
                }
            elif partial_match and len(partial_match) > 1:
                return {
                    "snippet": None,
                    "next_tags": next_tags,
                    "status": {"code": 1, "msg": "Valid tags but no snippet"},
                    "selected_tags": request['selected_tags']
                }
        # None of the tag is matching
        return {
            "snippet": None,
            "next_tags": [],
            "status": {"code": 2, "msg": "Invalid tags"},
            "selected_tags": request['selected_tags']
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--html_path",
        help="path leading to the html file",
        type=str,
        required=True,
    )

    args = parser.parse_args()
    with open(args.html_path, "r") as f:
        html_str = f.read()
    service_funnel = ServiceFunnel()
    service_funnel.scrape_html(html_str)
    service_funnel.handle_request({"selected_tags": [{"name": "C"}, {"name": "A"}]})
