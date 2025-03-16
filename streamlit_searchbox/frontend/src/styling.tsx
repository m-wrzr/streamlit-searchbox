import React from "react";
import {
  CSSObjectWithLabel,
  StylesConfig,
  ControlProps,
  OptionProps,
  components,
} from "react-select";
import { HelpCircle as HelpCircleIcon } from "react-feather"
import {
  StatefulTooltip,
} from "baseui/tooltip"

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
   * Help icon and tooltip
   * @param menu
   * @returns
   */
  iconHelp(help: string, overrides: any) {
    return (
      <span style={{
        float: "right"
      }}>
        <StatefulTooltip
          content={<div
                     style={{
                       boxSizing: "border-box",
                       font: this.theme.font,
                       fontFamily: "Source Sans Pro, sans-serif",
                       fontSize: "0.82em",
                       overflow: "auto",
                       padding: "1em",
                     }}
                   >
                   {help}
                   </div>
          }
          placement={"auto"}
          showArrow={false}
          popoverMargin={10}
          onMouseEnterDelay={1}
          overrides={{
            Body: {
              style: {
                // This is annoying, but a bunch of warnings get logged when the
                // shorthand version `borderRadius` is used here since the long
                // names are used by BaseWeb and mixing the two is apparently
                // bad :(
                borderTopLeftRadius: "100px",
                borderTopRightRadius: "100px",
                borderBottomLeftRadius: "100px",
                borderBottomRightRadius: "100px",

                paddingTop: "0 !important",
                paddingBottom: "0 !important",
                paddingLeft: "0 !important",
                paddingRight: "0 !important",

                backgroundColor: "transparent",
              },
            },
            Inner: {
              style: {
                backgroundColor: this.theme.backgroundColor,
                color: this.theme.textColor,
                fontSize: "0.82em",
                fontWeight: "400",

                // See the long comment about `borderRadius`. The same applies here
                // to `padding`.
                paddingTop: "0 !important",
                paddingBottom: "0 !important",
                paddingLeft: "0 !important",
                paddingRight: "0 !important",
              },
            },
          }} 
        > 
          <HelpCircleIcon 
            style={{
              stroke: "rgba(49, 51, 63, 0.6)",
              strokeWidth: "2.25",
              width: "16px",
              height: "16px",
            }}
	  />
        </StatefulTooltip>
      </span>
    )
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
          marginLeft: "2px",
        }}
      >
        <DropdownIcon
          // streamlit has fixed icon sizes at 15x15
          width={15}
          height={15}
          stroke={this.theme.textColor}
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

    // fill / stroke color might be passed by react-select
    iconProps = {
      ...iconProps,
      ref: ref,
      // streamlit has fixed icon sizes at 15x15
      width: 22,
      height: 22,
      ...overrides,
    };

    // if stroke or fill in iconProps don't set hover color
    const isColorOverride = "stroke" in iconProps || "fill" in iconProps;

    if (iconProps.icon === "cross") {
      return (
        <ClearIconCross
          // replace opacity single overlapping strokes will look weird
          stroke={this.theme.textColor}
          strokeHover={isColorOverride ? undefined : this.theme.primaryColor}
          {...iconProps}
        />
      );
    }

    if (iconProps.icon === "circle-unfilled") {
      return (
        <ClearIconCircularUnfilled
          // replace opacity single overlapping strokes will look weird
          stroke={this.theme.textColor}
          strokeHover={isColorOverride ? undefined : this.theme.primaryColor}
          {...iconProps}
          // icon can't be filled
          fill="none"
        />
      );
    }

    return (
      <ClearIconCircularFilled
        fill={this.theme.fadedText60}
        fillHover={isColorOverride ? undefined : this.theme.textColor}
        {...iconProps}
      />
    );
  }

  optionHighlighted = (props: any, highlightColor: string | undefined) => {
    if (!highlightColor || highlightColor === "") {
      return <components.Option {...props} />;
    }

    const { children, selectProps } = props;
    const inputValue = selectProps.inputValue as string;

    // split into parts that match or don't match the inputValue
    const parts =
      typeof children === "string"
        ? children.split(new RegExp(`(${inputValue})`, "gi"))
        : [];

    return (
      <components.Option {...props}>
        {parts.map((part, index) =>
          part.toLowerCase() === inputValue.toLowerCase() ? (
            <span key={index} style={{ backgroundColor: highlightColor }}>
              {part}
            </span>
          ) : (
            part // no match
          ),
        )}
      </components.Option>
    );
  };
}

export default SearchboxStyle;
