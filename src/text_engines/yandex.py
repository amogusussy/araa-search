import json
from urllib.parse import urlencode, unquote
from src import helpers
from src.text_engines.objects.fullEngineResults import FullEngineResults
from src.text_engines.objects.textResult import TextResult


url_args = {
    "lr:": 109560,
    "msid": "1731247888309154-911837082813266234-balancer-l7leveler-kubr-yp-klg-243-BAL",
    "search_source": "yacom_desktop_common",
    "suggest_reqid": 583322468173124780878886042737036
}

results_path = "li.serp-item"
url_path = "a.b-serp-item__title-link"
title_path = "h3.b-serp-item__title a.b-serp-item__title-link span"
desc_path = "div.b-serp-item__content div.b-serp-item__text"


def gen_url(query, page):
    args = url_args.copy()
    args["text"] = query

    if page > 1:
        args["p"] = page - 1

    print(args)

    return "https://yandex.com/search/site/" + urlencode(args)


def search(query: str, page: int, search_type: str, user_settings: helpers.Settings):
    if search_type == "reddit":
        query += " site:reddit.com"
    url = gen_url(query, page)

    html, code = helpers.makeHTMLRequest(url, is_yandex=True)

    if code != 200:
        return FullEngineResults(
            engine="yandex",
            search_type=search_type,
            ok=False,
            code=code
        )

    results = []
    for result in html.select(results_path):
        print(result)
        results.append(TextResult(
            title=result.select(title_path)[0].get_text(),
            desc=result.select(desc_path)[0].get_text(),
            url=unquote(result.select(url_path)[0].get("href", "")),
            sublinks=[]
        ))


    return FullEngineResults(
        engine = "yandex",
        search_type = search_type,
        ok = True,
        code = 200,
        results = results,
        wiki = None,
        featured = None,
        correction = None,
        top_result_sublinks = [],
    )
