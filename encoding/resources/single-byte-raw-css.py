def main(request, response):
  response.headers.set("Content-Type", "text/css;charset=" + request.GET.first("label"))
  bytes = []
  for byte in xrange(255):
      if byte in [0x0A, 0x0C, 0x0D, 0x22, 0x5C]:
          bytes.append(chr(0x5C))
          bytes.append(chr(byte))
      else:
          bytes.append(chr(byte))
  response.content = "body::before { content:\"" + "".join(bytes) + "\" }"
