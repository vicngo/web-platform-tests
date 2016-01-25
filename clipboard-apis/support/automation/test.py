from marionette import Marionette

m_instance = Marionette(host='localhost', port=2828)
m_instance.start_session()
#m_instance.navigate('data:text/html,<html><head><title>Test document</title></head><body><form><input autofocus></form></body>')
#m_instance.navigate('http://localhost:8000/marionette-input-focus.htm')
m_instance.navigate('http://localhost:8000/clipboard-apis/getdata_method_in_paste_event_retrieving_plain_text_paste_on_document.html')
result = m_instance.execute_script('return document.activeElement.tagName ==="INPUT"')

print(result)
