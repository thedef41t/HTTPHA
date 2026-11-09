import re

def unsafe_csp(csp: str) -> bool:
    for directives in csp.split(";"):
        parts = directives.strip().split()
        if not parts:
            continue
        for source in parts[1:]:
            if source == "*":
                return True
            if source in ("'unsafe-inline'", "'unsafe-eval'"):
                return True
    return False

def request_header_checker(headers: dict) -> dict:
    normalized_headers = {key.lower(): value for key, value in headers.items()}
    list = []

    # ----------------------------------------------------------------------------------------------
    csp = normalized_headers.get("content-security-policy")
    if not csp:
        list.append({
            "header": "Content-Security-Policy",
            "message": "CSP is missing. Possible XSS risk!"
        })
    elif unsafe_csp(csp):
        list.append({
            "header": "Content-Security-Policy",
            "message": "CSP contains unsafe directives (eg. * or unsafe-inline/eval)"
        })
    # ----------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------
    hsts = normalized_headers.get("strict-transport-security")
    if not hsts:
        list.append({
            "header": "Strict-Transport-Security",
            "message": "HSTS is missing. Possible insecure connection!"
        })
    match_max_age = re.search(r"max-age=(\d+)", hsts)
    if not match_max_age:
        list.append({
            "header": "Strict-Transport-Security",
            "message": "`max-age` directive is missing!"
        })
    max_age_seconds = int(match_max_age.group(1))
    one_year_age = 31536000
    if max_age_seconds < one_year_age:
        list.append({
            "header": "Strict-Transport-Security",
            "message": "`max-age` directive is weak!"
        })
    # ----------------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------
    acao = normalized_headers.get("access-control-allow-origin")
    if acao and acao.strip() == "*":
        list.append({
            "header": "Access-Control-Allow-Origin",
            "message": "ACAO contains unsafe directives!"
        })
    # ----------------------------------------------------------------------------------------------

    return list
