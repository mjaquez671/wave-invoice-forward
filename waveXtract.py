import requests
from datetime import datetime


class WaveInvoiceManager:
    def __init__(self, auth_token, business_id):
        self.auth_token = auth_token
        self.business_id = business_id
        self.url = "https://gql.waveapps.com/graphql/public"
        self.response_data = None

    def fetch_invoice_data(self, query, variables=None):
        """Execute a GraphQL query and return the response."""
        headers = {"Authorization": self.auth_token, "Content-Type": "application/json"}
        json_data = {
            "query": query,
            "variables": variables,
        }
        response = requests.post(self.url, json=json_data, headers=headers)
        self.response_data = response.json()
        return self.response_data

    @staticmethod
    def format_date(date_str):
        """Converts a date string from 'YYYY-MM-DDTHH:MM:SS.sssZ' format to 'MM/DD/YY' format."""
        if date_str is not None:
            try:
                # Parse the date string to a datetime object, ignoring the timezone for simplicity
                date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                # Format the datetime object to 'MM/DD/YY' string format
                return date_obj.strftime("%m/%d/%y")
            except ValueError:
                # Returns original date string if parsing fails
                return date_str
        else:
            return "Not Viewed"

    @staticmethod
    def calculate_days_overdue(due_date, current_date):
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        current_date = datetime.strptime(current_date, "%Y-%m-%d")
        return (current_date - due_date).days if current_date > due_date else 0

    def organize_invoice_data(self):
        response_data = self.response_data
        current_date = datetime.now().strftime("%Y-%m-%d")

        organized_data = {}
        for edge in response_data["data"]["business"]["invoices"]["edges"]:
            node = edge["node"]
            customer_name = node["customer"]["name"]
            if customer_name not in organized_data:
                organized_data[customer_name] = []

            days_overdue = self.calculate_days_overdue(node["dueDate"], current_date) if node[
                                                                                             "status"] != "Paid" else 0

            invoice_info = {
                "invoiceNumber": node["invoiceNumber"],
                "lastViewedAt": self.format_date(node.get("lastViewedAt", "N/A")),
                "viewUrl": node["viewUrl"],
                "daysOverdue": days_overdue,
                # Assuming phone number is available from the node or some other source
                "firstName": node["customer"]["firstName"],
                "phoneNumber": node["customer"]["mobile"],
                "email" : node["customer"]["email"],
                "dueDate" : node["dueDate"]
            }

            organized_data[customer_name].append(invoice_info)

        return organized_data


# Example usage
if __name__ == "__main__":
    auth_token = "your_wave_api_token"
    business_id = "your_business_id"
    invoice_query = """
    query ($businessId: ID!) {
        business(id: $businessId) {
            invoices {
                edges {
                    node {
                        invoiceNumber
                        dueDate
                        status
                        lastViewedAt
                        viewUrl
                        customer {
                            name
                            mobile
                        }
                    }
                }
            }
        }
    }
    """
    wave_invoice_manager = WaveInvoiceManager(auth_token, business_id)
    response_data = wave_invoice_manager.fetch_invoice_data(invoice_query, variables={"businessId": business_id})
    organized_data = wave_invoice_manager.organize_invoice_data(response_data)
    print(organized_data)
