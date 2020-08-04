import unittest
from main import ServiceFunnel


class TestServiceFunnelScrape(unittest.TestCase):
    def setUp(self):
        self.service_funnel = ServiceFunnel()
        html_string = """
            <article class="article " id="id-39334" data-tags="A"><h2>S1</h2></article>
            <article class="article " id="id-39334" data-tags="A,B,C"><h2>S2</h2></article>
            <article class="article " id="id-39334" data-tags="A,B,D"><h2>S3</h2></article>
            <article class="article " id="id-39334" data-tags="A,D,E"><h2>S4</h2></article>
        """
        self.service_funnel.scrape_html(html_string)

    def test_valid_tags_with_snippet(self):
        result = self.service_funnel.handle_request(
            {"selected_tags": [{"name": "A"}, {"name": "B"}, {"name": "C"}]}
        )
        self.assertEqual(result["status"]["code"], 0)
        self.assertEqual(result["status"]["msg"], "Valid tags with snippet")
        self.assertEqual(
            result["selected_tags"],
            [{"name": "A"}, {"name": "B"}, {"name": "C"}],
        )
        self.assertCountEqual(result["next_tags"], [])
        self.assertEqual(
            result["snippet"],
            '<article class="article" data-tags="A,B,C" id="id-39334"><h2>S2</h2></article>',
        )

    def test_invalid_tags_without_snippet(self):
        result = self.service_funnel.handle_request(
            {"selected_tags": [{"name": "F"}]}
        )
        self.assertEqual(result["status"]["code"], 2)
        self.assertEqual(result["status"]["msg"], "Invalid tags")
        self.assertEqual(result["selected_tags"], [{"name": "F"}])
        self.assertCountEqual(
            result["next_tags"],[])
        self.assertEqual(result["snippet"], None)

    def test_one_tag_match(self):
        result = self.service_funnel.handle_request(
            {"selected_tags": [{"name": "E"}]}
        )
        print(result)
        self.assertEqual(result["status"]["code"], 0)
        self.assertEqual(result["status"]["msg"], "Valid tags with snippet")
        self.assertEqual(
            result["selected_tags"], [{"name": "E"}]
        )
        self.assertCountEqual(result["next_tags"], [])
        self.assertEqual(
            result["snippet"],
            '<article class="article" data-tags="A,D,E" id="id-39334"><h2>S4</h2></article>')

if __name__ == "__main__":
    unittest.main()