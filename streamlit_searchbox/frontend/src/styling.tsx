import React from "react";
import {
  CSSObjectWithLabel,
  StylesConfig,
  ControlProps,
  OptionProps,
} from "react-select";

import {
  DropdownIcon,
  ClearIconCircularFilled,
  ClearIconCross,
  ClearIconCircularUnfilled,
} from "./icons";
class SearchboxStyle {
  theme: any;
  label: any;
  select: StylesConfig;

  constructor(theme: any, overrides: any) {
    this.theme = theme;
    this.label = {
      color: theme.textColor,
      fontSize: "0.82em",
      fontWeight: 400,
      font: theme.font,
      marginBottom: "0.85rem",
    };

    this.select = {
      // overall option list
      menuList: (styles: any) => {
        return {
          ...styles,
          backgroundColor: theme.backgroundColor,
          ...(overrides.menuList || {}),
        };
      },
      singleValue: (styles: any) => ({
        ...styles,
        color: theme.textColor,
        ...(overrides.singleValue || {}),
      }),
      // custom styles needed for default mobile paste behavior
      // https://github.com/JedWatson/react-select/issues/4106
      // filler text and icons
      input: (styles: any) => ({
        ...styles,
        color: theme.textColor,
        // expand input area to fill all the available area
        gridTemplateColumns: "0 minmax(min-content, 1fr)",
        ...(overrides.input || {}),
      }),
      // placeholder text
      placeholder: (styles: any) => {
        return {
          ...styles,
          pointerEvents: "none",
          userSelect: "none",
          MozUserSelect: "none",
          WebkitUserSelect: "none",
          msUserSelect: "none",
          color: theme.fadedText60,
          ...(overrides.placeholder || {}),
        };
      },
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
          ...(overrides.control || {}),
        };
      },
      // single cell in option list
      option: (
        styles: CSSObjectWithLabel,
        { isDisabled, isFocused, isSelected }: OptionProps,
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
          ...(overrides.option || {}),
        };
      },
    };
  }

  /**
   * Dropdown icon, adjusted if menu is open
   * @param menu
   * @returns
   */
  iconDropdown(menu: boolean, overrides: any) {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          marginRight: "8px",
        }}
      >
        <DropdownIcon
          // streamlit has fixed icon sizes at 15x15
          width={15}
          height={15}
          fill={this.theme.textColor}
          transform={menu && overrides && overrides.rotate ? "rotate(180)" : ""}
          {...overrides}
        />
      </div>
    );
  }

  /**
   * Clear icon, props are passed by react-select
   * @param props
   * @returns
   */
  clearIndicator(props: any, overrides: any) {
    let {
      innerProps: { ref, ...iconProps },
    } = props;

    iconProps = {
      ...iconProps,
      ref: ref,
      fill: this.theme.fadedText60,
      // streamlit has fixed icon sizes at 15x15
      width: 15,
      height: 15,
      ...overrides,
    };

    if (iconProps.icon === "cross") {
      return (
        <ClearIconCross
          // replace opacity single overlapping strokes will look weird
          stroke={this.theme.textColor}
          {...iconProps}
        />
      );
    }

    if (iconProps.icon === "circle-unfilled") {
      return (
        <ClearIconCircularUnfilled
          // replace opacity single overlapping strokes will look weird
          stroke={this.theme.textColor}
          {...iconProps}
          // icon can't be filled
          fill="none"
        />
      );
    }

    return <ClearIconCircularFilled {...iconProps} />;
  }
}

export default SearchboxStyle;
