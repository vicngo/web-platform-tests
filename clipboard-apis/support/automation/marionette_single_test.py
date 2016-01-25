import argparse
import re
import time

from marionette import Marionette
from marionette_driver import Actions
from marionette_driver import keys
from marionette_driver.errors import NoSuchElementException

from Tkinter import Tk


def marionette_single_test(url):

    print('Will connect to desktop...')
    m_instance = Marionette(host='localhost', port=2828)
    m_instance.start_session()
    print('Opening %s...' % url)
    m_instance.navigate(url)

    time.sleep(1)

    try:
        result = m_instance.execute_script('return document.activeElement.tagName ==="INPUT"')
        print('focused? %s' % result)
    except:
        pass

    # Check what data is supposed to be on the clipboard when this test runs
    # -- look for this type of instruction in the test page:
    # Please place this on the clipboard before continuing the test: "clipboard text"

    instructions = m_instance.find_element('css selector', 'p').text
    rx_cbinit = re.compile('Please place this on the clipboard before continuing the test: "(.*)"')
    rx_result = rx_cbinit.search(instructions)
    if rx_result:
        print('Will set clipboard: %s ' % rx_result.group(1))
        set_clipboard_data(rx_result.group(1))
    else:
        set_clipboard_data('')

    # Detect what event the test expects. This can be either cut,copy,paste or
    # a manual button click. Look either for this string:
    # Test in progress, waiting for paste event
    # or a BUTTON element with text "Click here to run test"
    rx_event = re.compile('Test in progress, waiting for (cut|copy|paste) event')
    rx_result = rx_event.search(instructions)
    if rx_result:
        print('Will trigger event: %s' % rx_result.group(1))
        trigger_clipboard_event(m_instance, rx_result.group(1))
    else:
        try:
            print('Will click button')
            btn = m_instance.find_element('css selector', 'button')
            if btn:
                btn.click()
            else:
                raise Warning('WOT? Not sure how to automate this test: %s' % url)
        except NoSuchElementException:
            print('No button')
            raise

    # Now something will supposedly happen..
    time.sleep(1)
    # Look for this instruction:
    # This test passes if this text is now on the system clipboard: "clipboard text"
    rx_expected = re.compile('This test passes if this text is now on the system clipboard: "(.*)"')
    rx_result = rx_expected.search(m_instance.find_element('css selector', 'p').text)
    test_result = None
    if rx_result:
        print('Will post result, comparing "%s" to "%s" ' % (Tk().clipboard_get(), rx_result.group(1)))
        test_result = Tk().clipboard_get() == rx_result.group(1)
        m_instance.execute_script('window.wrappedJSObject.result(arguments[0])', script_args=[test_result])
    # If this instruction is *not* in the page,
    # the test likely already knows if it passed or failed.
    # We only need to call result() if JS can't determine
    # pass or fail from within the page.
    # However, for the output it's convenient to read pass/fail information
    # from the DOM for the other tests too, so let's do that so the method can
    # return consistent values..

    if test_result is None:
        try:
            m_instance.find_element('css selector', 'section#summary div.pass')
            test_result = True
        except NoSuchElementException:
            test_result = False
        try:
            m_instance.find_element('css selector', 'section#summary div.fail')
            test_result = False
        except NoSuchElementException:
            pass
    m_instance.delete_session()

    return test_result


def set_clipboard_data(data):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(data)  # TODO: figure out how to do multiple types
    r.destroy()


def trigger_clipboard_event(marionette_instance, evt):
    print('will trigger %s' % evt)
    key = ''
    if evt == 'copy':
        key = 'c'
    elif evt == 'paste':
        key = 'v'
    elif evt == 'cut':
        key = 'x'
    else:
        raise ValueError('Unknown event: %s' % evt)
    print('will chain actions..')
    action = Actions(marionette_instance)
    action.key_down(keys.Keys.CONTROL).key_down(key).key_up(key).key_up(keys.Keys.CONTROL)
    print('ready..')
    action.perform()
    print('done!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=("Run a clipboard test case automated"))
    parser.add_argument("test", type=str, help="Test case URL", default=None)
    args = parser.parse_args()

    if not args.test:
        print("Required argument: test case URL")
        quit()

    test_result = marionette_single_test(args.test)
    print(test_result)
