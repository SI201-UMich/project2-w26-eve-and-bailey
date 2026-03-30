# Your name: Eve Orban and Bailey Ellul
# Your student id: 50136872 | 19398388
# Your email: eveorban@umich.edu | bellul@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Bailey Ellul
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    results = []
    with open(html_path, "r", encoding="utf-8-sig") as f:
        
        soup = BeautifulSoup(f.read(), 'html.parser')
     
        url_links = soup.find_all('a', href=True)
        for url in url_links: 
            href = url.get('href', '')

            pattern = re.findall(r'/rooms/(?:plus/)?(\d+)', href)
            if pattern: 
                listing_id = pattern[0]
                title_tag = url.find_next("div", {"data-testid": "listing-card-title"})
                listing_title = title_tag.get_text(strip=True) if title_tag else None
                # listing_title = f"Listing {listing_id}"
                if not listing_title:
                    continue
                if listing_id in [result[1] for result in results]:
                    continue
                results.append((listing_title, listing_id))

        return results

    # ==============================
    # pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    details = {}
    file_path = os.path.join(os.path.dirname(__file__), "html_files", f"listing_{listing_id}.html")
    # print(file_path)

    with open(file_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    full_text = soup.get_text(" ", strip=True)

    policy_number = ''
    if 'Pending' in full_text: 
        policy_number = 'Pending'
    elif 'Exempt' in full_text: 
        policy_number = 'Exempt'
    else: 
        policy_pattern = re.findall(r'([A-Z0-9\-]{6,})', full_text)
        if policy_pattern:
            policy_number = policy_pattern[0]
        else:
            policy_number = 'Pending'

    host_type = ''
    if 'Superhost' in full_text: 
        host_type = 'Superhost'
    else: 
        host_type = 'regular'

    host_name = '' 
    name_pattern = re.findall(r'Hosted by ([A-Za-z]+(?: [A-Za-z]+)*(?: And [A-Za-z]+(?: [A-Za-z]+)*)?)', full_text)
    if name_pattern:
        host_name = name_pattern[0].split("Joined")[0].strip()
    
    subtitle = soup.find("h2").get_text(strip=True)

    if 'Private' in subtitle:
        room_type = 'Private Room'
    elif 'Shared' in subtitle:
        room_type = 'Shared Room'
    else:
        room_type = 'Entire Room'
    
    location_rating = 0.0
    location_pattern = re.findall(r'Location\s*([0-9]\.[0-9])', full_text)
    if location_pattern:
        location_rating = float(location_pattern[0])

    details[listing_id] = {
        "policy_number": policy_number,
        "host_type": host_type,
        "host_name": host_name,
        "room_type": room_type, 
        "location_rating": location_rating
        }

    # print(details)
    return details
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    database = []

    listing_details = load_listing_results(html_path)

    for listing_title, listing_id in listing_details: 
        specific_details = get_listing_details(listing_id)[listing_id]

        database.append((
            listing_title,
            listing_id, 
            specific_details['policy_number'],
            specific_details['host_type'],
            specific_details['host_name'],
            specific_details['room_type'],  
            specific_details['location_rating']
        ))
    
    return database

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "listing_title", "listing_id", "policy_number", "host_type", "host_name", "room_type", "location_rating"   
        ])
    for row in sorted_data:
        writer.writerow(row)
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    totals = {}
    counts = {}
    for row in data: 
        room_type = row[5]
        rating = row[6]
        if rating == 0.0:
            continue
        if room_type not in totals:
            totals[room_type] = 0
            counts[room_type] = 0
        totals[room_type] += rating 
        counts[room_type] += 1
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid = []
    pattern = r'^STR-\d{7}$'
    for row in data:
        listing_id = row[1]
        policy_number = row[2]
        if policy_number in ["Pending", "Exempt"]:
            continue
        if not re.match(pattern, policy_number):
            invalid.append(listing_id)
    return invalid
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        # result = load_listing_results(self.search_results_path)
        self.assertEqual(len(self.listings), 18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))
        #pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        first_check = get_listing_details('467507')['467507']
        second_check = get_listing_details('1550913')['1550913']
        third_check = get_listing_details("1944564")['1944564']
        fourth_check = get_listing_details('4614763')['4614763']
        fifth_check = get_listing_details("6092596")['6092596']

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        self.assertEqual(first_check['policy_number'], "STR-0005349")
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        self.assertEqual(third_check['host_type'], 'Superhost')
        self.assertEqual(third_check['room_type'], 'Entire Room')
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(third_check['location_rating'], 4.9)
        # pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for tuple in self.detailed_data:
            self.assertEqual(len(tuple), 7)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(self.detailed_data[-1], ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8))
        # pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        out_path = os.path.join(self.base_dir, "test.csv")
        output_csv(self.detailed_data, out_path)
        rows = []
        with open(out_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)        
            rows = list(reader)
        self.assertEqual(
            rows[1]
            ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
        )
        os.remove(out_path)
    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        result = avg_location_rating_by_room_type(self.detailed_data)
        self.assertEqual(result["Private Room"], 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        self.assertEqual(invalid_listings, ["16204265"] )


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)