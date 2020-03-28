import asyncio
import aiohttp
import sys
from bs4 import BeautifulSoup

async def translate(word):
    url = 'https://dictionary.cambridge.org/dictionary/english/' + word
    async with aiohttp.request('GET', url) as resp:
        html = await resp.text()
        return html

async def suggest(word):
    url = 'https://dictionary.cambridge.org/spellcheck/english/?q=' + word
    async with aiohttp.request('GET', url) as resp:
        html = await resp.text()
        return html

def getTranslate(word):
    url = asyncio.get_event_loop().run_until_complete(translate(word))
    soup = BeautifulSoup(url, 'html.parser')

    body = soup.findAll('div', attrs={'class': 'pr dictionary'})

    if len(body)!=0:
        pr1 = body[0]
        sb = pr1.findAll('div', attrs={'class': 'sense-body dsense_b'})
        dbs = [defs.findAll('div', attrs={'class': 'def-block ddef_block'}) for defs in sb]
        defBlocks=[defBlock for resultSet in dbs for defBlock in resultSet]
        definitions = [definition.findAll('div', attrs={'class': 'def ddef_d db'}) for definition in defBlocks]
        results=[result.text for resultSet in definitions for result in resultSet]
        examplesSet = [example.findAll('span', attrs={'class': 'eg deg'}) for example in defBlocks]
        examples = [[exList.text for exList in exSet] for exSet in examplesSet]

        searchResult = {}
        for dfn, exs in zip(results,examples):
            searchResult[dfn[:-2]] = exs

    else:
        return False

    return searchResult


def getSuggestions(word):
    url = asyncio.get_event_loop().run_until_complete(suggest(word))
    soup = BeautifulSoup(url, 'html.parser')

    body = soup.find('div', attrs={'class': 'x lmt-15'})
    suggs = body.findAll('li', attrs={'class':'lbt lp-5 lpl-20'})
    result= [item.text.strip() for item in suggs]
    return result
    


# if __name__ == "__main__":
#     if len(sys.argv) != 2 and type(sys.argv[1])!='str':
#         pass
#     else:
#         myWord=sys.argv[1]
#         a = getTranslate(myWord)
#         if a == False:
#             a = getSuggestions(myWord)

        # findAll('li', attrs={'class': 'lbt lp-5 lpl-20'})