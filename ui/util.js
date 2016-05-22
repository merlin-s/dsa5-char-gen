function padl(pad, str) {
  if (typeof str === 'undefined')
    return pad;
  return (pad + str).slice(-Math.max(pad.length, str.length))
}
function padr(pad, str) {
  if (typeof str === 'undefined')
    return pad;
  return (str + pad).substring(0, pad.length);
}
function tint(bc, tc, alpha) {
  return Qt.tint(bc, Qt.rgba(tc.r, tc.g, tc.b, tc.a * alpha))
}