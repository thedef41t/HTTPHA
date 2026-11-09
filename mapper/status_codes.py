def analyze_status_code(status_code: int) -> dict:

    if 200 <= status_code < 300:
        return {
            "category": "Success",
            "description": "Response successfully receivced",
            "is_reachable": True,
            "color": "green3"
        }

    elif 300 <= status_code < 400: 
        return {
            "category": "Redirection",
            "description": "Futher actions needs to be taken to complete request",
            "is_reachable": True,
            "color": "yellow2"
        }

    elif 400 <= status_code < 500: 
        return {
            "category": "Client Error",
            "description": "Request contains bad syntax or cannot be fulfilled",
            "is_reachable": False,
            "color": "orange1"
        }

    elif 400 <= status_code < 500: 
        return {
            "category": "Server Error",
            "description": "Server failed to respond",
            "is_reachable": False,
            "color": "red"
        }

    else:
        return {
            "category": "Unknown",
            "description": "Unrecognized or invalid status code",
            "is_reachable": False,
            "color": "gray30"
        }
