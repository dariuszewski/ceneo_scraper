import requests, re
from bs4 import BeautifulSoup
import report_defs as rd

def scraper(category, parameters, formatting):

    parameters = parameters.replace(' ', '+').lower()
    dataset = {}

    page = 0
    url = f'https://www.ceneo.pl/{category};szukaj-{parameters};0020-30-0-0-{page}.htm'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    #sour_soup if the parameters are incorrect
    sour_soup = soup.select('div[class="not-found"]')
    if len(sour_soup) > 0:
        report = 'Brak produktów dla podanych parametrów.'
        return report


    while True:
        #print('this is page ' + str(page)) -> this will let you know what page u are on / how many it scraped
        soup = BeautifulSoup(res.text, 'lxml')
        offers = soup.select('div[class="cat-prod-row__content"]')
        for offer in offers:
	#some of the selectors differ depending on product
            try:
                id_and_name = offer.select('a[class="js_seoUrl js_clickHash go-to-product"]')
                id = id_and_name[0]['href']
                name = id_and_name[0]['title']

            except IndexError:
                try:
                    id_selector = offer.select('a[class="cat-prod-row__product-link"]')
                    id = id_selector[0]['href']
                    name_selector = offer.select('a[class="js_seoUrl js_clickHash go-to-shop"]')
                    name = name_selector[0]['title']

                except:
                    pass

            price_selector = offer.select('span[class="price"]')
            price = float(str(price_selector[0].text).replace(',', '.').replace(' ', ''))

            try:
                score_selector = offer.select('span[class="product-score"]')
                score = float(score_selector[0].text[1:4].replace(',','.'))
                reviews_selector = offer.select('span[class="prod-review__qo"]')
                reviews = int(re.sub('[^0-9]', '', reviews_selector[0].text.strip()))

            except IndexError:
                score = None
                reviews = 0

            except ValueError:
                score = None
                reviews = 0

            try:
                avability_selector = offer.select('span[class="shop-numb"]')
                avability = int(re.sub('[^0-9]', '', avability_selector[0].text.strip()))
            except ValueError:
                avability = 0
            except IndexError:
                avability = 0


            dataset[id[:9]] = {'name' : name, 'price' : price, 'score' : score,
                            'reviews' : reviews, 'avability' : avability}


            params = offer.select('ul[class="prod-params cat-prod-row__params"] li')
            for param in params:

                param_name = param.text[:param.text.index(':')]
                for product in dataset:
                    dataset[product][param_name] = 'No info'

                try:
                    if re.match(r'[0-9]', param.text[param.text.index(':')+2:]):
                        dataset[product][param_name] = float(re.sub('[^0-9,]', '',
                        param.text[param.text.index(':')+2:]).replace(',','.'))
                    else:
                        dataset[product][param_name] = param.text[param.text.index(':')+2:]
                except:
                    dataset[product][param_name] = 'No info'


        page +=1
        url = f'https://www.ceneo.pl/{category};szukaj-{parameters};0020-30-0-0-{page}.htm'
        res = requests.get(url)
        #condition at the end of the loop
        if res.request.url == f'https://www.ceneo.pl/{category};szukaj-{parameters}':
            break


    functions = {
    'Python dict' : rd.report_pydict(dataset),
    'JSON' : rd.report_json(dataset),
    'CSV' : rd.report_csv(dataset),
    'Short text' : rd.txt_short_report(dataset),
    'XML' : rd.xml_report(dataset)
    }

    return functions[formatting]
