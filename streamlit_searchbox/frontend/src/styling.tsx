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
import { fill } from "lodash";
class SearchboxStyle {
  theme: any;
  label: any;
  select: StylesConfig;

  constructor(theme: any) {
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
      menuList: (styles: any) => ({
        ...styles,
        backgroundColor: theme.backgroundColor,
      }),
      singleValue: (styles: any) => ({
        ...styles,
        color: theme.textColor,
      }),
      // custom styles needed for default mobile paste behavior
      // https://github.com/JedWatson/react-select/issues/4106
      // filler text and icons
      input: (styles: any) => ({
        ...styles,
        color: theme.textColor,
        // expand input area to fill all the available area
        gridTemplateColumns: "0 minmax(min-content, 1fr)",
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
        };
      },
    };
  }

  /**
   * Dropdown icon, adjusted if menu is open
   * @param menu
   * @returns
   */
  iconDropdown(props: any, menu: boolean, styles: any) {
    console.log(props);
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <DropdownIcon
          // streamlit has fixed icon sizes at 15x15
          width={15}
          height={15}
          fill={this.theme.textColor}
          style={{
            marginRight: "8px",
          }}
          transform={menu && styles && styles.rotate ? "rotate(180)" : ""}
          {...styles}
        />
      </div>
    );
  }

  /**
   * Clear icon, props are passed by react-select
   * @param props
   * @returns
   */
  clearIndicator(props: any, styles: any) {
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
      // overwrite default styles if provided
      ...styles,
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
