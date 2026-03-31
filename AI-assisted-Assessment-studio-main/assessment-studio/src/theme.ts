import { alpha, createTheme } from "@mui/material/styles";

const bg = "#F6F8FB";
const paper = "#FFFFFF";
const paperSoft = "#F9FBFC";
const border = "#E3E8EE";
const borderStrong = "#CED7E1";
const text = "#17212B";
const textSecondary = "#60707F";
const textMuted = "#8693A0";
const primary = "#1E6676";
const primaryHover = "#15515F";
const primarySoft = "#E8F2F5";
const info = "#3C7396";
const infoBg = "#EEF5FA";
const success = "#46705C";
const successBg = "#EEF5F1";
const warning = "#8D6A34";
const warningBg = "#F8F2E7";
const error = "#A14740";
const errorBg = "#FAEFEE";

export const studioTheme = createTheme({
  cssVariables: true,
  spacing: 8,
  palette: {
    mode: "light",
    primary: {
      main: primary,
      dark: primaryHover,
      light: primarySoft,
      contrastText: paper
    },
    secondary: {
      main: textSecondary,
      dark: text,
      light: paperSoft,
      contrastText: paper
    },
    background: {
      default: bg,
      paper
    },
    text: {
      primary: text,
      secondary: textSecondary,
      disabled: textMuted
    },
    divider: border,
    info: {
      main: info,
      light: infoBg
    },
    success: {
      main: success,
      light: successBg
    },
    warning: {
      main: warning,
      light: warningBg
    },
    error: {
      main: error,
      light: errorBg
    }
  },
  shape: {
    borderRadius: 16
  },
  typography: {
    fontFamily: 'var(--font-ui), sans-serif',
    h1: {
      fontFamily: 'var(--font-ui), sans-serif',
      fontSize: 'clamp(1.9rem, 3vw, 2.45rem)',
      lineHeight: 1.08,
      fontWeight: 680,
      letterSpacing: '-0.04em'
    },
    h2: {
      fontFamily: 'var(--font-ui), sans-serif',
      fontSize: 'clamp(1.25rem, 1.6vw, 1.55rem)',
      lineHeight: 1.2,
      fontWeight: 660,
      letterSpacing: '-0.03em'
    },
    h3: {
      fontFamily: 'var(--font-ui), sans-serif',
      fontSize: '0.98rem',
      lineHeight: 1.34,
      fontWeight: 640,
      letterSpacing: '-0.01em'
    },
    h4: {
      fontFamily: 'var(--font-ui), sans-serif',
      fontSize: '0.9rem',
      lineHeight: 1.35,
      fontWeight: 640
    },
    body1: {
      fontSize: '0.96rem',
      lineHeight: 1.65,
      color: text
    },
    body2: {
      fontSize: '0.88rem',
      lineHeight: 1.55,
      color: textSecondary
    },
    button: {
      textTransform: 'none',
      fontWeight: 600,
      letterSpacing: 0
    },
    overline: {
      fontSize: '0.7rem',
      lineHeight: 1.4,
      letterSpacing: '0.06em',
      fontWeight: 700,
      color: textMuted
    },
    caption: {
      fontSize: '0.78rem',
      lineHeight: 1.45,
      color: textMuted
    }
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          color: text,
          backgroundColor: bg
        },
        code: {
          fontFamily: 'var(--font-mono), monospace'
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          border: `1px solid ${border}`,
          boxShadow: `0 1px 2px ${alpha('#0F172A', 0.04)}, 0 10px 30px ${alpha('#0F172A', 0.025)}`
        }
      }
    },
    MuiCard: {
      styleOverrides: {
        root: {
          border: `1px solid ${border}`,
          boxShadow: `0 1px 2px ${alpha('#0F172A', 0.035)}`
        }
      }
    },
    MuiButton: {
      defaultProps: {
        disableElevation: true
      },
      styleOverrides: {
        root: {
          minHeight: 42,
          borderRadius: 14,
          paddingInline: 18,
          fontSize: '0.9rem',
          boxShadow: 'none'
        },
        containedPrimary: {
          backgroundColor: primary,
          color: paper,
          '&:hover': {
            backgroundColor: primaryHover,
            boxShadow: 'none'
          }
        },
        outlined: {
          borderColor: borderStrong,
          backgroundColor: paper,
          '&:hover': {
            borderColor: primary,
            backgroundColor: alpha(primarySoft, 0.72)
          }
        },
        outlinedPrimary: {
          color: primary
        },
        text: {
          color: textSecondary,
          '&:hover': {
            backgroundColor: alpha(primary, 0.06)
          }
        },
        textPrimary: {
          color: primary
        }
      }
    },
    MuiChip: {
      styleOverrides: {
        root: {
          height: 27,
          borderRadius: 999,
          backgroundColor: paperSoft,
          border: `1px solid ${alpha(borderStrong, 0.9)}`,
          color: textSecondary,
          fontWeight: 600
        },
        sizeSmall: {
          height: 23,
          fontSize: '0.72rem'
        },
        colorPrimary: {
          backgroundColor: primarySoft,
          borderColor: alpha(primary, 0.14),
          color: primary
        },
        colorSecondary: {
          backgroundColor: paperSoft,
          borderColor: border,
          color: textSecondary
        },
        colorSuccess: {
          backgroundColor: successBg,
          borderColor: alpha(success, 0.18),
          color: success
        },
        colorWarning: {
          backgroundColor: warningBg,
          borderColor: alpha(warning, 0.18),
          color: warning
        },
        colorError: {
          backgroundColor: errorBg,
          borderColor: alpha(error, 0.18),
          color: error
        }
      }
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          borderColor: border
        }
      }
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 14,
          backgroundColor: paper,
          '& .MuiOutlinedInput-notchedOutline': {
            borderColor: borderStrong
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: alpha(primary, 0.55)
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: primary,
            borderWidth: 1
          }
        },
        input: {
          fontSize: '0.92rem'
        }
      }
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          height: 6,
          borderRadius: 999,
          backgroundColor: alpha(primary, 0.1)
        },
        bar: {
          borderRadius: 999
        }
      }
    },
    MuiSlider: {
      styleOverrides: {
        root: {
          color: primary,
          paddingBlock: 10
        },
        rail: {
          backgroundColor: alpha(primary, 0.14)
        },
        track: {
          border: 0
        },
        thumb: {
          width: 15,
          height: 15,
          boxShadow: 'none',
          border: `2px solid ${paper}`
        }
      }
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: 14,
          border: `1px solid ${border}`,
          alignItems: 'center',
          boxShadow: 'none'
        },
        standardInfo: {
          backgroundColor: infoBg,
          color: info
        },
        standardSuccess: {
          backgroundColor: successBg,
          color: success
        },
        standardWarning: {
          backgroundColor: warningBg,
          color: warning
        },
        standardError: {
          backgroundColor: errorBg,
          color: error
        }
      }
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          textWrap: 'pretty'
        }
      }
    }
  }
});
