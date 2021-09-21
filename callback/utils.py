import base64
import hashlib
import hmac


def base64_url_encode(string):
    """
    Removes any `=` used as padding from the encoded string.
    """
    encoded = base64.urlsafe_b64encode(string)
    return encoded.rstrip(b"=")


def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "=" * padding_factor
    return base64.b64decode(str(inp).translate(dict(zip(map(ord, u"-_"), u"+/"))))


def parse_signed_request(signed_request, secret, request):
    sign_part = signed_request.split(".", 2)
    # encoded_sig = l[0]
    # protected = {"alg": "HS256", "typ": "JWT"}
    sign_part[2] = base64_url_decode(sign_part[2])

    q = hmac.new(
        secret,
        sign_part[0].encode() + ".".encode() + base64_url_encode(request),
        hashlib.sha256,
    ).digest()
    if q == sign_part[2]:
        return True
    else:
        return False
