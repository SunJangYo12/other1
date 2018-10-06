from bs4 import BeautifulSoup as bs


def generatePayload(self, query):
        payload = {}.copy()
	counter = 1
        if query:
            payload.update(query)
        payload['__req'] = str_base(counter, 36)
        payload['seq'] = "1"
        counter += 1
        return payload

def get(self, url, query=None, timeout=30, fix_request=False, as_json=False, error_retries=3, free=False):
        payload = _generatePayload(query)

	print "----- Tunggu ------"
	r = self._session.get(url, headers=self._header, params=payload, timeout=timeout, verify=self.ssl_verify)
	if not fix_request:
		return r
	try:
		return check_request(r, as_json=as_json)
	except FBchatFacebookError as e:
		if error_retries > 0 and self._fix_fb_errors(e.fb_error_code):
			return self._get(url, query=query, timeout=timeout, fix_request=fix_request, as_json=as_json, error_retries=error_retries-1)
		raise e

soup = bs(get("https://free.facebook.com").text, "html.parser")
