from flask import Flask, render_template, request
from markupsafe import escape
from urllib.parse import urlparse
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_folder="static", template_folder="templates")

# Optional secure cookie defaults (handy once you add sessions/auth)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

# If running behind a reverse proxy (e.g., Nginx), this makes request.is_secure accurate
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Demo product data
products = [
    {"id": 1, "name": "Stylish Camera", "price": 299.99, "image": "Men_cloth.png", "badge": "New", "rating": 4.8},
    {"id": 2, "name": "Wireless Headphones", "price": 149.99, "image": "Headset.png", "badge": "Top", "rating": 4.6},
    {"id": 3, "name": "Smart Watch", "price": 199.99, "image": "Watch.png", "badge": "Sale", "rating": 4.7},
]

def safe_internal_path(candidate: str) -> str:
    """
    Allow only site-relative paths (no scheme/host).
    Falls back to '/offers' if invalid or empty.
    """
    if not candidate:
        return "/offers"
    try:
        p = urlparse(candidate)
        # Only allow paths like "/something" with no scheme/host and no protocol-relative //
        if not p.scheme and not p.netloc and candidate.startswith("/") and not candidate.startswith("//"):
            return candidate
    except Exception:
        pass
    return "/offers"

@app.after_request
def set_security_headers(resp):
    # Strict CSP: no external JS/CSS; serve fonts locally if you use them
    csp = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self'; "
        "font-src 'self'; "
        "script-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    )
    resp.headers["Content-Security-Policy"] = csp
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"] = "geolocation=()"
    # Send HSTS only when HTTPS is in use (or FORCE_HSTS=1 for staging)
    if request.is_secure or os.environ.get("FORCE_HSTS") == "1":
        resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    return resp

@app.route("/")
def index():
    # Explicitly escape any reflected text (Jinja also auto-escapes)
    welcome_text = escape(request.args.get("welcome", ""))
    # Footer link must be internal; anything else falls back to /offers
    ext_offer = safe_internal_path(request.args.get("next", ""))
    return render_template("index.html", products=products, welcome_text=welcome_text, ext_offer=ext_offer)

@app.route("/offers")
def offers():
    # Simple internal target used by the safe link fallback
    return render_template("offers.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)