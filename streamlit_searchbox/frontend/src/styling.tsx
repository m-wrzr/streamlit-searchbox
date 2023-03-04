import React from "react"
import {
  CSSObjectWithLabel,
  StylesConfig,
  ControlProps,
  OptionProps,
} from "react-select"

import { ReactComponent as Dropdown } from "./icons/st-arrow.svg"
import { ReactComponent as Clear } from "./icons/st-clear.svg"

class SearchboxStyle {
  theme: any
  label: any
  select: StylesConfig

  constructor(theme: any) {
    this.theme = theme
    this.label = {
      color: theme.textColor,
      fontSize: "0.82em",
      fontWeight: 400,
      font: theme.font,
      marginBottom: "0.85rem",
    }

    this.select = buildStyleSelect(theme)
  }

  /**
   * Dropdown icon, adjusted if menu is open
   * @param menu
   * @returns
   */
  iconDropdown(menu: boolean) {
    return (
      <div>
        <Dropdown
          // streamlit has fixed icon sizes at 15x15
          width={15}
          height={15}
          fill={this.theme.textColor}
          style={{
            marginRight: menu ? "7px" : "8px",
            marginBottom: menu ? "0px" : "3px",
          }}
        />
      </div>
    )
  }

  /**
   * Clear icon, props are passed by react-select
   * @param props
   * @returns
   */
  clearIndicator(props: any) {
    const {
      innerProps: { ref, ...restInnerProps },
    } = props

    return (
      <Clear
        {...restInnerProps}
        ref={ref}
        fill={this.theme.fadedText60}
        // streamlit has fixed icon sizes at 15x15
        width={15}
        height={15}
      />
    )
  }
}

function buildStyleSelect(theme: any): any {
  return {
    // overall option list
    menuList: (styles: any) => ({
      ...styles,
      backgroundColor: theme.backgroundColor,
    }),
    // filler text and icons
    input: (styles: any) => ({ ...styles, color: theme.textColor }),
    //
    singleValue: (styles: any) => ({
      ...styles,
      color: theme.textColor,
    }),
    // placeholder text
    placeholder: (styles: any) => ({
      ...styles,
      color: theme.fadedText60,
    }),
    // searchbox and others, e.g. options window
    control: (styles: CSSObjectWithLabel, { isFocused }: ControlProps) => {
      return {
        ...styles,
        backgroundColor: theme.secondaryBackgroundColor,
        color: theme.secondaryBackgroundColor,
        border: !isFocused
          ? "1px transparent"
          : "1px solid " + theme.primaryColor,
        boxShadow: "none",
        "&:hover": {
          border: !isFocused
            ? "1px transparent"
            : "1px solid " + theme.primaryColor,
        },
      }
    },
    // single cell in option list
    option: (
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
        cursor: isDisabled ? "not-allowed" : "Search ...",
      }
    },
  }
}

export default SearchboxStyle
