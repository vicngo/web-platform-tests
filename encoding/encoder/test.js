var tests = [];
var cplist = [];
var numTests = null;
var numFrames = 2;
var chunkSize = 500;
var numChunks = null;
var frames = null;
var frames = null;
var forms = null;
var seperator = ",";
var encodedSeperator = encodeURIComponent(",");
var currentChunkIndex = 0;

setup(function() {
    // set up a sparse array of all unicode codepoints listed in the index
    // "Let pointer be the index pointer for code point in index jis0208."
    var codepoints = []  // index is unicode cp, value is pointer
    for (p=0; p < jis0208.length; p++) {
        if (jis0208[p] != null  && codepoints[jis0208[p]] == null) {
            // if there are duplicates, select the first pointer
            codepoints[jis0208[p]] = p
        }
    }
    codepoints[0x2022] = codepoints[0xFF0D];  // "If code point is U+2022, set it to U+FF0D. "

    // convert the information into a simple array of objects that can be easily traversed
    var currentChunk = [];
    var currentTests = [];
    cplist = [currentChunk];
    tests = [currentTests]
    for (i=0; i< codepoints.length; i++) {
        if (currentChunk.length == chunkSize) {
            currentChunk = [];
            cplist.push(currentChunk);
            currentTests = [];
            tests.push(currentTests);
        }
        if (codepoints[i] != null) {
            var item = {};
            currentChunk.push(item)
            item.cp = i;
            item.ptr = makePercentEncodedEsc(codepoints[i]);
            currentTests.push(async_test("cp " + String.fromCodePoint(item.cp)));
        }
    }

    numChunks = cplist.length;

    for (var i=0; i<numFrames; i++) {
        var frame = document.createElement("iframe");
        frame.id = frame.name = "frame-" + i;
        document.body.appendChild(frame);
        var form = document.createElement("form");
        form.id = 'form-' + i;
        form.method = "GET";
        form.action = "dummy.html";
        form.acceptCharset = "euc-jp";
        form.target = frame.id;
        var input = document.createElement("input");
        input.id = input.name = "input-" + i;
        form.appendChild(input)
        document.body.appendChild(form);
    }

    addEventListener("load", function () {
        frames = Array.prototype.slice.call(document.getElementsByTagName("iframe"));
        forms = Array.prototype.slice.call(document.getElementsByTagName("form"));
        inputs = Array.prototype.slice.call(document.getElementsByTagName("input"));
        for (var i=0; i<Math.min(numFrames, numChunks); i++) {
            runNext(i);
        }
    });

});

function runNext(id) {
    var i = currentChunkIndex;
    currentChunkIndex += 1;

    var iframe = frames[id];
    var form = forms[id];
    var input = inputs[id];

    input.value = cplist[i].map(function(x) {
        return String.fromCodePoint(x.cp)
    }).join(seperator);
    form.submit();

    iframe.onload = function () {
        var url = iframe.contentWindow.location;
        var query = url.search;
        var result_string = query.substr(query.indexOf('=') + 1);
        var results = result_string.split(encodedSeperator);

        for (var j=0; j<cplist[i].length; j++) {
            var t = tests[i][j];
            t.step(function() {
                assert_equals(results[j], cplist[i][j].ptr);
            });
            t.done();
            }
        if (currentChunkIndex < numChunks) {
            runNext(id);
        }
    };
}

function makePercentEncodedEsc (pointer) {
    // uses the Encoding spec algorithm to generate a %-encoded byte sequence representing a EUC-JP character
    // excluding ASCII
    // pointer: integer, a number from the first column in the JIS 0208 index
    var lead = Math.floor(pointer/94) + 0xA1
    var trail = (pointer % 94) + 0xA1
    return '%'+lead.toString(16).toUpperCase()+'%'+trail.toString(16).toUpperCase()
}
