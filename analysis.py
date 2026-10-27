import json
from pathlib import Path 

import matplotlib.pyplot as plt 
import pandas as pd 
import requests 

API_URL = "https://jsonplaceholder.typicode.com/users" 

def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try: 
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch customers: {e}")
        return[]

def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items():
        print(f"{'  '* indent}{key}: {type(value).__name__}")
        if isinstance(value, dict):
            explore(value, indent + 1)

def extract_attributes(customers: list[dict]) -> list[dict]:
    """Returns aone flat dict per customer with the attribute listed in the task."""
    rows = []
    for customer in customers:
        row = {
            "customer_id": customer["id"],
            "name": customer["name"],
            "username": customer["username"],
            "email": customer["email"],
            "phone": customer["phone"],
            "website": customer["website"],
            "city": customer["address"]["city"],
            "zipcode": customer["address"]["zipcode"],
            "latitude": float(customer["address"]["geo"]["lat"]),
            "longitude": float(customer["address"]["geo"]["lng"]),
            "company": customer["company"]["name"],
            "email_domain": customer["email"].split(".")[-1],


        }
        rows.append(row)
    return rows

def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {customer["address"]["city"] for customer in customers}

def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop."""
    counts = {}
    for customer in customers:
        city = customer["address"]["city"]
        counts[city] = counts.get(city, 0) + 1
    return counts

def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top domain. """
    domains = [customer["email"].split(".")[-1] for customer in customers]
    return {domain: domains.count(domain) for domain in set(domains)}

def sort_counts(counts: dict[str, int]) -> dict[str, int]:
    """Returns the counts sorted from most to least common."""
    return dict(sorted(counts.items(), key = lambda pair: (-pair[1],pair[0])))

def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert the flat customer rows into a pandas DataFrame."""
    columns = [
        "customer_id", "name", "username", "email", "email_domain", "phone",
        "city", "zipcode", "latitude", "longitude","company","website",
    ]
    return pd.DataFrame(rows)[columns]

def export_csvs(df: pd.DataFrame, counts: dict[str,int], out_dir: Path) -> None:
    """Write customers.csv and city-counts.csv into out-dir, without the pandas index. """
    out_dir.mkdir(exist_ok = True)
    df.to_csv(out_dir / "customers.csv", index = False)
    city_df = pd.DataFrame(list(counts.items()),columns = ["city","customer_count"])
    city_df.to_csv(out_dir / "city_counts.csv", index = False) 

def plot_distribution(counts: dict[str, int], path: Path, title: str = "customers per category", xlabel: str = "category") -> None:
    """Save a labelled chart of the distribution to path."""
    path.parent.mkdir(exist_ok = True)
    plt.figure(figsize = (10, 5))
    plt.bar(list(counts.keys()), list(counts.values()))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of customers")
    plt.xticks(rotation = 45, ha = "right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()







if __name__ == "__main__":
    customers = get_customers()
    print(len(customers))
    explore(customers[0])
    print(extract_attributes(customers)[0])
    cities = unique_cities(customers)
    print(len(cities), "unique cities for", len(customers),"customers")
    # print(city_counts(customers))
    # print(email_domain_counts(customers))
    print(sort_counts(city_counts(customers)))
    print(sort_counts(email_domain_counts(customers)))
    df = to_dataframe(extract_attributes(customers))
    print(df.shape)
    print(df.dtypes)
    print(df["email_domain"].value_counts())
    export_csvs(df, sort_counts(city_counts(customers)), Path("output"))
    plot_distribution(sort_counts(city_counts(customers)),Path("output/customer_distribution.png"),"customers per city", "city")
    plot_distribution(sort_counts(email_domain_counts(customers)), Path("output/email_domain_distribution.png"),"customers per email domain", "email domain")
    print("chart saved to    :output/customer_distribution.png")
    print("customere retrieved :", len(customers))
    print("unique cities       :",len(cities))
    top_city, top_n = next(iter(sort_counts(city_counts(customers)).items()))
    print(f"Most common city   : {top_city} ({top_n})")
    print("Email domains       :",sort_counts(email_domain_counts(customers)))