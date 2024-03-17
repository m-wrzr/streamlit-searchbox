import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib";
import React, { ReactNode } from "react";

import SearchboxStyle from "./styling";
import Select, { InputActionMeta, components } from "react-select";

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
    inputValue: "",
  };

  private style = new SearchboxStyle(this.props.theme!);
  private ref: any = React.createRef();

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

    streamlitReturn("search", input);
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
      this.setState({
        menu: false,
        option: option,
        // current
        // option
        // disabled
        inputValue:
          this.props.args.edit_after_submit === "current"
            ? this.state.inputValue
            : option.label,
      });
    }

    streamlitReturn("submit", option.value);
  }

  /**
   * show searchbox with label on top
   * @returns
   */
  public render = (): ReactNode => {
    const editableAfterSubmit =
      this.props.args.edit_after_submit !== "disabled";

    // always focus the input field to enable edits
    const onFocus = () => {
      if (editableAfterSubmit && this.state.inputValue) {
        this.state.inputValue && this.ref.current.select.inputRef.select();
      }
    };

    return (
      <div>
        {this.props.args.label && (
          <div style={this.style.label}>{this.props.args.label}</div>
        )}

        <Select
          // showing the disabled react-select leads to the component
          // not showing the inputValue but just an empty input field
          // we therefore need to re-render the component if we want to keep the focus
          value={this.state.option}
          inputValue={editableAfterSubmit ? this.state.inputValue : undefined}
          isClearable={true}
          isSearchable={true}
          styles={this.style.select}
          options={this.props.args.options}
          placeholder={this.props.args.placeholder}
          // component overrides
          components={{
            ClearIndicator: (props) => this.style.clearIndicator(props),
            DropdownIndicator: () => this.style.iconDropdown(this.state.menu),
            IndicatorSeparator: () => null,
            Input: editableAfterSubmit ? Input : components.Input,
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
