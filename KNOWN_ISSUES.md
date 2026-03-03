# Known Issues

## kramdown-rfc emits deprecated RFCXML v2 elements even with `-3` flag

**Tool:** [kramdown-rfc](https://github.com/cabo/kramdown-rfc) v1.7.31
**Flag used:** `kramdown-rfc -3` (should enable RFCXML v3 output per RFC 7991)

### Problem

kramdown-rfc generates deprecated RFCXML v2 elements even when the `-3` (v3 mode) flag is passed. This causes 22+ warnings from [idnits](https://github.com/ietf-tools/idnits):

- **`<spanx>`** — deprecated in RFC 7991 §3.7. Should emit `<em>`, `<strong>`, or `<tt>` instead.
- **`<list>`** — deprecated in RFC 7991 §3.4. Should emit `<dl>`, `<ul>`, or `<ol>` instead.
- **`title` attribute on `<references>`** — should use a `<name>` child element instead.
- **`<?line ?>` processing instructions** — present in output.

### Expected behavior

With `-3`, kramdown-rfc should emit RFCXML v3 (RFC 7991) compliant elements:
- `<spanx style="emph">` → `<em>`
- `<spanx style="strong">` → `<strong>`
- `<spanx style="verb">` → `<tt>`
- `<list style="symbols">` → `<ul>`
- `<list style="numbers">` → `<ol>`
- `<list style="hanging">` → `<dl>`
- `<references title="...">` → `<references><name>...</name>`

### Reproduction

```sh
kramdown-rfc -3 draft-zzn-dvs.md > output.xml
npx @ietf-tools/idnits output.xml
# Observe DEPRECATED_ELEMENT warnings for <spanx> and <list>
```

## kramdown-rfc duplicates RFC2119/RFC8174 when BCP14 is in YAML header

**Tool:** kramdown-rfc v1.7.31
**idnits warning:** `PREFER_BCP14_REF`

### Problem

idnits recommends referencing BCP14 instead of RFC2119/RFC8174 individually. However, adding `BCP14:` to the kramdown-rfc YAML header while using `{::boilerplate bcp14-tagged}` causes duplicate `anchor="RFC2119"` and `anchor="RFC8174"` entries in the generated XML, because:

1. The `BCP14` referencegroup expands to include RFC2119 and RFC8174
2. The `{::boilerplate bcp14-tagged}` macro independently injects RFC2119 and RFC8174 references

This causes xml2rfc to fail with: `Error: ID RFC2119 redefined`

### Workaround

Keep `RFC2119:` and `RFC8174:` in the YAML header individually (without `BCP14:`). Accept the `PREFER_BCP14_REF` idnits warning.

## idnits false positive: `sitemaps.org` flagged as non-reserved domain

**Tool:** [idnits](https://github.com/ietf-tools/idnits) v3.0.0-alpha.74
**idnits warning:** `INVALID_DOMAIN_TLD`

### Problem

idnits flags `sitemaps.org` as a non-reserved domain per RFC 6761, suggesting `.example.org` instead. However, `sitemaps.org` is a real external domain referenced as an informative reference (`[SITEMAP]`) — it is not being used as an example domain. This is a false positive.
