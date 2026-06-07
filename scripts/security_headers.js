function handler(event) {
    var response = event.response;
    var headers = response.headers;

    // Strict-Transport-Security (HSTS)
    headers['strict-transport-security'] = { value: 'max-age=63072000; includeSubdomains; preload' };
    
    // X-Content-Type-Options
    headers['x-content-type-options'] = { value: 'nosniff' };
    
    // X-Frame-Options
    headers['x-frame-options'] = { value: 'DENY' };
    
    // X-XSS-Protection
    headers['x-xss-protection'] = { value: '1; mode=block' };
    
    // Referrer-Policy
    headers['referrer-policy'] = { value: 'same-origin' };

    return response;
}
