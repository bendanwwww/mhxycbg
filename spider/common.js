const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
window = dom.window;
document = window.document;
XMLHttpRequest = window.XMLHttpRequest;

var a1 = ['substring', 'atob', 'charCodeAt', 'push', 'test'];
(function (a2, a3) {
    var a5 = function (a4) {
        while (--a4) {
            a2['push'](a2['shift']());
        }
    };
    a5(++a3);
}(a1, 0x153));
var a6 = function (a7, a8) {
    a7 = a7 - 0x0;
    var a9 = a1[a7];
    return a9;
};
function decode_desc(a11) {
    if (a11 = a11['replace'](/^\s+|\s+$/g, ''), !/^@[\s\S]*@$/ [a6('0x0')](a11)) return a11;
    var a18 = (/\b_k=([^;]*)/ ['exec'](document['cookie']) || [])[0x1] || '';
    if (a11 = a11['replace'](/^@|@$/g, ''), /^[^@]+@[\s\S]+/ ['test'](a11)) {
        var a19 = a11['indexOf']('@');
        a18 = a11[a6('0x1')](0x0, a19), a11 = a11['substring'](a19 + 0x1);
    }
    var a12 = function s(a11) {
        try {
            return window['eval']('(' + a11 + ')');
        } catch (_0x40b9c3) {
            return null;
        }
    }(a11 = window[a6('0x2')](a11));
    a12 && 'object' == typeof a12 && a12['d'] && (a12 = a12['d']);
    for (var a13 = [], a14 = 0x0, a16 = 0x0; a16 < a12['length']; a16++) {
        var a15 = a12['charCodeAt'](a16),
            a17 = a18[a6('0x3')](a14 % a18['length']);
        a14 += 0x1, a15 = 0x1 * a15 ^ a17, a13[a6('0x4')](a15['toString'](0x2));
    }
    return function d(a11) {
        for (var a18 = [], a19 = 0x0; a19 < a11['length']; a19++) a18['push'](window['String']['fromCharCode'](window['parseInt'](a11[a19], 0x2)));
        return a18['join']('');
    }(a13);
}
