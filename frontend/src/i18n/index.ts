import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";

import en from "./locales/en.json";
import zhCN from "./locales/zh-CN.json";
import zhTW from "./locales/zh-TW.json";

const STORAGE_KEY = "arts-cs-language";

// M-48: Map i18n language codes to HTML lang attribute values
const languageCodeMap: Record<string, string> = {
  en: "en",
  "zh-CN": "zh-CN",
  "zh-TW": "zh-TW",
};

// M-48: Update HTML lang attribute when language changes
function updateHtmlLang(lng: string) {
  if (typeof document !== "undefined") {
    document.documentElement.lang = languageCodeMap[lng] || lng;
  }
}

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      "zh-CN": { translation: zhCN },
      "zh-TW": { translation: zhTW },
    },
    fallbackLng: "en",
    interpolation: { escapeValue: false },
    detection: {
      order: ["localStorage", "navigator"],
      lookupLocalStorage: STORAGE_KEY,
      caches: ["localStorage"],
    },
  });

// M-48: Set initial language and listen for changes
updateHtmlLang(i18n.language);
i18n.on("languageChanged", updateHtmlLang);

export default i18n;
export { STORAGE_KEY };
