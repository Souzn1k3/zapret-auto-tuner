import time
import requests
import dns.resolver

def test_connection(domain: str) -> dict:
    """
    Checks connection to a target domain via DNS resolution and HTTP requests.
    Returns metrics to help the LLM diagnose the type of block.
    """
    result = {
        "domain": domain,
        "dns_resolved": False,
        "dns_ip": None,
        "http_status": None,
        "http_error": None,
        "latency_ms": None
    }
    
    # 1. DNS Diagnostic
    try:
        answers = dns.resolver.resolve(domain, 'A')
        result["dns_resolved"] = True
        result["dns_ip"] = answers[0].to_text()
    except Exception as e:
        result["dns_resolved"] = False
        result["http_error"] = f"DNS Error: {type(e).__name__}"
        return result  # Cannot proceed without DNS (unless hijacked, which might resolve to wrong IP)

    # 2. HTTP Diagnostic (testing DPI drops / connection reset)
    start_time = time.time()
    try:
        # Use timeout to detect DPI drops
        response = requests.get(f"https://{domain}", timeout=2)
        result["http_status"] = response.status_code
        result["latency_ms"] = int((time.time() - start_time) * 1000)
    except requests.exceptions.ConnectionError as e:
        result["http_error"] = "Connection Reset / DPI Block"
    except requests.exceptions.Timeout:
        result["http_error"] = "Timeout / DPI Drop"
    except Exception as e:
        result["http_error"] = str(e)
        
    return result
