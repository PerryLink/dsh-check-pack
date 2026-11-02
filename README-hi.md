# dsh-check-pack

> **Renamed from [`@perrylink/dsh-checkers`](https://www.npmjs.com/package/@perrylink/dsh-checkers).** The old scoped package is deprecated; install **`dsh-check-pack`**.

> **पैकेज नाम:** `dsh-check-pack` इंस्टॉल करें (वर्तमान shim)। `dsh-check-pack` पुराना alias है; अब यह यहाँ इंगित करता है।

**53-अनुपालन प्लगइन PerryLink अनुपालन सूट** के लिए एक-कमांड इंस्टॉलर।

```sh
# npm
dsh plugin --profile web add dsh-check-pack

# available now: the GitHub git channel
dsh plugin --profile web add github:PerryLink/dsh-check-pack
```

यह सभी अनुपालन प्लगइन इंस्टॉल करता है और एक ही bundle परत से सभी 53 Cordis पंक्तियाँ जोड़ता है।
हर अनुपालन प्लगइन का अपना npm नाम, नियम पैक, README और संस्करण रहता है; यह पैकेज केवल सूट
प्रवेश बिंदु है।

**दायरा:** चीनी दस्तावेज़ जाँच (व्यापार, सीमा शुल्क, निविदा, HSE, चिकित्सा, कानून,
सरकार, विनिर्माण)। हर अनुपालन प्लगइन केवल अंतर बताता है, कानूनी/चिकित्सीय/सीमा शुल्क निर्णय नहीं।
सटीक सूची और संस्करण `checkers.json` में हैं।

**अनइंस्टॉल:** `dsh plugin --profile web remove dsh-check-pack`.

Apache-2.0. बदलाव के बाद `node build.mjs` चलाएँ।
