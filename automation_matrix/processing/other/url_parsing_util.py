from urllib.parse import urlparse, parse_qs
import urllib
from common import pretty_print
import tldextract


# The world's greatest URL Utility ever made!!!!!

def check_for_domain_property(entry):
    search_string = "sc-domain:"
    sc_domain = False

    if search_string in entry:
        sc_domain = True  # Set the flag to True if found
        start_index = entry.find(search_string) + len(search_string)
        url = entry[start_index:]

        if "%3A" in url:
            url = urllib.parse.unquote(url)
    else:
        url = entry

    return sc_domain, url


def parse_url_and_details(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    hostname = parsed_url.hostname
    port = parsed_url.port
    path = parsed_url.path
    params = parsed_url.params
    query = parsed_url.query
    fragment = parsed_url.fragment

    if scheme == '':
        top_level_domain, remainder, www = get_tld_and_remaining(path)
        path = ''
    else:
        top_level_domain, remainder, www = get_tld_and_remaining(hostname)
    print(parsed_url, scheme, netloc, hostname, port, path, params, query, fragment, top_level_domain, remainder, www)
    return parsed_url, scheme, netloc, hostname, port, path, params, query, fragment, top_level_domain, remainder, www


def get_tld_and_remaining(netloc):
    extracted = tldextract.extract(netloc)

    www = 'www' in extracted.subdomain

    subdomain = extracted.subdomain.replace('www.', '').replace('www', '')
    remaining_parts = [subdomain, extracted.domain] if subdomain else [extracted.domain]
    remaining = '.'.join(filter(None, remaining_parts))

    tld = extracted.suffix

    return tld, remaining, www


def get_subdomain(remaining):
    parts = remaining.split('.')
    if len(parts) > 1:
        subdomain = '.'.join(parts[:-1])
    else:
        subdomain = ''

    if subdomain:
        subdomain_end_index = len(subdomain) + 1
        sld = remaining[subdomain_end_index:]
    else:
        sld = remaining

    return subdomain, sld


def parse_query(query):
    parsed_query = parse_qs(query)

    if not parsed_query:
        return {}

    query_components = {k: v[0] for k, v in parsed_query.items() if v}

    return query_components


def parse_text_fragment(fragment):
    prefix = ':~:text='

    if fragment.startswith(prefix):
        text_fragment = fragment[len(prefix):]
        decoded_fragment = urllib.parse.unquote(text_fragment)
        components = decoded_fragment.split(',')

        fragment_components = {
            'startString': components[0] if len(components) > 0 else '',
            'prefix': components[1] if len(components) > 1 else '',
            'textStart': components[2] if len(components) > 2 else '',
            'textEnd': components[3] if len(components) > 3 else '',
            'suffix': components[4] if len(components) > 4 else ''
        }

        return fragment_components
    else:
        return fragment


def url_analysis_orchestrator(url_input):
    sc_domain_flag, url = check_for_domain_property(url_input)
    parsed_url, scheme, netloc, hostname, port, path, params, query, fragment, top_level_domain, remainder, www = parse_url_and_details(url)

    subdomain, sld = get_subdomain(remainder)

    parsed_query_components = parse_query(query)
    parsed_fragment = parse_text_fragment(fragment)

    if isinstance(parsed_fragment, dict):
        fragment_details = {
            'complete_fragment': fragment,
            **parsed_fragment
        }
    else:
        fragment_details = {
            'complete_fragment': fragment,
            'parsed_fragment': parsed_fragment
        }

    analysis = {
        'url': url_input,
        'sc_domain': sc_domain_flag,
        'scheme': scheme,
        'www': www,
        'subdomain': subdomain,
        'second_level_domain': sld,
        'top_level_domain': top_level_domain,
        'path': path,
        'fragment': fragment_details,
        'query': query,
        'parsed_query_components': parsed_query_components,
    }
    return analysis

def get_query_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    query = analysis_results[0]['query']
    print(f"Query: {query}")

def get_fragment_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    fragment = analysis_results[0]['fragment']
    print(f"Fragment: {fragment}")

def get_path_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    path = analysis_results[0]['path']
    print(f"Path: {path}")

def get_subdomain_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    subdomain = analysis_results[0]['subdomain']
    print(f"Subdomain: {subdomain}")

def get_second_level_domain_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    second_level_domain = analysis_results[0]['second_level_domain']
    print(f"Second Level Domain: {second_level_domain}")

def get_top_level_domain_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    top_level_domain = analysis_results[0]['top_level_domain']
    print(f'Top Level Domain: {top_level_domain}')

def get_www_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    www = analysis_results[0]['www']
    print(f"WWW: {www}")

def get_scheme_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    scheme = analysis_results[0]['scheme']
    print(f"Scheme: {scheme}")

def get_sc_domain_from_url(url):
    analysis_results = analyze_url_list(url_inputs)

    sc_domain = analysis_results[0]['sc_domain']
    print(f"SC Domain: {sc_domain}")

def get_clean_url_from_url(url):
    # Assuming analyze_url_list takes a list of URLs and returns a list of analysis results
    analysis_results = analyze_url_list([url])

    # Get the first (and presumably only) analysis result
    analysis = analysis_results[0]

    # Reconstruct the URL without query and fragment
    clean_url = ''
    if analysis['scheme']:
        clean_url += analysis['scheme'] + '://'
    if analysis['www']:
        clean_url += 'www.'
    if analysis['subdomain']:
        clean_url += analysis['subdomain'] + '.'
    clean_url += analysis['second_level_domain']
    if analysis['top_level_domain']:
        clean_url += '.' + analysis['top_level_domain']
    if analysis['path']:
        clean_url += analysis['path']

    print(f"Clean URL: {clean_url}")
    return clean_url



def analyze_url_list(url_inputs):
    results = []
    for url in url_inputs:
        analysis = url_analysis_orchestrator(url)
        results.append(analysis)
    return results


if __name__ == "__main__": # Getting a lot of info, but need to now have a central function that returns exactly what we need with a simple call.

    url_inputs = [
        "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTv2y22cR_Vj8hsgi8WqKz_EmMU2msv5wvMlhI6uUL-5zWWNAfKRhk0uxrV"
        #"sc-domain:sst4.superseotemplate.com",
        # "https://cosmeticinjectables.com/blog/what-is-novathreads-dr-soleiman-answers-your-questions/#What_Are_the_Advantages_of_NovaThreads",
        # "https://www.example.co.uk/blog/article/search?docid=720&hl=en#dayone",
        # "https://datadestruction.com/",
        # "https://www.datadestruction.com",
        # "http://www.datadestruction.com/",
        # "https://www.datadestruction.com/locations",
        # "http://www.datadestruction.com/locations/",
        # "https://platform.openai.com/playground/p/I8JHcMBsrP4rDTDsyMFkgkp3?mode=chat",
        # "www.allgreenrecycling.com/",
        # "sc-domain:nazarianplasticsurgery.com",
        # "https://search.google.com/search-console/performance/search-analytics?resource_id=sc-domain%3Acosmeticinjectables.com&num_of_months=16&breakdown=page",
    ]

    analysis_results = analyze_url_list(url_inputs)

    for result in analysis_results:
        pretty_print_data(result)

    get_query_from_url(url_inputs)
    get_fragment_from_url(url_inputs)
    get_path_from_url(url_inputs)
    get_subdomain_from_url(url_inputs)
    get_second_level_domain_from_url(url_inputs)
    get_top_level_domain_from_url(url_inputs)
    get_www_from_url(url_inputs)
    get_scheme_from_url(url_inputs)
    get_sc_domain_from_url(url_inputs)
    # get_clean_url_from_url(url_inputs)
