import unittest
from main import ServiceFunnel


class TestServiceFunnelScrape(unittest.TestCase):
    def setUp(self):
        self.service_funnel = ServiceFunnel()
        html_string = """
            <article class="article " id="id-39334" data-tags="A,X,Z"><h2>S1</h2></article>
            <article class="article " id="id-39334" data-tags="A,B,C"><h2>S2</h2></article>
            <article class="article " id="id-39334" data-tags="A,B,D"><h2>S3</h2></article>
            <article class="article " id="id-39334" data-tags="A,D,E"><h2>S4</h2></article>
        """
        self.service_funnel.scrape_html(html_string)

    def test_common_tags(self):
        result = self.service_funnel.handle_request(
            {"selected_tags": [{"name": "A"}, {"name": "B"}, {"name": "C"}, {"name": "D"}, {"name": "E"}]}
        )
        self.assertEqual(result["status"]["code"], 2)
        self.assertEqual(result["status"]["msg"], "Invalid tags")
        self.assertEqual(
            result["selected_tags"],
            [{"name": "A"}, {"name": "B"}, {"name": "C"}, {"name": "D"}, {"name": "E"}],
        )
        self.assertCountEqual(result["next_tags"], [])
        self.assertEqual(
            result["snippet"], None)

    def test_two_tag_match(self):
        result = self.service_funnel.handle_request(
            {"selected_tags": [{"name": "B"}, {"name": "D"}]}
        )
        self.assertEqual(result["status"]["code"], 0)
        self.assertEqual(result["status"]["msg"], "Valid tags with snippet")
        self.assertEqual(
            result["selected_tags"], [{'name': 'B'}, {'name': 'D'}]
        )
        self.assertCountEqual(result["next_tags"], [])
        self.assertEqual(
            result["snippet"],
            '<article class="article" data-tags="A,B,D" id="id-39334"><h2>S3</h2></article>')

    def test_two_tag_match_2(self):
        result = self.service_funnel.handle_request(
            {"selected_tags": [{"name": "A"}, {"name": "B"}]}
        )
        self.assertEqual(result["status"]["code"], 1)
        self.assertEqual(result["status"]["msg"], "Valid tags but no snippet")
        self.assertEqual(
            result["selected_tags"], [{'name': 'A'}, {'name': 'B'}]
        )
        self.assertCountEqual(result["next_tags"], [{'name': 'C'}, {'name': 'D'}, ])
        self.assertEqual(
            result["snippet"], None)


if __name__ == "__main__":
    unittest.main()
