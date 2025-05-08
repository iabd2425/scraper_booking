import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
from urllib.parse import urlparse, parse_qs

def scrape_booking_almeria(checkin_date, checkout_date):
    """
    Scrapes hotel data from Booking.com for Almería province.

    Args:
        checkin_date (str): Check-in date in 'YYYY-MM-DD' format.
        checkout_date (str): Check-out date in 'YYYY-MM-DD' format.

    Returns:
        list: A list of dictionaries, where each dictionary represents a hotel.
    """
    # Base URL for Booking.com search results for Almería
    # You might need to find the correct URL for Almería province specifically.
    # This is a placeholder URL, you'll need to replace it with the actual one.
    # The dates and currency will be added as query parameters.
    # Added selected_currency=EUR to try and force EUR prices.
    base_url = "https://www.booking.com/searchresults.es.html?lang=es%E2%82%AC&dest_id=1363&dest_type=region&ac_langcode=es&nflt=ht_id%3D204&shw_aparth=0&selected_currency=EUR&checkin={}&checkout={}"
    url = base_url.format(checkin_date, checkout_date)

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    ]
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    hotel_list = []

    try:
        # Add a random delay before making the request
        time.sleep(random.uniform(2, 5)) # Delay between 2 and 5 seconds

        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all hotel listings on the page
        # You'll need to inspect the HTML of the search results page
        # to find the correct selector for individual hotel listings.
        # This is a placeholder selector.
        hotels = soup.select('div[data-testid="property-card"]')

        for hotel in hotels:
            hotel_data = {}

            # Extract data points
            # You'll need to inspect the HTML for each data point and find its selector.
            # These are placeholder selectors and logic.

            # URL hotel (sin fechas)
            try:
                hotel_url_element = hotel.select_one('a[data-testid="title-link"]')
                if hotel_url_element and 'href' in hotel_url_element.attrs:
                    full_url = hotel_url_element['href']
                    # Remove date parameters from URL
                    clean_url = full_url.split('?')[0]
                    hotel_data['URL hotel'] = clean_url

                    # Extract ID from 'aid' parameter in the URL
                    parsed_url = urlparse(full_url)
                    query_params = parse_qs(parsed_url.query)
                    aid = query_params.get('aid', [None])[0] # Get the first value of 'aid'
                    hotel_data['ID Hotel'] = aid

                else:
                    hotel_data['URL hotel'] = None
                    hotel_data['ID Hotel'] = None
            except Exception as e:
                print(f"Error extracting URL or Hotel ID: {e}")
                hotel_data['URL hotel'] = None
                hotel_data['ID Hotel'] = None

            # Nombre
            try:
                name_element = hotel.select_one('div[data-testid="title"]')
                hotel_data['Nombre'] = name_element.get_text(strip=True) if name_element else None
            except Exception as e:
                print(f"Error extracting Nombre: {e}")
                hotel_data['Nombre'] = None

            # Marca (Often not directly available on search results, might need to visit hotel page)
            hotel_data['Marca'] = None # Placeholder

            # Dirección
            try:
                address_element = hotel.select_one('span[data-testid="address"]')
                hotel_data['Dirección'] = address_element.get_text(strip=True) if address_element else None
            except Exception as e:
                print(f"Error extracting Dirección: {e}")
                hotel_data['Dirección'] = None

            # Coordenadas (Often not directly available on search results, might need to visit hotel page or use geocoding)
            hotel_data['Coordenadas'] = None # Placeholder

            # Servicios populares (Often not directly available on search results, might need to visit hotel page)
            hotel_data['Servicios populares'] = None # Placeholder

            # ¿Mascotas? (Often not directly available on search results, might need to visit hotel page)
            hotel_data['¿Mascotas?'] = None # Placeholder

            # Descripción (Often not fully available on search results, might need to visit hotel page)
            hotel_data['Descripción'] = None # Placeholder

            # Puntuación, Opinión, Numero comentarios
            # Puntuación, Opinión, Numero comentarios
            try:
                review_score_container = hotel.select_one('div[data-testid="review-score"]')
                if review_score_container:
                    # Get all direct child div texts
                    score_texts = [div.get_text(strip=True) for div in review_score_container.select(':scope > div')]

                    # Assign based on index, similar to the provided snippet
                    # Puntuación (numeric value from index 0)
                    if len(score_texts) > 0 and score_texts[0]:
                        match = re.search(r'\d+(\.\d+)?', score_texts[0])
                        hotel_data['Puntuación'] = match.group(0) if match else None
                    else:
                        hotel_data['Puntuación'] = None

                    # Opinión (from index 1)
                    hotel_data['Opinión'] = score_texts[1] if len(score_texts) > 1 and score_texts[1] else None

                    # Numero comentarios (numeric value from index 2 using split)
                    if len(score_texts) > 2 and score_texts[2]:
                        num_comments_text = score_texts[2]
                        # Use regex to find the number of comments
                        match = re.search(r'\d+', num_comments_text)
                        # Use regex to find the number of comments and append " comentarios"
                        match = re.search(r'\d+', num_comments_text)
                        hotel_data['Numero comentarios'] = f"{match.group(0)} comentarios" if match else None
                    else:
                        hotel_data['Numero comentarios'] = None

                else:
                    hotel_data['Puntuación'] = None
                    hotel_data['Opinión'] = None
                    hotel_data['Numero comentarios'] = None

            except Exception as e:
                print(f"Error extracting Puntuación, Opinión, or Numero comentarios: {e}")
                hotel_data['Puntuación'] = None
                hotel_data['Opinión'] = None
                hotel_data['Numero comentarios'] = None


            # Fecha entrada (Provided by user)
            hotel_data['Fecha entrada'] = checkin_date

            # Fecha salida (Provided by user)
            hotel_data['Fecha salida'] = checkout_date

            # Precio
            try:
                price_element = hotel.select_one('span[data-testid="price-and-discounted-price"]')
                if price_element:
                     hotel_data['Precio'] = price_element.get_text(strip=True)
                else:
                    # Sometimes the price is in a different structure
                    price_element_alt = hotel.select_one('div[data-testid="price-and-discounted-price"] span')
                    hotel_data['Precio'] = price_element_alt.get_text(strip=True) if price_element_alt else None

            except Exception as e:
                print(f"Error extracting Precio: {e}")
                hotel_data['Precio'] = None


            # Scrape additional details from the hotel's individual page
            if hotel_data.get('URL hotel'):
                hotel_details = scrape_hotel_details(hotel_data['URL hotel'])
                if hotel_details:
                    # Construct the dictionary in the desired order
                    ordered_hotel_data = {
                        'URL hotel': hotel_data.get('URL hotel'),
                        'ID Hotel': hotel_data.get('ID Hotel'),
                        'Nombre': hotel_data.get('Nombre'),
                        'Marca': hotel_details.get('Marca'), # Get Marca from hotel_details
                        'Destacados': hotel_details.get('Destacados'), # Add Destacados
                        'Dirección': hotel_data.get('Dirección'),
                        'Coordenadas': hotel_details.get('Coordenadas'), # Get Coordenadas from hotel_details
                        'Servicios populares': hotel_details.get('Servicios populares'), # Get Servicios populares from hotel_details
                        '¿Mascotas?': hotel_details.get('¿Mascotas?'), # Get ¿Mascotas? from hotel_details
                        'Descripción': hotel_details.get('Descripción'), # Get Descripción from hotel_details
                        'Puntuación': hotel_data.get('Puntuación'),
                        'Opinión': hotel_data.get('Opinión'),
                        'Numero comentarios': hotel_data.get('Numero comentarios'),
                        'Fecha entrada': hotel_data.get('Fecha entrada'),
                        'Fecha salida': hotel_data.get('Fecha salida'),
                        'Precio': hotel_data.get('Precio'),
                    }
                    # Remove keys with None or empty list values to keep the output clean
                    hotel_data = {k: v for k, v in ordered_hotel_data.items() if v is not None and v != []}


            hotel_list.append(hotel_data)

        # TODO: Implement pagination if needed

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

    return hotel_list

def scrape_hotel_details(hotel_url):
    """
    Scrapes additional details from an individual hotel page on Booking.com.

    Args:
        hotel_url (str): The URL of the individual hotel page.

    Returns:
        dict: A dictionary containing additional hotel details.
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    ]
    headers = {
        'User-Agent': random.choice(user_agents)
    }

    details = {}

    try:
        # Add a random delay before making the request
        time.sleep(random.uniform(2, 5)) # Delay between 2 and 5 seconds

        response = requests.get(hotel_url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract additional data points from the hotel page
        # You'll need to inspect the HTML of an individual hotel page
        # to find the correct selectors for each data point.
        # These are placeholder selectors and logic.

        # Destacados
        # Destacados
        try:
            # Use the corrected selector for the main container of Destacados
            highlight_container = soup.select_one('span.hp__hotel_ratings.pp-header__badges.pp-header__badges--combined div[data-capla-component-boundary="b-property-web-property-page/Badges"]')
            if highlight_container:
                # Select all direct child elements within the container
                highlight_elements = highlight_container.select(':scope > *')
                # Extract text from each child element and store in a list
                details['Destacados'] = [elem.get_text(strip=True) for elem in highlight_elements if elem.get_text(strip=True)]
            else:
                details['Destacados'] = None # Or an empty list []

        except Exception as e:
            print(f"Error extracting Destacados from {hotel_url}: {e}")
            details['Destacados'] = None # Or an empty list []

        # Marca
        try:
            brand_element = soup.select_one('div.d7b319a0ec div.b08850ce41')
            details['Marca'] = brand_element.get_text(strip=True) if brand_element else None
        except Exception as e:
            print(f"Error extracting Marca from {hotel_url}: {e}")
            details['Marca'] = None

        # Coordenadas
        try:
            coords_element = soup.select_one('a#map_trigger_header_pin')
            if coords_element and 'data-atlas-latlng' in coords_element.attrs:
                details['Coordenadas'] = coords_element['data-atlas-latlng']
            else:
                # Fallback to meta tags if the primary selector is not found
                lat_meta = soup.find('meta', {'property': 'booking_com:location:latitude'})
                lon_meta = soup.find('meta', {'property': 'booking_com:location:longitude'})
                coords_content = None
                if lat_meta and 'content' in lat_meta.attrs and lon_meta and 'content' in lon_meta.attrs:
                    coords_content = f"{lat_meta['content']},{lon_meta['content']}"

                if not coords_content or coords_content == ',':
                     # Try alternative meta tag
                     geo_position_meta = soup.find('meta', {'name': 'geo.position'})
                     if geo_position_meta and 'content' in geo_position_meta.attrs:
                          coords_content = geo_position_meta['content']

                details['Coordenadas'] = coords_content if coords_content and coords_content != ',' else None

        except Exception as e:
            print(f"Error extracting Coordenadas from {hotel_url}: {e}")
            details['Coordenadas'] = None

        # Servicios populares
        try:
            amenities_list = soup.select('div.hp--popular_facilities ul.e9f7361569 li.b0bf4dc58f div.aa8988bf9c span.f006e3fcbd')
            details['Servicios populares'] = [amenity.get_text(strip=True) for amenity in amenities_list] if amenities_list else None
        except Exception as e:
            print(f"Error extracting Servicios populares from {hotel_url}: {e}")
            details['Servicios populares'] = None

        # ¿Mascotas?
        try:
            # Find the element containing "Mascotas" and then the following div with the policy
            pets_header = soup.find('div', class_='dace71f323', string=re.compile(r'Mascotas', re.IGNORECASE))
            if pets_header:
                pets_policy_element = pets_header.find_next_sibling('div', class_='c92998be48')
                if pets_policy_element:
                    policy_text = pets_policy_element.get_text(strip=True)
                    details['¿Mascotas?'] = "Sí se admiten" if "se admiten" in policy_text.lower() else "No se admiten"
                else:
                     details['¿Mascotas?'] = "Información no disponible"
            else:
                details['¿Mascotas?'] = "Información no disponible"
        except Exception as e:
            print(f"Error extracting ¿Mascotas? from {hotel_url}: {e}")
            details['¿Mascotas?'] = "Error al extraer"

        # Descripción
        try:
            description_element = soup.select_one('p[data-testid="property-description"]')
            details['Descripción'] = description_element.get_text(strip=True) if description_element else None
        except Exception as e:
            print(f"Error extracting Descripción from {hotel_url}: {e}")
            details['Descripción'] = None

        # Precio (Already extracted from search results, but confirming selector if needed)
        # The price on the individual page might be different or more detailed.
        # For now, we'll rely on the price from the search results as requested initially.
        # If a more specific price from the hotel page is needed, this section would be updated.
        # try:
        #     price_element = soup.select_one('selector_for_price_on_hotel_page')
        #     details['Precio'] = price_element.get_text(strip=True) if price_element else None
        # except Exception as e:
        #     print(f"Error extracting Precio from {hotel_url}: {e}")
        #     details['Precio'] = None


    except requests.exceptions.RequestException as e:
        print(f"Error fetching hotel page {hotel_url}: {e}")
        return None

    return details

if __name__ == "__main__":
    # Use the dates provided by the user
    checkin = "2025-05-08"
    checkout = "2025-05-09"

    print(f"Starting scraping for Almería from {checkin} to {checkout}...")
    hotels_data = scrape_booking_almeria(checkin, checkout)

    if hotels_data:
        output_filename = "booking_almeria_hotels.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(hotels_data, f, ensure_ascii=False, indent=4)
        print(f"Scraping finished. Data saved to {output_filename}")
    else:
        print("Scraping failed.")
