import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random

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
    # The dates will be added as query parameters.
    base_url = "https://www.booking.com/searchresults.es.html?lang=es%E2%82%AC&dest_id=1363&dest_type=region&ac_langcode=es&nflt=ht_id%3D204&shw_aparth=0&checkin={}&checkout={}"
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
                    hotel_data['URL hotel'] = full_url.split('?')[0]
                else:
                    hotel_data['URL hotel'] = None
            except Exception as e:
                print(f"Error extracting URL: {e}")
                hotel_data['URL hotel'] = None

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

            # Estrellas
            try:
                stars_element = hotel.select_one('span[data-testid="rating-stars"]')
                if stars_element and 'aria-label' in stars_element.attrs:
                     hotel_data['Estrellas'] = stars_element['aria-label']
                else:
                    hotel_data['Estrellas'] = None
            except Exception as e:
                print(f"Error extracting Estrellas: {e}")
                hotel_data['Estrellas'] = None


            # Servicios populares (Often not directly available on search results, might need to visit hotel page)
            hotel_data['Servicios populares'] = None # Placeholder

            # ¿Mascotas? (Often not directly available on search results, might need to visit hotel page)
            hotel_data['¿Mascotas?'] = None # Placeholder

            # Descripción (Often not fully available on search results, might need to visit hotel page)
            hotel_data['Descripción'] = None # Placeholder

            # Puntuación
            try:
                score_element = hotel.select_one('div[data-testid="review-score"] div:first-child')
                hotel_data['Puntuación'] = score_element.get_text(strip=True) if score_element else None
            except Exception as e:
                print(f"Error extracting Puntuación: {e}")
                hotel_data['Puntuación'] = None

            # ¿Puntuación Ubicación? (Often not directly available on search results, might need to visit hotel page)
            hotel_data['¿Puntuación Ubicación?'] = None # Placeholder

            # Opinión (e.g., Bien, Muy bien)
            try:
                opinion_element = hotel.select_one('div[data-testid="review-score"] div:nth-child(2) div:first-child')
                hotel_data['Opinión'] = opinion_element.get_text(strip=True) if opinion_element else None
            except Exception as e:
                print(f"Error extracting Opinión: {e}")
                hotel_data['Opinión'] = None

            # Numero comentarios
            try:
                num_comments_element = hotel.select_one('div[data-testid="review-score"] div:nth-child(2) div:nth-child(2)')
                if num_comments_element:
                    # Extract only the number
                    num_comments_text = num_comments_element.get_text(strip=True)
                    match = re.search(r'\d+', num_comments_text)
                    hotel_data['Numero comentarios'] = match.group(0) if match else None
                else:
                    hotel_data['Numero comentarios'] = None
            except Exception as e:
                print(f"Error extracting Numero comentarios: {e}")
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
                    hotel_data.update(hotel_details)

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

        # Marca (Selector supuesto)
        try:
            # This is highly speculative, might need adjustment
            brand_element = soup.select_one('div.hp__hotel-type') # Example selector
            details['Marca'] = brand_element.get_text(strip=True) if brand_element else None
        except Exception as e:
            print(f"Error extracting Marca from {hotel_url}: {e}")
            details['Marca'] = None

        # Coordenadas (Selector supuesto)
        try:
            # Look for a meta tag with geo.position
            coords_meta = soup.find('meta', {'name': 'geo.position'})
            if coords_meta and 'content' in coords_meta.attrs:
                details['Coordenadas'] = coords_meta['content']
            else:
                details['Coordenadas'] = None
        except Exception as e:
            print(f"Error extracting Coordenadas from {hotel_url}: {e}")
            details['Coordenadas'] = None

        # Servicios populares (Selector supuesto)
        try:
            # Look for a section with amenities and list items
            amenities_list = soup.select('div.hp_facilities_group div.hp_facilities_list li') # Example selector
            details['Servicios populares'] = [amenity.get_text(strip=True) for amenity in amenities_list] if amenities_list else None
        except Exception as e:
            print(f"Error extracting Servicios populares from {hotel_url}: {e}")
            details['Servicios populares'] = None

        # ¿Mascotas? (Selector supuesto)
        try:
            # Look for text indicating pet policy
            pets_element = soup.find(text=re.compile(r'mascotas', re.IGNORECASE))
            if pets_element:
                # This is a very basic check, might need more sophisticated logic
                details['¿Mascotas?'] = "Sí se admiten" if "se admiten" in pets_element.lower() else "No se admiten"
            else:
                details['¿Mascotas?'] = "Información no disponible"
        except Exception as e:
            print(f"Error extracting ¿Mascotas? from {hotel_url}: {e}")
            details['¿Mascotas?'] = "Error al extraer"

        # Descripción (Selector supuesto)
        try:
            # Look for a description section
            description_element = soup.select_one('div#property_description_content') # Example selector
            details['Descripción'] = description_element.get_text(strip=True) if description_element else None
        except Exception as e:
            print(f"Error extracting Descripción from {hotel_url}: {e}")
            details['Descripción'] = None

        # ¿Puntuación Ubicación? (Selector supuesto)
        try:
            # Look for location score near reviews
            location_score_element = soup.select_one('div.bui-review-score__content span.bui-review-score__title + span.bui-review-score__score') # Example selector
            if location_score_element and "ubicación" in location_score_element.find_previous('span', class_='bui-review-score__title').get_text(strip=True).lower():
                 details['¿Puntuación Ubicación?'] = location_score_element.get_text(strip=True)
            else:
                details['¿Puntuación Ubicación?'] = None
        except Exception as e:
            print(f"Error extracting ¿Puntuación Ubicación? from {hotel_url}: {e}")
            details['¿Puntuación Ubicación?'] = None


    except requests.exceptions.RequestException as e:
        print(f"Error fetching hotel page {hotel_url}: {e}")
        return None

    return details

if __name__ == "__main__":
    # Use the dates provided by the user
    checkin = "2025-05-06"
    checkout = "2025-05-07"

    print(f"Starting scraping for Almería from {checkin} to {checkout}...")
    hotels_data = scrape_booking_almeria(checkin, checkout)

    if hotels_data:
        output_filename = "booking_almeria_hotels.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(hotels_data, f, ensure_ascii=False, indent=4)
        print(f"Scraping finished. Data saved to {output_filename}")
    else:
        print("Scraping failed.")
