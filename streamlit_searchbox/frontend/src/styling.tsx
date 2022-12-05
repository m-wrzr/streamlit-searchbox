import React from "react"
import {
  CSSObjectWithLabel,
  StylesConfig,
  ControlProps,
  OptionProps,
} from "react-select"

import { ReactComponent as SearchIconSvg } from "./magnifying-glass-solid.svg"

/**
 * load svg icon and fill with text color
 * @param theme
 * @returns
 */
export function getStyledIcon(theme: any) {
  return (
    <div>
      <SearchIconSvg
        fill={theme.fadedText60}
        width={24}
        style={{
          marginLeft: "6px",
          marginRight: "6px",
          padding: "4px",
        }}
      />
    </div>
  )
}

/**
 * parameterize react-select style with streamlit data
 * @param theme
 * @returns
 */
export function getStyleConfig(theme: any): StylesConfig {
  // searchbox and others, e.g. options window
  const control = (styles: CSSObjectWithLabel, { isFocused }: ControlProps) => {
    return {
      ...styles,
      backgroundColor: theme.secondaryBackgroundColor,
      color: theme.secondaryBackgroundColor,
      border: !isFocused ? "0px" : "1px solid " + theme.primaryColor,
      boxShadow: "none",
      "&:hover": {
        border: !isFocused ? "0px" : "1px solid " + theme.primaryColor,
      },
    }
  }

  // single cell in option list
  const option = (
    styles: CSSObjectWithLabel,
    { isDisabled, isFocused, isSelected }: OptionProps
  ) => {
    return {
      ...styles,
      backgroundColor: isDisabled
        ? undefined
        : isSelected
        ? theme.secondaryBackgroundColor
        : isFocused
        ? theme.secondaryBackgroundColor
        : theme.backgroundColor,
      // option text
      color: theme.textColor,
      cursor: isDisabled ? "not-allowed" : "default",
    }
  }

  return {
    indicatorSeparator: (styles) => ({
      ...styles,
      backgroundColor: theme.fadedText60,
    }),
    // overall option list
    menuList: (styles) => ({
      ...styles,
      backgroundColor: theme.backgroundColor,
    }),
    // filler text and icons
    input: (styles) => ({ ...styles, color: theme.textColor }),
    singleValue: (styles) => ({ ...styles, color: theme.textColor }),
    placeholder: (styles) => ({ ...styles, color: theme.fadedText60 }),
    // dynamic based on content
    control: control,
    option: option,
  }
}
