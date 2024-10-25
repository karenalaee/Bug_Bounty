import requests
from bs4 import BeautifulSoup

def scan_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                if "login" in link.get('href', '').lower() or "signup" in link.get('href', '').lower():
                    print(f"Found login/signup page: {link.get('href')}")
                    # Perform additional testing on the login/signup page
                    check_login_page(link.get('href'))
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def check_login_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            for form in forms:
                if "login" in form.get('action', '').lower():
                    print(f"Found login form on {url}")
                    # Perform additional testing on the login form
                    test_login_form(form, url)
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def test_login_form(form, url):
    # Perform various tests on the login form
    # Check for weak password policies
    # Test for default credentials
    # Test for SQL injection vulnerabilities
    # Check for missing security headers
    # ...
    print("Performing additional tests on the login form...")
    # Save the logs to logs.txt
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"Performing additional tests on the login form: {form}\n")

    # Check for SQL injection vulnerabilities
    sql_injection_tests = [
        "' OR 1=1--",
        "' OR '1'='1",
        "') OR ('1'='1",
        "') OR ('1'='1'--",
        "') OR ('1'='1'-- -"
    ]
    for test in sql_injection_tests:
        form_data = {
            'username': test,
            'password': test
        }
        response = requests.post(url, data=form_data)
        if "SQL syntax" in response.text:
            report_bug(url, "SQL Injection", f"Potential SQL injection vulnerability found with payload: {test}")

    # Check for XSS vulnerabilities
    xss_tests = [
        "<script>alert('XSS')</script>",
        '"><script>alert("XSS")</script>',
        "'/><script>alert(/XSS/)</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg/onload=alert('XSS')>"
    ]
    for test in xss_tests:
        form_data = {
            'username': test,
            'password': test
        }
        response = requests.post(url, data=form_data)
        if test in response.text:
            report_bug(url, "Cross-Site Scripting (XSS)", f"Potential XSS vulnerability found with payload: {test}")

    # Check for missing security headers
    headers = response.headers
    missing_headers = []
    required_headers = [
        'X-Frame-Options',
        'Content-Security-Policy',
        'X-Content-Type-Options',
        'Strict-Transport-Security',
        'Referrer-Policy'
    ]
    for header in required_headers:
        if header not in headers:
            missing_headers.append(header)
    if missing_headers:
        report_bug(url, "Missing Security Headers", f"The following security headers are missing: {', '.join(missing_headers)}")

def report_bug(url, bug_type, description):
    # Code to report the bug to the bug bounty program
    print(f"Reporting bug: {url} - {bug_type} - {description}")
    # Save the bug details to bugs.txt
    with open('bugs.txt', 'a') as bug_file:
        bug_file.write(f"{url} - {bug_type} - {description}\n")

def main():
    target_website = input("Enter the target website URL: ")
    print(f"Starting bug bounty scan for {target_website}")
    scan_website(target_website)
    print("Bug bounty scan completed.")

if __name__ == "__main__":
    main()