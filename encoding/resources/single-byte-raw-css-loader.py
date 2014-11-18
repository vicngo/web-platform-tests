def main(request, response):
  response.headers.set("Content-Type", "text/html;charset=utf-8")
  response.content = "<!doctype html><link rel=stylesheet href=single-byte-raw-css.py?label=" + request.GET.first("label") + ">"
