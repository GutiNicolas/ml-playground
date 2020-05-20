from enum import Enum
from selenium import webdriver
import time
from datetime import datetime
from datetime import date
from selenium.common.exceptions import  NoSuchElementException

class MELI_CONSTANTS(Enum):
    price_orders = ["", "*DESC"]
    realestate_url = 'https://listado.mercadolibre.com.uy/inmuebles/casas/venta/{}/_OrderId_PRICE{}_PriceRange_{}USD-{}USD'
    price_ranges = [("100000", "240000"), ("50000", "120000"), ("72000", "139000")]
    target_citis = ['montevideo']
    Total_surface = 'total_surface_sq_meters'
    Superficie_total = 'Superficie total'
    Superficie_terreno = 'Superficie del terreno (m²)'
    Build_surface = 'builded_surface_sq_meters'
    Superficie_cubierta = 'Superficie cubierta'
    Superficie_construida = 'Superficie construida (m²)'
    Cocheras = 'Cocheras'
    Garages = 'garages'
    Antiguedad = 'Antigüedad'
    Property_age = 'property_age'
    Pisos = 'Pisos'
    Plantas = 'Plantas'
    Property_floors = 'property_floors'
    Gastos_comunes = 'Gastos comunes'
    Common_expenses = 'common_expenses'
    Orientacion = 'Orientación'
    Orientation = 'orientation'
    Tipo_de_casa = 'Tipo de casa'
    Inmueble = 'Inmueble'
    Tipo_de_edificaion = 'Tipo de edificación'
    Property_type = 'property_type'
    Ambientes = 'Ambientes'
    Rooms = 'rooms'



def get_order(order):
    return 'high' if len(order) > 2 else 'low'


def get_attrs(attrs):
    meters = None
    dorms = None
    if "|" in attrs:
        meters = attrs.split('|')[0].split(None, 1)[0].replace(",", "").replace(".", "")
        dorms = attrs.split('|')[1].split(None, 1)[0].replace(",", "").replace(".", "")
    elif "dorms" in attrs:
        dorms = attrs.split(None, 1)[0].replace(",", "").replace(".", "")
    elif "m²" in attrs:
        meters = attrs.split(None, 1)[0].replace(",", "").replace(".", "")
    return meters, dorms


def get_address(address):
    addr = None
    nbhood = None
    if address is not None and address.count(',') == 1:
        addr = address.split(',')[0].strip().title()
        nbhood = address.split(',')[1].strip().title()
    elif address is not None:
        nbhood = address
    return addr, nbhood


def map_label(label):
    if label == MELI_CONSTANTS.Superficie_total.value or label == MELI_CONSTANTS.Superficie_terreno.value:
        return MELI_CONSTANTS.Total_surface.value
    elif label == MELI_CONSTANTS.Superficie_cubierta.value or label == MELI_CONSTANTS.Superficie_construida.value:
        return MELI_CONSTANTS.Build_surface.value
    elif label == MELI_CONSTANTS.Cocheras.value:
        return MELI_CONSTANTS.Garages.value
    elif label == MELI_CONSTANTS.Antiguedad.value:
        return MELI_CONSTANTS.Property_age.value
    elif label == MELI_CONSTANTS.Pisos.value or label == MELI_CONSTANTS.Plantas.value:
        return MELI_CONSTANTS.Property_floors.value
    elif label == MELI_CONSTANTS.Gastos_comunes.value:
        return MELI_CONSTANTS.Common_expenses.value
    elif label == MELI_CONSTANTS.Orientacion.value:
        return MELI_CONSTANTS.Orientation.value
    elif label == MELI_CONSTANTS.Tipo_de_casa.value or label == MELI_CONSTANTS.Tipo_de_edificaion.value or label == MELI_CONSTANTS.Inmueble.value:
        return MELI_CONSTANTS.Property_type.value
    elif label == MELI_CONSTANTS.Ambientes.value:
        return MELI_CONSTANTS.Rooms.value
    else:
        return label


def get_currency(value):
    return 'USD' if value is not None and 'USD' in value.upper() else 'UYU'


def map_cp(cp):
    if cp is None:
        return
    if cp == 'Sur':
        return 'South'
    elif cp == 'Norte':
        return 'North'
    elif cp == 'Este':
        return 'East'
    elif cp == 'Oeste':
        return 'West'
    else:
        return cp


def map_val(value):
    try:
        val = value.split(None, 1)[0]
        return val
    except (ValueError, IndexError):
        return value


driver = webdriver.Firefox()
date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
res = []
not_found = set()
not_found_with_vals = {}
save_duplicates = False
for city in MELI_CONSTANTS.target_citis.value:
    for order_by in MELI_CONSTANTS.price_orders.value:
        for p_r in MELI_CONSTANTS.price_ranges.value:
            links = []
            driver.get(MELI_CONSTANTS.realestate_url.value.format(city, order_by, p_r[0], p_r[1]))
            time.sleep(2)
            item_cards = driver.find_elements_by_class_name('results-item')
            print('[INFO] Getting items for {} order {}'.format(city, order_by))
            for card in item_cards:
                if card is None:
                    break
                link = card.find_element_by_class_name('item__info-link').get_attribute('href')
                links.append(link)

            for link in links:
                if link is None:
                    break
                driver.get(link)
                price = driver.find_element_by_class_name('price-tag-fraction').text
                item_id = driver.find_element_by_name('item_id').get_property('value')
                address = driver.find_element_by_class_name('item-title__primary').text
                meters = None
                try:
                    meters = driver.find_element_by_class_name('align-surface').text.split(None, 1)[0]
                except ( NoSuchElementException, IndexError):
                    print('[WARN] SQ Meters not found on item {}'.format(item_id))
                dorms = driver.find_element_by_class_name('align-room').text.split(None, 1)[0]
                barhs = None
                try:
                    baths = driver.find_element_by_class_name('align-bathroom').text.split(None, 1)[0]
                except (NoSuchElementException, IndexError):
                    print('[WARN] No Baths found on item {}'.format(item_id))
                addr, nbhood = get_address(address)
                d = {'id': item_id, 'price': price.replace(".", ""), 'square_meters': meters, 'dorms': dorms,
                     'city': city.title(), 'neighborhood': nbhood, 'address': addr, 'date': date,
                    'order_type': get_order(order_by), 'bathrooms': baths, MELI_CONSTANTS.Total_surface.value: None,
                    MELI_CONSTANTS.Build_surface.value: None, MELI_CONSTANTS.Garages.value: None,
                    MELI_CONSTANTS.Property_age.value: None, MELI_CONSTANTS.Property_floors.value: None,
                    MELI_CONSTANTS.Common_expenses.value: None, MELI_CONSTANTS.Orientation.value: None,
                    MELI_CONSTANTS.Property_type.value: None, MELI_CONSTANTS.Rooms.value: None}
                specs = driver.find_element_by_class_name('specs-list')
                for spec in specs.find_elements_by_tag_name('li'):
                    if spec is None:
                        break
                    label = spec.find_element_by_tag_name('strong').text
                    value = spec.find_element_by_tag_name('span').text
                    if label != map_label(label):
                        if d[map_label(label)] is None:
                            if label == MELI_CONSTANTS.Orientacion.value:
                                d[map_label(label)] = map_cp(value)
                            else:
                                d[map_label(label)] = map_val(value)
                            if label == MELI_CONSTANTS.Gastos_comunes.value:
                                d['common_expenses_currency'] = get_currency(value)
                        else:
                            print('\n[WARN] Value already exists')
                            print('Value for label {} already exists: {}'.format(map_label(label), d[map_label(label)]))
                            clean_label = label.lower().strip().replace(" ", "_")
                            if d[map_label(label)] != map_val(value) and save_duplicates:
                                print('Storing new value({}) with created label {}'.format(map_val(value), clean_label))
                                d[clean_label] = map_val(value)
                            else:
                                print('Not saving {} because value matches old value or saving duplicates is off? {}'.format(map_val(value), not save_duplicates))
                    else:
                        if label not in not_found:
                            not_found.add(label)
                            not_found_with_vals[label] = {'value': value, 'link': link}
                res.append(d)

for nf in not_found:
    print("\n[WARN] No mapping found for '{}'".format(nf))
    print("Missed value example: '{}'".format(not_found_with_vals[nf]['value']))
    print("See more on mercadolibre at {}".format(not_found_with_vals[nf]['link']))

save = open('data/realestate/data.csv', 'a')
sep = ";"
keys = list(res[0].keys())
save_first = False
if save_first:
    first_line = "{}\n".format(sep.join(keys))
    save.write(first_line)
lines = []
for property in res:
    values = []
    for key in keys:
        values.append(property[key] if property[key] is not None else 'None')
    line = "{}\n".format(sep.join(values))
    lines.append(line)
    print(line)
save.writelines(lines)
save.close()

