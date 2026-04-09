/** M-47: Detect high/low contrast preference for accessibility */

import { useState, useEffect } from "react";

type ContrastPreference = "no-preference" | "more" | "less" | "custom";

export function usePrefersContrast(): ContrastPreference {
  const [contrastPreference, setContrastPreference] = useState<ContrastPreference>("no-preference");

  useEffect(() => {
    // Check for high contrast (more)
    const moreQuery = window.matchMedia("(prefers-contrast: more)");
    // Check for low contrast (less)
    const lessQuery = window.matchMedia("(prefers-contrast: less)");
    // Check for custom contrast
    const customQuery = window.matchMedia("(prefers-contrast: custom)");

    const updatePreference = () => {
      if (moreQuery.matches) {
        setContrastPreference("more");
      } else if (lessQuery.matches) {
        setContrastPreference("less");
      } else if (customQuery.matches) {
        setContrastPreference("custom");
      } else {
        setContrastPreference("no-preference");
      }
    };

    updatePreference();

    moreQuery.addEventListener("change", updatePreference);
    lessQuery.addEventListener("change", updatePreference);
    customQuery.addEventListener("change", updatePreference);

    return () => {
      moreQuery.removeEventListener("change", updatePreference);
      lessQuery.removeEventListener("change", updatePreference);
      customQuery.removeEventListener("change", updatePreference);
    };
  }, []);

  return contrastPreference;
}
