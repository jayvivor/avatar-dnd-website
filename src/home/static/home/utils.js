function nlListed(iterable, style = " / ", useAnd = false) {
    let listed = Array.from(iterable, model => String(model));
    if (listed.length === 0) return "";
    if (listed.length === 1) return listed[0];
    let finalStr = listed.slice(0, -2).join(style);
    if (listed.length > 2) finalStr += style;
    finalStr += useAnd ? `${listed[listed.length - 2]} and ${listed[listed.length - 1]}` : `${listed[listed.length - 2]}${style}${listed[listed.length - 1]}`;
    return finalStr;
}
