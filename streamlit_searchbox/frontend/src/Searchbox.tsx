import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from "react";

import SearchboxStyle from "./styling";
import Select, { InputActionMeta, components } from "react-select";
import { debounce } from "lodash";

type Option = {
  value: string;
  label: string;
};

interface State {
  menu: boolean;
  option: Option | null;
  inputValue: string;
}

interface StreamlitReturn {
  interaction: "submit" | "search" | "reset";
  value: any;
}
const Input = (props: any) => <components.Input {...props} isHidden={false} />;

export function streamlitReturn(interaction: string, value: any): void {
  Streamlit.setComponentValue({
    interaction: interaction,
    value: value,
  } as StreamlitReturn);
}

class Searchbox extends StreamlitComponentBase<State> {
  public state: State = {
    menu: false,
    option: null,
    inputValue: this.props.args.default_searchterm || "",
  };

  private ref: any = React.createRef();

  constructor(props: any) {
    super(props);

    // bind the search function and debounce to avoid too many requests
    // this should be bound to the streamlit state, since we still want to
    // keep proper track of the `inputValue` state
    if (props.args.debounce && props.args.debounce > 0) {
      this.callbackSearchReturn = debounce(
        this.callbackSearchReturn.bind(this),
        props.args.debounce,
      );
    }
  }

  private getStyleFromTheme = (): SearchboxStyle => {
    return new SearchboxStyle(
      this.props.theme,
      this.props.args.style_overrides?.searchbox || {},
    );
  };

  private isInputTrackingActive = (): boolean => {
    return this.props.args.edit_after_submit !== "disabled";
  };

  private callbackSearchReturn = (input: string): void => {
    streamlitReturn("search", input);
  };

  /**
   * new keystroke on searchbox
   * @param input
   * @param _
   * @returns
   */
  private callbackSearch = (input: string): void => {
    this.setState({
      inputValue: input,
      option: null,
    });

    this.callbackSearchReturn(input);
  };

  /**
   * reset button was clicked
   */
  private callbackReset(): void {
    this.setState({
      menu: false,
      option: null,
      inputValue: "",
    });

    streamlitReturn("reset", null);
  }

  /**
   * submitted selection, clear optionally
   * @param option
   */
  private callbackSubmit(option: Option) {
    if (this.props.args.clear_on_submit) {
      this.setState({
        menu: false,
        inputValue: "",
        option: null,
      });
    } else {
      let input = "";

      switch (this.props.args.edit_after_submit) {
        case "current":
          input = this.state.inputValue;
          break;

        case "option":
          input = option.label;
          break;

        case "concat":
          input = this.state.inputValue + " " + option.label;
          break;
      }

      this.setState({
        menu: false,
        option: option,
        inputValue: input,
      });
    }

    streamlitReturn("submit", option.value);
  }

  /**
   * show searchbox with label on top
   * @returns
   */
  public render = (): ReactNode => {
    // always focus the input field to enable edits
    const onFocus = () => {
      if (this.isInputTrackingActive() && this.state.inputValue) {
        this.state.inputValue && this.ref.current.select.inputRef.select();
      }
    };

    const style = this.getStyleFromTheme();

    // option when the clear button is shown
    const clearable = this.props.args.style_overrides?.clear?.clearable;

    return (
      // HTH:
      <div style={this.props.args.style_overrides?.wrapper || {}}>
        {this.props.args.label && (
          <div style={style.label}>{this.props.args.label}
           {this.props.args.help && (
	     style.iconHelp(
               this.props.args.help,
               this.props.args.style_overrides?.help
             )
           )}
          </div>
        )}

        <Select
          // showing the disabled react-select leads to the component
          // not showing the inputValue but just an empty input field
          // we therefore need to re-render the component if we want to keep the focus
          value={
            this.state.option === null &&
            this.state.inputValue &&
            clearable === "always"
              ? {
                  value: null,
                  label: null,
                }
              : this.state.option
          }
          inputValue={
            // for edit_after_submit we want to disable the tracking
            // since the inputValue is equal to the value
            this.isInputTrackingActive() ||
            // only use this for the initial default value
            this.props.args.default_searchterm === this.state.inputValue
              ? this.state.inputValue
              : undefined
          }
          isClearable={clearable !== "never"}
          isSearchable={true}
          styles={style.select}
          options={this.props.args.options}
          placeholder={this.props.args.placeholder}
          // component overrides
          components={{
            ClearIndicator: (props) =>
              style.clearIndicator(
                props,
                this.props.args.style_overrides?.clear || {},
              ),
            DropdownIndicator: () =>
              style.iconDropdown(
                this.state.menu,
                this.props.args.style_overrides?.dropdown || {},
              ),
            IndicatorSeparator: () => null,
            Input: this.isInputTrackingActive() ? Input : components.Input,
            Option: (props) =>
              style.optionHighlighted(
                props,
                this.props.args.style_overrides?.searchbox?.option
                  ?.highlightColor || undefined,
              ),
          }}
          // handlers
          filterOption={(_, __) => true}
          onFocus={() => onFocus()}
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          onChange={(option: any, a: any) => {
            switch (a.action) {
              case "select-option":
                this.callbackSubmit(option);
                return;

              case "clear":
                this.callbackReset();
                return;
            }
          }}
          onInputChange={(
            inputValue: string,
            { action, prevInputValue }: InputActionMeta,
          ) => {
            switch (action) {
              // ignore menu close or blur/unfocus events
              case "input-change":
                this.callbackSearch(inputValue);
                return;
            }
          }}
          onMenuOpen={() => this.setState({ menu: true })}
          onMenuClose={() => this.setState({ menu: false })}
          menuIsOpen={this.props.args.options && this.state.menu}
        />
      </div>
    );
  };
}
export default withStreamlitConnection(Searchbox);
